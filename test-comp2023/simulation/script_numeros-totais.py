import os
import csv

def gather_all_entries_from_csv(root_dir):
    """
    Percorre a árvore de diretórios a partir de root_dir, 
    lê os arquivos CSV (que terminam com "_results.csv") gerados anteriormente,
    e retorna uma lista de entradas (dicionários).
    
    Cada entrada terá os seguintes campos:
      - program_file (no formato "subcategoria/filename")
      - time (como string)
      - status
      - coverage
      - testcov_result
      - category (extraído do diretório onde o CSV está)
      - subcategory (primeira parte do campo program_file)
    """
    all_entries = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('_results.csv'):
                csv_path = os.path.join(root, file)
                # O diretório em que o CSV está é considerado como "category"
                category = os.path.basename(root)
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        prog_file = row.get('program_file', '')
                        if '/' in prog_file:
                            subcategory = prog_file.split('/')[0]
                        else:
                            subcategory = ''
                        row['category'] = category
                        row['subcategory'] = subcategory
                        all_entries.append(row)
    return all_entries

def safe_float(value):
    try:
        return float(value)
    except:
        return None

def compute_summary(entries):
    """
    Calcula um sumário com métricas e contagens em escopos globais, por categoria e por subcategoria.
    
    São calculadas as seguintes métricas:
      - total de programas
      - contagem de status FALSE, TRUE, UNKNOWN
      - contagem de cobertura 0.0 e cobertura positiva
      - média dos tempos (excluindo entradas com time == 360.000)
      - média dos tempos (incluindo entradas com time == 360.000)
      - total de programas com time >= 360.000
    """
    summary = []
    threshold = 360.0

    def calc_time_metrics(group_entries):
        times_incl = [safe_float(e['time']) for e in group_entries if safe_float(e['time']) is not None]
        times_excl = [t for t in times_incl if t != threshold]
        media_excl = sum(times_excl) / len(times_excl) if times_excl else 0
        media_incl = sum(times_incl) / len(times_incl) if times_incl else 0
        count_ge = sum(1 for t in times_incl if t >= threshold)
        return media_excl, media_incl, count_ge

    # Global summary
    global_entries = entries
    media_excl, media_incl, count_ge = calc_time_metrics(global_entries)
    global_counts = {
        'scope_type': 'Global',
        'scope_name': 'All',
        'total_program_files': len(global_entries),
        'total_FALSE': sum(1 for e in global_entries if e.get('status','') == 'FALSE'),
        'total_TRUE': sum(1 for e in global_entries if e.get('status','') == 'TRUE'),
        'total_UNKNOWN': sum(1 for e in global_entries if e.get('status','') == 'UNKNOWN'),
        'total_coverage_0.0': sum(1 for e in global_entries if safe_float(e.get('coverage','N/A')) == 0.0),
        'total_coverage_pos': sum(1 for e in global_entries if (safe_float(e.get('coverage','N/A')) is not None and safe_float(e.get('coverage','N/A')) > 0.0)),
        'media_time_excl_360000': media_excl,
        'media_time_incl_360000': media_incl,
        'total_time_ge_360000': count_ge
    }
    summary.append(global_counts)

    # Summary por categoria
    categories = set(e['category'] for e in entries)
    for cat in categories:
        cat_entries = [e for e in entries if e['category'] == cat]
        media_excl, media_incl, count_ge = calc_time_metrics(cat_entries)
        cat_counts = {
            'scope_type': 'Category',
            'scope_name': cat,
            'total_program_files': len(cat_entries),
            'total_FALSE': sum(1 for e in cat_entries if e.get('status','') == 'FALSE'),
            'total_TRUE': sum(1 for e in cat_entries if e.get('status','') == 'TRUE'),
            'total_UNKNOWN': sum(1 for e in cat_entries if e.get('status','') == 'UNKNOWN'),
            'total_coverage_0.0': sum(1 for e in cat_entries if safe_float(e.get('coverage','N/A')) == 0.0),
            'total_coverage_pos': sum(1 for e in cat_entries if (safe_float(e.get('coverage','N/A')) is not None and safe_float(e.get('coverage','N/A')) > 0.0)),
            'media_time_excl_360000': media_excl,
            'media_time_incl_360000': media_incl,
            'total_time_ge_360000': count_ge
        }
        summary.append(cat_counts)

    # Summary por subcategoria (agrupando por category e subcategory)
    subcats = set((e['category'], e['subcategory']) for e in entries)
    for cat, subcat in subcats:
        subcat_entries = [e for e in entries if e['category'] == cat and e['subcategory'] == subcat]
        media_excl, media_incl, count_ge = calc_time_metrics(subcat_entries)
        subcat_counts = {
            'scope_type': 'Subcategory',
            'scope_name': f"{cat}/{subcat}",
            'total_program_files': len(subcat_entries),
            'total_FALSE': sum(1 for e in subcat_entries if e.get('status','') == 'FALSE'),
            'total_TRUE': sum(1 for e in subcat_entries if e.get('status','') == 'TRUE'),
            'total_UNKNOWN': sum(1 for e in subcat_entries if e.get('status','') == 'UNKNOWN'),
            'total_coverage_0.0': sum(1 for e in subcat_entries if safe_float(e.get('coverage','N/A')) == 0.0),
            'total_coverage_pos': sum(1 for e in subcat_entries if (safe_float(e.get('coverage','N/A')) is not None and safe_float(e.get('coverage','N/A')) > 0.0)),
            'media_time_excl_360000': media_excl,
            'media_time_incl_360000': media_incl,
            'total_time_ge_360000': count_ge
        }
        summary.append(subcat_counts)

    return summary

def write_summary_csv(summary, output_csv):
    fieldnames = [
        'scope_type', 'scope_name',
        'total_program_files',
        'total_FALSE', 'total_TRUE', 'total_UNKNOWN',
        'total_coverage_0.0', 'total_coverage_pos',
        'media_time_excl_360000', 'media_time_incl_360000', 'total_time_ge_360000'
    ]
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary:
            writer.writerow(row)

if __name__ == '__main__':
    root_dir = "resultados_de_testes"
    all_entries = gather_all_entries_from_csv(root_dir)
    summary = compute_summary(all_entries)
    output_csv = os.path.join(root_dir, "summary_report.csv")
    write_summary_csv(summary, output_csv)
    print(f"Summary report generated: {output_csv}")
