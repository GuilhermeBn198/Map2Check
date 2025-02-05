import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import yaml  # type: ignore
import time
import glob

# Funcao para criar pastas para organizar os resultados
def criar_pasta_destino(base_dir, categoria, subcategoria):
    subcategoria_dir = os.path.join(base_dir, categoria, subcategoria)
    os.makedirs(subcategoria_dir, exist_ok=True)
    print("[INFO] Pasta de destino criada: {}".format(subcategoria_dir))
    return subcategoria_dir

# Funcao para ler as subcategorias a partir do arquivo includesfile
def ler_includesfile(includesfile_path):
    print("[INFO] Lendo arquivo includesfile: {}".format(includesfile_path))
    subcategorias = []
    with open(includesfile_path, "r") as includesfile:
        for linha in includesfile:
            linha = linha.strip()
            if linha and not linha.startswith("#"):  # Ignorar comentarios e linhas vazias
                subcategorias.append(linha)
    print("[INFO] Subcategorias encontradas: {}".format(subcategorias))
    return subcategorias

# Funcao para extrair os arquivos de entrada (input_files) de arquivos .yml
def extrair_input_files(yml_path, subcategoria):
    input_files = []
    print("[INFO] Processando arquivo .yml: {}".format(yml_path))
    try:
        with open(yml_path, "r") as file:
            data = yaml.safe_load(file)
            if "input_files" in data:
                raw_input = data["input_files"].strip("'")
                input_file_path = "../sv-benchmarks/c/{}/{}".format(subcategoria, raw_input)
                input_files.append(input_file_path)
                print("[INFO] Input file encontrado: {}".format(input_file_path))
    except Exception as e:
        print("[ERRO] Erro ao processar {}: {}".format(yml_path, e))
    return input_files

# Funcao para processar os arquivos dentro de uma subcategoria
def processar_subcategoria(subcategoria_path, destino, categoria, subcategoria_nome):
    subcategoria_path = os.path.join("sv-benchmarks/c/", subcategoria_path)
    print("[INFO] Processando subcategoria: {} em {}".format(subcategoria_nome, subcategoria_path))

    # Coletar arquivos YML
    arquivos_yml = glob.glob(subcategoria_path)
    tempos = []

    if not arquivos_yml:
        print("[ERRO] Nenhum arquivo .yml encontrado em {}".format(subcategoria_path))
        return

    for yml_file in arquivos_yml:
        input_files = extrair_input_files(yml_file, subcategoria_nome)
        for input_file in input_files:
            comando = ["python3", "map2check-wrapper.py", "-p", "coverage-error-call.prp", input_file]
            print("[INFO] Executando ferramenta para o arquivo: {}".format(input_file))
            cwd_release = os.path.join(os.getcwd(), "release")
            print("[DEBUG] cwd_release definido como: {}".format(cwd_release))
            # A funcao retorna: tempo de execucao, (opcional) caminho do test-suite e o resultado da ferramenta
            tempo_execucao, test_suite_path, resultado = executar_ferramenta(comando, input_file, destino, cwd=cwd_release)
            time.sleep(1)  # Delay para visualizacao clara no terminal

            if test_suite_path:
                print("[INFO] Test-suite.zip gerado: {}".format(test_suite_path))
                # Chama o testcov (dentro do container) e extrai os parametros relevantes
                resultado_testcov, output_file = executar_testcov(test_suite_path, input_file, destino)
                tempos.append((os.path.basename(input_file), tempo_execucao, resultado_testcov, output_file))
                print("[DEBUG] Resultado do testcov: {}".format(resultado_testcov))
                time.sleep(1)
            else:
                print("[INFO] Resultado da ferramenta: {}".format(resultado))
                tempos.append((os.path.basename(input_file), tempo_execucao, resultado, None))
                print("")

    tempos_file = os.path.join(destino, "tempos.txt")
    with open(tempos_file, "w") as f:
        for arquivo, tempo, resultado, output_file in tempos:
            # Reduzir a precisao do tempo para 3 casas decimais
            tempo_formatado = "{:.3f}".format(tempo) if tempo is not None else "N/A"
            linha = "{}: {} segundos, Resultado: {}".format(arquivo, tempo_formatado, resultado)
            if output_file:
                linha += ", Saida: {}".format(output_file)
            f.write(linha + "\n")
    print("[INFO] Arquivo tempos.txt gerado: {}".format(tempos_file))
    print("\n" * 5)

# Funcao principal para processar categorias e subcategorias
def processar_tarefas(map2check_file, resultados_dir):
    print("[INFO] Processando tarefas a partir de {}".format(map2check_file))
    tree = ET.parse(map2check_file)
    root = tree.getroot()

    for tasks in root.findall("tasks"):
        categoria = tasks.get("name")
        includesfile_path = tasks.find("includesfile").text
        print("[INFO] Processando categoria: {}".format(categoria))

        if includesfile_path and os.path.exists(includesfile_path):
            subcategorias = ler_includesfile(includesfile_path)
            for subcategoria_path in subcategorias:
                subcategoria_nome = os.path.dirname(subcategoria_path).split("/")[-1]  # Nome correto
                destino = criar_pasta_destino(resultados_dir, categoria, subcategoria_nome)
                processar_subcategoria(subcategoria_path, destino, categoria, subcategoria_nome)
                time.sleep(1)
                print("\n" * 2)    
        else:
            print("[ERRO] Arquivo includesfile nao encontrado: {}".format(includesfile_path))

