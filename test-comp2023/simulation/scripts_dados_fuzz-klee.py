import os
import csv
import re

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
    category_counts = {}
    subcategory_counts = {}
    not_matched_programs = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "map2check_output.txt" in filenames:
            file_path = os.path.join(dirpath, "map2check_output.txt")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"Erro ao ler {file_path}: {e}")
                continue

            klee_flag = ("KLEE: done: total instructions =" in content) and ("FALSE" in content)
            fuzzy_flag = ("SUMMARY: libFuzzer: deadly signal" in content) and ("FALSE" in content) and (not ("KLEE: done: total instructions =" in content))
            unknown_flag = ("UNKNOWN" in content) and (not ("KLEE: done: total instructions =" in content)) and (not ("SUMMARY: libFuzzer: deadly signal" in content))

            program_klee = 1 if klee_flag else 0
            program_fuzzy = 1 if fuzzy_flag else 0
            program_unknown = 1 if unknown_flag else 0

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

            if not (klee_flag or fuzzy_flag or unknown_flag):
                program_folder = os.path.basename(os.path.dirname(file_path))
                not_matched_programs.append({"program_folder": program_folder, "subcategory": subcategory})

            global_counts["klee"] += program_klee
            global_counts["fuzzy"] += program_fuzzy
            global_counts["unknown"] += program_unknown

            if category not in category_counts:
                category_counts[category] = {"klee": 0, "fuzzy": 0, "unknown": 0}
            category_counts[category]["klee"] += program_klee
            category_counts[category]["fuzzy"] += program_fuzzy
            category_counts[category]["unknown"] += program_unknown

            key = (category, subcategory)
            if key not in subcategory_counts:
                subcategory_counts[key] = {"klee": 0, "fuzzy": 0, "unknown": 0}
            subcategory_counts[key]["klee"] += program_klee
            subcategory_counts[key]["fuzzy"] += program_fuzzy
            subcategory_counts[key]["unknown"] += program_unknown

    return global_counts, category_counts, subcategory_counts, not_matched_programs

def aggregate_true_false_counts(root_dir):
    """
    Percorre a árvore de diretórios procurando pelos arquivos "testcov_output.txt"
    nos mesmos diretórios onde existe "map2check_output.txt". Para cada programa, se ele
    for pontuado em klee ou fuzzy (de acordo com map2check_output.txt), extrai a linha
    que contém "Coverage:" do testcov_output.txt e, se o valor de cobertura for > 0, 
    pontua 1 na coluna correspondente.
    
    Retorna:
      - global_tf: dict com chaves "klee" e "fuzzy"
      - category_tf: dict (key: category) com dicts {"klee": valor, "fuzzy": valor}
      - subcategory_tf: dict (key: (category, subcategory)) com dicts {"klee": valor, "fuzzy": valor}
    """
    global_tf = {"klee": 0, "fuzzy": 0}
    category_tf = {}
    subcategory_tf = {}
    
    coverage_regex = re.compile(r'Coverage:\s*([\d.]+)%')
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "map2check_output.txt" in filenames and "testcov_output.txt" in filenames:
            map2check_path = os.path.join(dirpath, "map2check_output.txt")
            testcov_path = os.path.join(dirpath, "testcov_output.txt")
            try:
                with open(map2check_path, "r", encoding="utf-8") as f:
                    map2check_content = f.read()
            except Exception as e:
                print(f"Erro ao ler {map2check_path}: {e}")
                continue
            # Verifica as condições (mesmo que antes)
            klee_flag = ("KLEE: done: total instructions =" in map2check_content) and ("FALSE" in map2check_content)
            fuzzy_flag = ("SUMMARY: libFuzzer: deadly signal" in map2check_content) and ("FALSE" in map2check_content) and (not ("KLEE: done: total instructions =" in map2check_content))
            
            # Se o programa não se enquadra em klee nem em fuzzy, pula.
            if not (klee_flag or fuzzy_flag):
                continue
            
            try:
                with open(testcov_path, "r", encoding="utf-8") as f:
                    testcov_content = f.read()
            except Exception as e:
                print(f"Erro ao ler {testcov_path}: {e}")
                continue
            
            # Procura a linha que contém "Coverage:" e extrai o valor
            match = coverage_regex.search(testcov_content)
            coverage_value = float(match.group(1)) if match and match.group(1) else 0.0
            
            # Só pontua se a cobertura for maior que 0
            tf_klee = 1 if klee_flag and coverage_value > 0 else 0
            tf_fuzzy = 1 if fuzzy_flag and coverage_value > 0 else 0
            
            # Determina categoria e subcategoria (mesma lógica de antes)
            parts = os.path.normpath(map2check_path).split(os.sep)
            try:
                idx = parts.index("resultados_de_testes")
            except ValueError:
                idx = 0
            if len(parts) > idx + 3:
                category = parts[idx+1]
                subcategory = parts[idx+2]
            else:
                continue

            global_tf["klee"] += tf_klee
            global_tf["fuzzy"] += tf_fuzzy

            if category not in category_tf:
                category_tf[category] = {"klee": 0, "fuzzy": 0}
            category_tf[category]["klee"] += tf_klee
            category_tf[category]["fuzzy"] += tf_fuzzy

            key = (category, subcategory)
            if key not in subcategory_tf:
                subcategory_tf[key] = {"klee": 0, "fuzzy": 0}
            subcategory_tf[key]["klee"] += tf_klee
            subcategory_tf[key]["fuzzy"] += tf_fuzzy

    return global_tf, category_tf, subcategory_tf

