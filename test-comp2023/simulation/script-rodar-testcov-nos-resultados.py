import os
import subprocess
import xml.etree.ElementTree as ET
import yaml
import time
import glob

HOST_SIMULATION_DIR = "/mnt/c/Users/bguil/Documents/GitHub/Map2Check/test-comp2023/simulation"
CONTAINER_BASE = "/simulation"
TESTCOV_BIN = f"{CONTAINER_BASE}/testcov/bin/testcov"

def setup_docker_container():
    max_wait_time = 300
    start_time = time.time()
    
    inspect_result = subprocess.run(
        ["docker", "inspect", "testcov_container"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    if inspect_result.returncode != 0:
        docker_cmd = [
            "sudo", "docker", "run", "--name", "testcov_container", "-d", "-it",
            "-v", f"{HOST_SIMULATION_DIR}:{CONTAINER_BASE}",
            "registry.gitlab.com/sosy-lab/benchmarking/competition-scripts/user:latest",
            "bash", "-c",
            "apt update && apt install -y software-properties-common python3-venv python3-pip && "
            "add-apt-repository -y ppa:sosy-lab/benchmarking && "
            "apt update && apt install -y benchexec && "
            "python3 -m venv --system-site-packages /testcov_env && "
            "source /testcov_env/bin/activate && "
            "pip install tsbuilder lxml numpy pycparser matplotlib && "
            "exec bash"
        ]
        subprocess.run(docker_cmd, check=True)
        print("[INFO] Docker container created")

    while time.time() - start_time < max_wait_time:
        check_result = subprocess.run(
            ["docker", "exec", "testcov_container", "test", "-f", "/testcov_env/bin/python"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if check_result.returncode == 0:
            print("[INFO] Docker container ready")
            return
        print("[INFO] Waiting for container setup...")
        time.sleep(5)
    
    raise RuntimeError("Docker container setup timed out after 300 seconds")

def host_to_container_path(host_path):
    """Convert host path to container path using the simulation mount point"""
    abs_host_path = os.path.abspath(host_path)
    return abs_host_path.replace(HOST_SIMULATION_DIR, CONTAINER_BASE)

def run_testcov(input_file_host, program_dir_host):
    try:
        # Converte os caminhos do host para os caminhos do container
        test_suite_container = host_to_container_path(
            os.path.join(program_dir_host, "test-suite.zip")
        )
        source_file_container = host_to_container_path(input_file_host)

        docker_cmd = [
            "docker", "exec", "testcov_container",
            "/testcov_env/bin/python", TESTCOV_BIN,
            "--no-isolation",
            "--test-suite", test_suite_container,
            source_file_container
        ]

        try:
            result_output = subprocess.check_output(
                docker_cmd,
                stderr=subprocess.STDOUT,
                timeout=300
            ).decode('utf-8')
            
            print("[DEBUG] Testcov output:\n{}".format(result_output))
            metrics = {
                "Tests run": "N/A",
                "Tests in suite": "N/A",
                "Coverage": "N/A",
                "Number of goals": "N/A",
                "Result": "N/A"
            }
            
            for line in result_output.splitlines():
                line = line.strip()
                for metric in metrics:
                    if line.startswith(metric):
                        metrics[metric] = line.split(":")[1].strip()
                        break
            
            summary = "TESTCOV: {Tests run} runs/{Tests in suite} suite/{Coverage} coverage/{Number of goals} goals | Result: {Result}".format(**metrics)
            
            output_file = os.path.join(program_dir_host, "testcov_output.txt")
            with open(output_file, "w", encoding='utf-8') as f:
                f.write(result_output)
            
            return summary, None
            
        except subprocess.CalledProcessError as e:
            error_output = e.output.decode('utf-8', errors='replace')
            print("[ERRO] Testcov execution error: {}".format(error_output))
            return "Error: {}".format(error_output), None
            
        except subprocess.TimeoutExpired:
            print("[ERRO] Testcov timeout")
            return "Timeout after 300 seconds", None

    except Exception as e:
        print("[ERRO CRITICO] Unexpected error: {}".format(str(e)))
        return "Critical error: {}".format(str(e)), None

def criar_pasta_destino(base_dir, categoria, subcategoria):
    subcategoria_dir = os.path.join(base_dir, categoria, subcategoria)
    os.makedirs(subcategoria_dir, exist_ok=True)
    print(f"[INFO] Destination folder created: {subcategoria_dir}")
    return subcategoria_dir

def ler_includesfile(includesfile_path):
    print(f"[INFO] Reading includesfile: {includesfile_path}")
    subcategorias = []
    with open(includesfile_path, "r") as includesfile:
        for linha in includesfile:
            linha = linha.strip()
            if linha and not linha.startswith("#"):
                subcategorias.append(linha)
    print(f"[INFO] Found subcategories: {subcategorias}")
    return subcategorias

def extrair_input_files(yml_path, subcategoria):
    input_files = []
    print(f"[INFO] Processing YAML file: {yml_path}")
    try:
        with open(yml_path, "r") as file:
            data = yaml.safe_load(file)
            if "input_files" in data:
                raw_input = data["input_files"].strip("'")
                input_file_path = os.path.join(
                    os.path.dirname(yml_path),
                    raw_input
                )
                if os.path.exists(input_file_path):
                    input_files.append(input_file_path)
                else:
                    print(f"[WARNING] Input file not found: {input_file_path}")
    except Exception as e:
        print(f"[ERROR] Error processing {yml_path}: {e}")
    return input_files

def processar_subcategoria(subcategoria_path, destino, categoria, subcategoria_nome):
    subcategoria_full_path = os.path.join(
        os.path.abspath(os.path.join(HOST_SIMULATION_DIR, "sv-benchmarks/c")),
        subcategoria_path
    )
    
    print(f"[INFO] Processing subcategory: {subcategoria_nome}")
    
    tempos_file = os.path.join(destino, "tempos.txt")
    processed_files = set()
    
    # Lê os arquivos já processados (aqueles que já possuem linha TESTCOV:)
    if os.path.exists(tempos_file):
        with open(tempos_file, "r") as f:
            lines = f.readlines()
            # Considera que cada programa ocupa uma ou duas linhas:
            # A primeira é o resultado do Map2check e, se testcov já foi executado, a segunda começa com "TESTCOV:"
            i = 0
            while i < len(lines):
                line = lines[i]
                if line.strip() and ":" in line:
                    filename = line.split(":")[0].strip()
                    processed_files.add(filename)
                    # Se a próxima linha já for de testcov, pula ela também.
                    if i + 1 < len(lines) and lines[i+1].startswith("TESTCOV:"):
                        i += 1
                i += 1
        print(f"[INFO] Found {len(processed_files)} processed files in tempos.txt")

    for yml_file in glob.glob(subcategoria_full_path):
        input_files = extrair_input_files(yml_file, subcategoria_nome)
        for input_file in input_files:
            input_filename = os.path.basename(input_file)
            program_name = os.path.splitext(input_filename)[0]
            program_dir = os.path.join(destino, program_name)
            test_suite_path = os.path.join(program_dir, "test-suite.zip")
            
            # Pula se não existir test-suite.zip
            if not os.path.exists(test_suite_path):
                print(f"[SKIP] No test-suite.zip for {input_filename}")
                continue
                
            # Pula se já foi processado (já existe resultado do Map2check)
            if input_filename not in processed_files:
                print(f"[SKIP] Skipping {input_filename} because Map2check result not found in tempos.txt")
                continue

            print(f"\n[PROCESSING] {input_filename}")
            print(f"  Test suite path: {test_suite_path}")
            print(f"  Program dir: {program_dir}")
            
            # Executa o testcov e obtém o resumo dos resultados
            testcov_summary, _ = run_testcov(input_file, program_dir)
            
            # Atualiza o arquivo tempos.txt:
            # Procura a linha que começa com o nome do arquivo (resultado do Map2check) e insere
            # ou substitui a linha TESTCOV logo em seguida.
            if os.path.exists(tempos_file):
                with open(tempos_file, "r+") as f:
                    lines = f.readlines()
                    new_lines = []
                    i = 0
                    while i < len(lines):
                        line = lines[i]
                        new_lines.append(line)
                        if line.startswith(input_filename + ":"):
                            # Verifica se a próxima linha já é do testcov
                            if i + 1 < len(lines) and lines[i+1].startswith("TESTCOV:"):
                                new_lines.append(f"TESTCOV: {testcov_summary}\n")
                                i += 1  # pula a linha antiga
                            else:
                                new_lines.append(f"TESTCOV: {testcov_summary}\n")
                        i += 1
                    f.seek(0)
                    f.truncate()
                    f.writelines(new_lines)
            else:
                # Se tempos.txt não existir, cria-o (embora o Map2check já deva tê-lo criado)
                with open(tempos_file, "w") as f:
                    f.write(f"{input_filename}: \n")
                    f.write(f"TESTCOV: {testcov_summary}\n")
                    
            print(f"[SUCCESS] Updated {input_filename} with TESTCOV results")

def processar_tarefas(map2check_file, resultados_dir):
    print(f"[INFO] Processing tasks from {map2check_file}")
    tree = ET.parse(map2check_file)
    root = tree.getroot()
    
    for tasks in root.findall("tasks"):
        categoria = tasks.get("name")
        includesfile = tasks.find("includesfile")
        
        if includesfile is None or not os.path.exists(includesfile.text):
            print(f"[ERROR] Missing includesfile for {categoria}")
            continue
            
        subcategorias = ler_includesfile(includesfile.text)
        
        for subcategoria_path in subcategorias:
            subcategoria_nome = os.path.dirname(subcategoria_path).split("/")[-1]
            destino = criar_pasta_destino(resultados_dir, categoria, subcategoria_nome)
            processar_subcategoria(subcategoria_path, destino, categoria, subcategoria_nome)

if __name__ == "__main__":
    try:
        setup_docker_container()
        map2check_file = os.path.join(HOST_SIMULATION_DIR, "map2check.xml")
        resultados_dir = os.path.join(HOST_SIMULATION_DIR, "resultados_de_testes")
        os.makedirs(resultados_dir, exist_ok=True)
        
        print(f"[START] Processing results in {resultados_dir}")
        processar_tarefas(map2check_file, resultados_dir)
        print("[COMPLETE] Testcov processing finished")
    except Exception as e:
        print(f"[FATAL ERROR] Script failed: {str(e)}")
        exit(1)
