import os
import csv

def aggregate_map2check_counts(root_dir):
    """
    Percorre a árvore de diretórios a partir de root_dir procurando arquivos 
    "map2check_output.txt" e, para cada programa, aplica as seguintes regras:
      - Se o conteúdo contém "KLEE: done: total instructions =" e "FALSE" → pontua 1 na coluna map2check(klee)
      - Se contém "SUMMARY: libFuzzer: deadly signal" e "FALSE" e NÃO contém "KLEE: done: total instructions =" → pontua 1 na coluna map2check(fuzzy)
      - Se contém "UNKNOWN" e não contém nenhuma das duas sentenças anteriores → pontua 1 na coluna confirm_unknown
    Retorna:
      - global_counts: dicionário com as contagens globais
      - category_counts: dicionário com as contagens por categoria
      - subcategory_counts: dicionário com as contagens por subcategoria (chave: (categoria, subcategoria))
      - not_matched_programs: lista de dicionários com o nome do programa e sua subcategoria, para os programas
        que não se enquadraram em nenhuma das condições.
    """
    global_counts = {"klee": 0, "fuzzy": 0, "unknown": 0}
    category_counts = {}      # key: category, value: dict com keys "klee", "fuzzy", "unknown"
    subcategory_counts = {}   # key: (category, subcategory), value: dict com keys "klee", "fuzzy", "unknown"
    not_matched_programs = []  # Lista de dicts: {"program_folder": <nome>, "subcategory": <subcategoria>}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "map2check_output.txt" in filenames:
            file_path = os.path.join(dirpath, "map2check_output.txt")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"Erro ao ler {file_path}: {e}")
                continue

            # Verifica as condições
            klee_flag = ("KLEE: done: total instructions =" in content) and ("FALSE" in content)
            fuzzy_flag = ("SUMMARY: libFuzzer: deadly signal" in content) and ("FALSE" in content) and (not ("KLEE: done: total instructions =" in content))
            unknown_flag = ("UNKNOWN" in content) and (not ("KLEE: done: total instructions =" in content)) and (not ("SUMMARY: libFuzzer: deadly signal" in content))

            program_klee = 1 if klee_flag else 0
            program_fuzzy = 1 if fuzzy_flag else 0
            program_unknown = 1 if unknown_flag else 0

            # Determina categoria e subcategoria com base na estrutura:
            # resultados_de_testes/<categoria>/<subcategoria>/<program_folder>/map2check_output.txt
            parts = os.path.normpath(file_path).split(os.sep)
            try:
                idx = parts.index("resultados_de_testes")
            except ValueError:
                idx = 0
            if len(parts) > idx + 3:
                category = parts[idx+1]
                subcategory = parts[idx+2]
            else:
                continue

            # Se nenhuma condição foi satisfeita, adiciona o programa à lista not_matched_programs.
            if not (klee_flag or fuzzy_flag or unknown_flag):
                program_folder = os.path.basename(os.path.dirname(file_path))
                not_matched_programs.append({"program_folder": program_folder, "subcategory": subcategory})

            # Agrega globalmente
            global_counts["klee"] += program_klee
            global_counts["fuzzy"] += program_fuzzy
            global_counts["unknown"] += program_unknown

            # Agrega por categoria
            if category not in category_counts:
                category_counts[category] = {"klee": 0, "fuzzy": 0, "unknown": 0}
            category_counts[category]["klee"] += program_klee
            category_counts[category]["fuzzy"] += program_fuzzy
            category_counts[category]["unknown"] += program_unknown

            # Agrega por subcategoria
            key = (category, subcategory)
            if key not in subcategory_counts:
                subcategory_counts[key] = {"klee": 0, "fuzzy": 0, "unknown": 0}
            subcategory_counts[key]["klee"] += program_klee
            subcategory_counts[key]["fuzzy"] += program_fuzzy
            subcategory_counts[key]["unknown"] += program_unknown

    return global_counts, category_counts, subcategory_counts, not_matched_programs

def update_summary_csv(summary_csv_path, output_csv_path, global_counts, category_counts, subcategory_counts):
    """
    Lê o summary_report.csv, que possui linhas com scope_type (Global, Category, Subcategory)
    e adiciona as colunas "map2check(klee)", "map2check(fuzzy)" e "confirm_unknown" com os valores
    agregados.
    """
    updated_rows = []
    with open(summary_csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ["map2check(klee)", "map2check(fuzzy)", "confirm_unknown"]
        for row in reader:
            scope_type = row.get("scope_type", "")
            if scope_type == "Global":
                row["map2check(klee)"] = global_counts.get("klee", 0)
                row["map2check(fuzzy)"] = global_counts.get("fuzzy", 0)
                row["confirm_unknown"] = global_counts.get("unknown", 0)
            elif scope_type == "Category":
                cat = row.get("scope_name", "")
                cat_counts = category_counts.get(cat, {"klee": 0, "fuzzy": 0, "unknown": 0})
                row["map2check(klee)"] = cat_counts.get("klee", 0)
                row["map2check(fuzzy)"] = cat_counts.get("fuzzy", 0)
                row["confirm_unknown"] = cat_counts.get("unknown", 0)
            elif scope_type == "Subcategory":
                parts = row.get("scope_name", "").split("/")
                if len(parts) == 2:
                    key = (parts[0], parts[1])
                    subcat_counts = subcategory_counts.get(key, {"klee": 0, "fuzzy": 0, "unknown": 0})
                    row["map2check(klee)"] = subcat_counts.get("klee", 0)
                    row["map2check(fuzzy)"] = subcat_counts.get("fuzzy", 0)
                    row["confirm_unknown"] = subcat_counts.get("unknown", 0)
                else:
                    row["map2check(klee)"] = 0
                    row["map2check(fuzzy)"] = 0
                    row["confirm_unknown"] = 0
            else:
                row["map2check(klee)"] = 0
                row["map2check(fuzzy)"] = 0
                row["confirm_unknown"] = 0
            updated_rows.append(row)
    
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

def write_not_matched_csv(not_matched_programs, output_csv_path):
    """
    Escreve um CSV contendo o nome de cada programa que não se enquadrou em nenhuma das condições,
    juntamente com a subcategoria a que pertence.
    """
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["program_folder", "subcategory"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for prog in not_matched_programs:
            writer.writerow(prog)

if __name__ == "__main__":
    resultados_dir = "resultados_de_testes"
    summary_csv_path = os.path.join(resultados_dir, "summary_report.csv")
    updated_summary_csv_path = os.path.join(resultados_dir, "summary_report_with_map2check.csv")
    not_matched_csv_path = os.path.join(resultados_dir, "programs_not_matched.csv")
    
    global_counts, category_counts, subcategory_counts, not_matched_programs = aggregate_map2check_counts(resultados_dir)
    update_summary_csv(summary_csv_path, updated_summary_csv_path, global_counts, category_counts, subcategory_counts)
    write_not_matched_csv(not_matched_programs, not_matched_csv_path)
    
    print(f"Updated summary report generated: {updated_summary_csv_path}")
    print(f"CSV with not matched programs generated: {not_matched_csv_path}")
