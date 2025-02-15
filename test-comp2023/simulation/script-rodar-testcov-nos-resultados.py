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
        # Convert host paths to container paths
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
    
    # Read existing entries to track processed files
    if os.path.exists(tempos_file):
        with open(tempos_file, "r") as f:
            for line in f:
                if "TESTCOV:" in line:
                    filename = line.split(":")[0].strip()
                    processed_files.add(filename)

    for yml_file in glob.glob(subcategoria_full_path):
        input_files = extrair_input_files(yml_file, subcategoria_nome)
        for input_file in input_files:
            input_filename = os.path.basename(input_file)
            program_name = os.path.splitext(input_filename)[0]
            program_dir = os.path.join(destino, program_name)
            test_suite_path = os.path.join(program_dir, "test-suite.zip")
            
            # Skip if no test-suite.zip exists
            if not os.path.exists(test_suite_path):
                print(f"[SKIP] No test-suite.zip for {input_filename}")
                continue
                
            # Skip if already processed
            if input_filename in processed_files:
                print(f"[SKIP] Already processed: {input_filename}")
                continue

            print(f"\n[PROCESSING] {input_filename}")
            print(f"  Test suite path: {test_suite_path}")
            print(f"  Program dir: {program_dir}")
            
            # Run testcov and get results
            testcov_summary, _ = run_testcov(input_file, program_dir)
            
            # Append testcov results after the existing entry
            with open(tempos_file, "r+") as f:
                lines = f.readlines()
                f.seek(0)
                
                for line in lines:
                    f.write(line)
                    if line.startswith(input_filename):
                        # Append testcov results after the original entry
                        f.write(f"TESTCOV: {testcov_summary}\n\n")
            
            print(f"[SUCCESS] Updated {input_filename}")


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