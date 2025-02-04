import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import yaml # type: ignore
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
            if linha and not linha.startswith("#"):  # Ignorar comentários e linhas vazias
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
    print("[INFO] Processando subcategoria: {} em {}".format(subcategoria_nome,subcategoria_path))

    # Debug do caminho
    print("[DEBUG] Caminho final para glob: {}".format(subcategoria_path))

    # Coletar arquivos YML
    arquivos_yml = glob.glob(subcategoria_path)
    # print("[DEBUG] Arquivos encontrados: {}".format(arquivos_yml))
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
            tempo_execucao, test_suite_path = executar_ferramenta(comando, input_file, destino, cwd=cwd_release)
            time.sleep(1)  # Delay para visualizacao clara no terminal

            if tempo_execucao is not None and test_suite_path:
                print("[INFO] Test-suite.zip gerado: {}".format(test_suite_path))
                resultado_testcov, output_file = executar_testcov(test_suite_path, input_file, destino)
                tempos.append((os.path.basename(input_file), tempo_execucao, resultado_testcov, output_file))
                print("")
                time.sleep(1)
            else:
                print("[ERRO] Falha ao gerar test-suite.zip para {}".format(input_file))
                tempos.append((os.path.basename(input_file), tempo_execucao, "Erro", None))
                print("")

    tempos_file = os.path.join(destino, "tempos.txt")
    with open(tempos_file, "w") as f:
        for arquivo, tempo, resultado, output_file in tempos:
            # Reduzir a precisao do tempo para 3 casas decimais
            tempo_formatado = "{:.3f}".format(tempo) if tempo is not None else "N/A"
            linha = "{}: {} segundos, TestCov: {}".format(arquivo, tempo_formatado, resultado)
            if output_file:
                linha += ", Saída: {}".format(output_file)
            f.write(linha + "\n")
    print("[INFO] Arquivo tempos.txt gerado: {}".format(tempos_file))
    print("")
    print("")
    print("")
    print("")
    print("")


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
                print("")
                print("")    
        else:
            print("[ERRO] Arquivo includesfile nao encontrado: {}".format(includesfile_path))

# Funcao para executar a ferramenta principal e medir o tempo de execucao
def executar_ferramenta(comando, arquivo, output_dir, cwd=None):
    try:
        inicio = time.time()
        subprocess.run(comando, check=True, cwd=cwd)
        fim = time.time()

        tempo_execucao = fim - inicio
        generated_file = os.path.join(cwd if cwd is not None else os.getcwd(), "test-suite.zip")
        if os.path.exists(generated_file):
            destino_arquivo = os.path.join(output_dir, "test-suite.zip")
            shutil.move(generated_file, destino_arquivo)
            return tempo_execucao, destino_arquivo
        else:
            return tempo_execucao, None
    except subprocess.CalledProcessError as e:
        print("[ERRO] Erro ao executar a ferramenta para {}: {}".format(arquivo, e))
        return None, None

# Funcao para analisar o arquivo test-suite.zip usando o testcov
def executar_testcov(test_suite_path, arquivo_original, output_dir):
    try:
        comando = [
            "./testcov/bin/testcov",
            "--no-isolation",
            "--test-suite", test_suite_path,
            arquivo_original
        ]
        output_file = os.path.join(output_dir, "testcov_output.txt")
        with open(output_file, "w") as output:
            subprocess.run(comando, check=True, stdout=output, stderr=output)
        return "Sucesso", output_file
    except subprocess.CalledProcessError as e:
        print("[ERRO] Erro ao executar testcov para {}: {}".format(test_suite_path,e))
        return "Erro", None

if __name__ == "__main__":
    map2check_file = "map2check.xml"
    resultados_dir = "resultados_de_testes"
    os.makedirs(resultados_dir, exist_ok=True)
    # Obter e exibir o caminho completo
    caminho_completo = os.path.abspath(resultados_dir)
    print("Pasta criada/em uso: {}".format(caminho_completo))
    input("aguardando confirmacao visual do operador(press enter)...")
    
    processar_tarefas(map2check_file, resultados_dir)
