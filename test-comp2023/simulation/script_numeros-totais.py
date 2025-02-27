import os
import re
import csv

def parse_tempos_file(file_path, category, subcategory):
    """
    Parses a tempos.txt file and returns a list of entries.
    Each entry is a dict with keys:
      - program_file: constructed as "subcategory/filename"
      - time: the numeric time (as a string)
      - category: category (parent folder)
      - subcategory: subcategory (current folder)
      - status: one of 'FALSE', 'TRUE', 'UNKNOWN', or None if not provided
      - coverage: extracted coverage value (as a string) or 'N/A'
      - testcov_result: result string from TESTCOV line or 'N/A'
    """
    entries = []
    current_entry = None

    # Updated pattern: match lines like "sep05-1.i: 84.532 segundos" or "file.c: 21.301 segundos"
    pattern = re.compile(r'^\s*(?P<filename>[^:]+\.(?:c|i)):\s+(?P<time>\d+\.\d{1,3})\s+segundos')

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        # Check if this line starts a new entry
        match = pattern.match(line)
        if match:
            # Save the previous entry, if any
            if current_entry is not None:
                entries.append(current_entry)
            
            filename = match.group('filename')
            time_value = match.group('time')
            current_entry = {
                'program_file': f"{subcategory}/{filename}",
                'time': time_value,
                'category': category,
                'subcategory': subcategory,
                'status': None,
                'coverage': 'N/A',
                'testcov_result': 'N/A'
            }
        
        # Detect status lines
        elif line in ['FALSE', 'TRUE', 'UNKNOWN']:
            if current_entry is not None:
                current_entry['status'] = line
        
        # Detect TESTCOV lines and extract coverage and result info
        elif line.startswith('TESTCOV:'):
            if current_entry is not None:
                testcov_data = line.split('TESTCOV: ')[-1]
                coverage_match = re.search(r'suite/([\d.]+)%', testcov_data)
                result_match = re.search(r'Result: (\w+)', testcov_data)
                if coverage_match:
                    current_entry['coverage'] = coverage_match.group(1)
                if result_match:
                    current_entry['testcov_result'] = result_match.group(1)
    
    # Append the last entry if present
    if current_entry is not None:
        entries.append(current_entry)
    
    return entries

def gather_all_entries(root_dir):
    """
    Walks through the folder tree starting at root_dir,
    looks for tempos.txt in subdirectories (assuming structure: .../category/subcategory/tempos.txt)
    and returns a list of all parsed entries.
    """
    all_entries = []
    for root, dirs, files in os.walk(root_dir):
        if 'tempos.txt' in files:
            path_parts = root.split(os.sep)
            # Assumes structure: .../category/subcategory
            if len(path_parts) >= 2:
                category = path_parts[-2]
                subcategory = path_parts[-1]
            else:
                category = path_parts[-1]
                subcategory = path_parts[-1]
            file_path = os.path.join(root, 'tempos.txt')
            entries = parse_tempos_file(file_path, category, subcategory)
            all_entries.extend(entries)
    return all_entries

def safe_float(value):
    """
    Converts value to float if possible.
    Returns None if conversion fails (e.g., if value is 'N/A').
    """
    try:
        return float(value)
    except:
        return None

def compute_summary(entries):
    """
    Computes a summary dictionary that contains counts and timing metrics per scope (global, category, subcategory).
    Além do sumário atual, são adicionadas as colunas:
      - media_time_excl_360000: média dos tempos, excluindo entradas com time == 360.000
      - media_time_incl_360000: média dos tempos, incluindo entradas com time == 360.000
      - total_time_ge_360000: total de programas com time >= 360.000
    Returns a list of dicts to be written as rows in the summary CSV.
    """
    summary = []
    threshold = 360.0  # Corrigido para 360.0 (segundos)
    
    # Helper function para calcular os tempos
    def calc_time_metrics(group_entries):
        # Converte os valores de "time" para float (filtrando os que não convertem)
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
        'total_FALSE': sum(1 for e in global_entries if e['status'] == 'FALSE'),
        'total_TRUE': sum(1 for e in global_entries if e['status'] == 'TRUE'),
        'total_UNKNOWN': sum(1 for e in global_entries if e['status'] == 'UNKNOWN'),
        'total_coverage_0.0': sum(1 for e in global_entries if safe_float(e['coverage']) == 0.0),
        'total_coverage_pos': sum(1 for e in global_entries if (safe_float(e['coverage']) is not None and safe_float(e['coverage']) > 0.0)),
        'media_time_excl_360000': media_excl,
        'media_time_incl_360000': media_incl,
        'total_time_ge_360000': count_ge
    }
    summary.append(global_counts)
    
    # Summary per category
    categories = set(e['category'] for e in entries)
    for cat in categories:
        cat_entries = [e for e in entries if e['category'] == cat]
        media_excl, media_incl, count_ge = calc_time_metrics(cat_entries)
        cat_counts = {
            'scope_type': 'Category',
            'scope_name': cat,
            'total_program_files': len(cat_entries),
            'total_FALSE': sum(1 for e in cat_entries if e['status'] == 'FALSE'),
            'total_TRUE': sum(1 for e in cat_entries if e['status'] == 'TRUE'),
            'total_UNKNOWN': sum(1 for e in cat_entries if e['status'] == 'UNKNOWN'),
            'total_coverage_0.0': sum(1 for e in cat_entries if safe_float(e['coverage']) == 0.0),
            'total_coverage_pos': sum(1 for e in cat_entries if (safe_float(e['coverage']) is not None and safe_float(e['coverage']) > 0.0)),
            'media_time_excl_360000': media_excl,
            'media_time_incl_360000': media_incl,
            'total_time_ge_360000': count_ge
        }
        summary.append(cat_counts)
    
    # Summary per subcategory
    subcategories = set((e['category'], e['subcategory']) for e in entries)
    for cat, subcat in subcategories:
        subcat_entries = [e for e in entries if e['category'] == cat and e['subcategory'] == subcat]
        media_excl, media_incl, count_ge = calc_time_metrics(subcat_entries)
        subcat_counts = {
            'scope_type': 'Subcategory',
            'scope_name': f"{cat}/{subcat}",
            'total_program_files': len(subcat_entries),
            'total_FALSE': sum(1 for e in subcat_entries if e['status'] == 'FALSE'),
            'total_TRUE': sum(1 for e in subcat_entries if e['status'] == 'TRUE'),
            'total_UNKNOWN': sum(1 for e in subcat_entries if e['status'] == 'UNKNOWN'),
            'total_coverage_0.0': sum(1 for e in subcat_entries if safe_float(e['coverage']) == 0.0),
            'total_coverage_pos': sum(1 for e in subcat_entries if (safe_float(e['coverage']) is not None and safe_float(e['coverage']) > 0.0)),
            'media_time_excl_360000': media_excl,
            'media_time_incl_360000': media_incl,
            'total_time_ge_360000': count_ge
        }
        summary.append(subcat_counts)
    
    return summary

def write_summary_csv(summary, output_csv):
    """
    Writes the summary data (list of dicts) into a CSV file.
    """
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
    all_entries = gather_all_entries(root_dir)
    summary = compute_summary(all_entries)
    output_csv = os.path.join(root_dir, "summary_report.csv")
    write_summary_csv(summary, output_csv)
    print(f"Summary report generated: {output_csv}")
