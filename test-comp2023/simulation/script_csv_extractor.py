import os
import csv
import re

def parse_tempos_file(file_path, category, subcategory):
    entries = []
    current_entry = None  # Using None to indicate no entry in progress
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        # Detect a new entry based on the file/time line
        if re.match(r'^[^:]+\.c: \d+\.\d{3} segundos', line):
            # Save the previous entry, if any
            if current_entry is not None:
                entries.append(current_entry)
            
            # Parse the file name and time
            parts = line.split(': ')
            filename = parts[0]
            time_value = parts[1].split(' ')[0]  # get the numeric time value
            
            # Build the entry dictionary using subcategory for the program file name
            current_entry = {
                'program_file': f"{subcategory}/{filename}",
                'time': time_value,
                'status': None,
                'coverage': 'N/A',
                'testcov_result': 'N/A'
            }
        
        # Detect status line (TRUE, FALSE, or UNKNOWN)
        elif line in ['FALSE', 'TRUE', 'UNKNOWN']:
            if current_entry is not None:
                current_entry['status'] = line
        
        # Detect the TESTCOV line and extract coverage and result information
        elif line.startswith('TESTCOV:'):
            if current_entry is not None:
                # Remove potential duplicate "TESTCOV:" from the beginning
                testcov_data = line.split('TESTCOV: ')[-1]
                # Look for the coverage percentage after "suite/"
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

def generate_csv_reports(root_dir):
    csv_data = {}
    
    # Walk the directory tree looking for "tempos.txt" files
    for root, dirs, files in os.walk(root_dir):
        if 'tempos.txt' in files:
            path_parts = root.split(os.sep)
            # Determine the category and subcategory.
            # Assumes structure: .../category/subcategory/tempos.txt
            category = path_parts[-2] if len(path_parts) >= 2 else path_parts[-1]
            subcategory = path_parts[-1]
            
            entries = parse_tempos_file(os.path.join(root, 'tempos.txt'), category, subcategory)
            
            if category not in csv_data:
                csv_data[category] = []
            csv_data[category].extend(entries)
    
    # Write a CSV file for each category
    for category, entries in csv_data.items():
        csv_dir = os.path.join(root_dir, category)
        os.makedirs(csv_dir, exist_ok=True)
        csv_path = os.path.join(csv_dir, f'{category}_results.csv')
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'program_file',
                'status',
                'time',
                'coverage',
                'testcov_result'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for entry in entries:
                writer.writerow(entry)

if __name__ == '__main__':
    resultados_dir = "resultados_de_testes"
    generate_csv_reports(resultados_dir)
    print(f"CSV reports generated in {resultados_dir} category directories")