def update_summary_csv(summary_csv_path, output_csv_path, global_counts, category_counts, subcategory_counts,
                       global_tf, category_tf, subcategory_tf):
    """
    Lê o summary_report.csv, que possui linhas com scope_type (Global, Category, Subcategory),
    e adiciona as colunas "map2check(klee)", "map2check(fuzzy)", "confirm_unknown",
    "true_false_klee" e "true_false_fuzzy" com os valores agregados.
    """
    updated_rows = []
    with open(summary_csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ["map2check(klee)", "map2check(fuzzy)", "confirm_unknown",
                                            "true_false_klee", "true_false_fuzzy"]
        for row in reader:
            scope_type = row.get("scope_type", "")
            if scope_type == "Global":
                row["map2check(klee)"] = global_counts.get("klee", 0)
                row["map2check(fuzzy)"] = global_counts.get("fuzzy", 0)
                row["confirm_unknown"] = global_counts.get("unknown", 0)
                row["true_false_klee"] = global_tf.get("klee", 0)
                row["true_false_fuzzy"] = global_tf.get("fuzzy", 0)
            elif scope_type == "Category":
                cat = row.get("scope_name", "")
                cat_counts = category_counts.get(cat, {"klee": 0, "fuzzy": 0, "unknown": 0})
                row["map2check(klee)"] = cat_counts.get("klee", 0)
                row["map2check(fuzzy)"] = cat_counts.get("fuzzy", 0)
                row["confirm_unknown"] = cat_counts.get("unknown", 0)
                cat_tf = category_tf.get(cat, {"klee": 0, "fuzzy": 0})
                row["true_false_klee"] = cat_tf.get("klee", 0)
                row["true_false_fuzzy"] = cat_tf.get("fuzzy", 0)
            elif scope_type == "Subcategory":
                parts = row.get("scope_name", "").split("/")
                if len(parts) == 2:
                    key = (parts[0], parts[1])
                    subcat_counts = subcategory_counts.get(key, {"klee": 0, "fuzzy": 0, "unknown": 0})
                    row["map2check(klee)"] = subcat_counts.get("klee", 0)
                    row["map2check(fuzzy)"] = subcat_counts.get("fuzzy", 0)
                    row["confirm_unknown"] = subcat_counts.get("unknown", 0)
                    subcat_tf = subcategory_tf.get(key, {"klee": 0, "fuzzy": 0})
                    row["true_false_klee"] = subcat_tf.get("klee", 0)
                    row["true_false_fuzzy"] = subcat_tf.get("fuzzy", 0)
                else:
                    row["map2check(klee)"] = 0
                    row["map2check(fuzzy)"] = 0
                    row["confirm_unknown"] = 0
                    row["true_false_klee"] = 0
                    row["true_false_fuzzy"] = 0
            else:
                row["map2check(klee)"] = 0
                row["map2check(fuzzy)"] = 0
                row["confirm_unknown"] = 0
                row["true_false_klee"] = 0
                row["true_false_fuzzy"] = 0
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
    global_tf, category_tf, subcategory_tf = aggregate_true_false_counts(resultados_dir)
    
    update_summary_csv(summary_csv_path, updated_summary_csv_path, global_counts, category_counts, subcategory_counts,
                       global_tf, category_tf, subcategory_tf)
    write_not_matched_csv(not_matched_programs, not_matched_csv_path)
    
    print(f"Updated summary report generated: {updated_summary_csv_path}")
    print(f"CSV with not matched programs generated: {not_matched_csv_path}")