# --- Funcao executada para a ferramenta Map2Check ---
def executar_ferramenta(comando, arquivo, output_dir, cwd=None):
    inicio = time.time()
    print("[DEBUG] Comando executado: {}".format(" ".join(comando)))
    try:
        result_output = subprocess.check_output(comando, cwd=cwd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("[ERRO] Erro ao executar a ferramenta para {}: {}".format(arquivo, e))
        fim = time.time()
        tempo_execucao = fim - inicio
        return tempo_execucao, None, "Erro"
    fim = time.time()
    tempo_execucao = fim - inicio

    generated_file = os.path.join(cwd if cwd is not None else os.getcwd(), "test-suite.zip")
    print("[DEBUG] Verificando existencia do arquivo: {}".format(generated_file))
    if os.path.exists(generated_file):
        print("[DEBUG] Arquivo test-suite.zip encontrado.")
        # Retorna o caminho do test-suite gerado sem move-lo
        return tempo_execucao, generated_file, "Test-Suite"
    else:
        resultado_str = result_output.decode("utf-8").strip()
        print("[DEBUG] Resultado da execucao: {}".format(resultado_str))
        return tempo_execucao, None, resultado_str

# --- Funcao para executar o testcov dentro do container externo ---
def executar_testcov(test_suite_path, arquivo_original, output_dir):
    """
    Executa o testcov no container usando Docker e extrai os parametros relevantes.
    Suposições:
      - O script e executado a partir da pasta raiz:
          /mnt/c/Users/bguil/Documents/GitHub/Map2Check/test-comp2023/simulation/
      - Essa pasta contem as pastas: release/, testcov/, resultados_de_testes/, etc.
      - O container sera montado com a raiz (simulation) em /simulation.
      - O comando sera executado a partir do diretorio /simulation/testcov.
      - Os parametros (test-suite e o arquivo original) serao fornecidos como caminhos relativos a /simulation/testcov.
    """
    # A raiz do projeto (simulation) e o diretorio corrente
    volume_host = "/mnt/c/Users/bguil/Documents/GitHub/Map2Check/test-comp2023/simulation"
    volume_container = "/simulation"
    workdir_container = os.path.join(volume_container, "testcov")
    
    print("[DEBUG] volume_host (host root): {}".format(volume_host))
    print("[DEBUG] volume_container (container root): {}".format(volume_container))
    print("[DEBUG] workdir_container (diretorio de trabalho no container): {}".format(workdir_container))
    
    # Calcula os caminhos relativos a partir do diretorio testcov no host
    base_for_rel = os.path.join(volume_host, "testcov")
    print("[DEBUG] Base para calculo de caminhos relativos: {}".format(base_for_rel))
    rel_test_suite = "../release/test-suite.zip"
    rel_input = os.path.relpath(arquivo_original, base_for_rel)
    
    print("[DEBUG] Caminho relativo do test-suite: {}".format(rel_test_suite))
    print("[DEBUG] Caminho relativo do arquivo original: {}".format(rel_input))
    
    docker_cmd = [
        "sudo", "docker", "run", "--rm", "-i", "-t",
        "-v", "{}:{}".format(volume_host, volume_container),
        "-w", workdir_container,
        "registry.gitlab.com/sosy-lab/benchmarking/competition-scripts/user:latest",
        "bash", "-c",
        "./bin/testcov --no-isolation --test-suite '{}' '{}'".format(rel_test_suite, rel_input)
    ]
    
    print("[DEBUG] Comando Docker para testcov: {}".format(" ".join(docker_cmd)))
    
    try:
        result_output = subprocess.check_output(docker_cmd, stderr=subprocess.STDOUT)
        result_text = result_output.decode("utf-8")
        print("[DEBUG] Saida do testcov:\n{}".format(result_text))
        # Exemplo de saida:
        # ⏳ Executing tests 2/2
        # ✔️  Done!
        #
        # ---Results---
        # Tests run: 2
        # Tests in suite: 2
        # Coverage: 100.0%
        # Number of goals: 2
        # Result: DONE

        tests_run = tests_in_suite = coverage = number_of_goals = result_status = None
        for line in result_text.splitlines():
            line = line.strip()
            if line.startswith("Tests run:"):
                tests_run = line.split("Tests run:")[1].strip()
            elif line.startswith("Tests in suite:"):
                tests_in_suite = line.split("Tests in suite:")[1].strip()
            elif line.startswith("Coverage:"):
                coverage = line.split("Coverage:")[1].strip()
            elif line.startswith("Number of goals:"):
                number_of_goals = line.split("Number of goals:")[1].strip()
            elif line.startswith("Result:"):
                result_status = line.split("Result:")[1].strip()
        summary = "Tests run: {}, Tests in suite: {}, Coverage: {}, Number of goals: {}, Result: {}".format(
            tests_run, tests_in_suite, coverage, number_of_goals, result_status
        )
        # Grava a saida completa em um arquivo dentro do diretorio de resultados
        output_file = os.path.join(output_dir, "testcov_output.txt")
        with open(output_file, "w") as f:
            f.write(result_text)
        print("[DEBUG] Testcov executado com sucesso. Resumo: {}".format(summary))
        return summary, output_file
    except subprocess.CalledProcessError as e:
        print("[ERRO] Erro ao executar testcov para {}: {}".format(test_suite_path, e))
        return "Erro", None

if __name__ == "__main__":
    map2check_file = "map2check.xml"
    resultados_dir = "resultados_de_testes"
    os.makedirs(resultados_dir, exist_ok=True)
    caminho_completo = os.path.abspath(resultados_dir)
    print("Pasta criada/em uso: {}".format(caminho_completo))
    input("aguardando confirmacao visual do operador(press enter)...")
    
    processar_tarefas(map2check_file, resultados_dir)
