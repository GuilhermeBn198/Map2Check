import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import yaml
import time
import glob

def criar_pasta_destino(base_dir, categoria, subcategoria):
    subcategoria_dir = os.path.join(base_dir, categoria, subcategoria)
    os.makedirs(subcategoria_dir, exist_ok=True)
    print("[INFO] Pasta de destino criada: {}".format(subcategoria_dir))
    return subcategoria_dir

def ler_includesfile(includesfile_path):
    print("[INFO] Lendo arquivo includesfile: {}".format(includesfile_path))
    subcategorias = []
    with open(includesfile_path, "r") as includesfile:
        for linha in includesfile:
            linha = linha.strip()
            if linha and not linha.startswith("#"):
                subcategorias.append(linha)
    print("[INFO] Subcategorias encontradas: {}".format(subcategorias))
    return subcategorias

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

def processar_subcategoria(subcategoria_path, destino, categoria, subcategoria_nome):
    subcategoria_full_path = os.path.join("sv-benchmarks/c/", subcategoria_path)
    print("[INFO] Processando subcategoria: {} em {}".format(subcategoria_nome, subcategoria_full_path))
    arquivos_yml = glob.glob(subcategoria_full_path)
    
    if not arquivos_yml:
        print("[ERRO] Nenhum arquivo .yml encontrado em {}".format(subcategoria_full_path))
        return

    tempos_file = os.path.join(destino, "tempos.txt")
    processed_files = set()
    if os.path.exists(tempos_file):
        with open(tempos_file, "r") as f:
            for line in f:
                filename = line.split(":")[0].strip()
                processed_files.add(filename)
        print("[INFO] Encontrados {} arquivos ja processados".format(len(processed_files)))

    for yml_file in arquivos_yml:
        input_files = extrair_input_files(yml_file, subcategoria_nome)
        for input_file in input_files:
            input_filename = os.path.basename(input_file)
            
            if input_filename in processed_files:
                print("[INFO] Pulando arquivo ja processado: {}".format(input_filename))
                continue
                
            comando = ["python3", "map2check-wrapper.py", "-p", "coverage-error-call.prp", input_file]
            print("[INFO] Executando ferramenta para: {}".format(input_file))
            cwd_release = os.path.join(os.getcwd(), "release")
            
            try:
                tempo_execucao, test_suite_path, resultado = executar_ferramenta(
                    comando, input_file, destino, cwd=cwd_release
                )
            except Exception as e:
                print("[ERRO CRITICO] Falha na execução: {}".format(e))
                tempo_execucao = 360.0
                test_suite_path = None
                resultado = "UNKNOWN"

            if test_suite_path:
                program_name = os.path.splitext(input_filename)[0]
                program_dir = os.path.join(destino, program_name)
                os.makedirs(program_dir, exist_ok=True)
                try:
                    shutil.move(
                        test_suite_path, 
                        os.path.join(program_dir, "test-suite.zip")
                    )
                    print("[SUCESSO] test-suite.zip movido para {}".format(program_dir))
                except Exception as e:
                    print("[ERRO] Falha ao mover test-suite.zip: {}".format(e))
            
            tempo_formatado = "{:.3f}".format(tempo_execucao) if tempo_execucao else "N/A"
            linha = "{}: {} segundos, Resultado: {}".format(input_filename, tempo_formatado, resultado)
            
            with open(tempos_file, "a") as f:
                f.write(linha + "\n")
            
            print("[INFO] Resultado registrado em {}".format(tempos_file))
            print("\n" + "-"*50 + "\n")

def processar_tarefas(map2check_file, resultados_dir):
    print("[INFO] Processando tarefas de {}".format(map2check_file))
    tree = ET.parse(map2check_file)
    root = tree.getroot()
    
    for tasks in root.findall("tasks"):
        categoria = tasks.get("name")
        includesfile = tasks.find("includesfile")
        
        if includesfile is None or not os.path.exists(includesfile.text):
            print("[ERRO] Includesfile nao encontrado para {}".format(categoria))
            continue
            
        subcategorias = ler_includesfile(includesfile.text)
        
        for subcategoria_path in subcategorias:
            subcategoria_nome = os.path.dirname(subcategoria_path).split("/")[-1]
            destino = criar_pasta_destino(resultados_dir, categoria, subcategoria_nome)
            processar_subcategoria(subcategoria_path, destino, categoria, subcategoria_nome)

def executar_ferramenta(comando, arquivo, output_dir, cwd=None):
    inicio = time.time()
    print("[DEBUG] Executando: {}".format(" ".join(comando)))
    
    try:
        result = subprocess.run(
            comando, 
            cwd=cwd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=360
        )
        
        output = result.stdout.strip() or "Sem saida"
        generated_file = os.path.join(cwd, "test-suite.zip") if cwd else "test-suite.zip"
        
        if os.path.exists(generated_file):
            return (time.time() - inicio), generated_file, output
        return (time.time() - inicio), None, output

    except subprocess.TimeoutExpired as e:
        # Format the specific timeout message
        timeout_output = (
            "Verifying with MAP2CHECK\n"
            "Command: timeout 360s ./map2check --timeout 356 --smt-solver yices2 "
            "--add-invariants --target-function --generate-witness {}\n"
            "UNKNOWN"
        ).format(arquivo)
        
        print("[TIMEOUT] Processo excedeu 360 segundos: {}".format(arquivo))
        return 360.0, None, timeout_output
        
    except Exception as e:
        error_msg = "Erro de execução: {}".format(str(e))
        print("[ERRO CRITICO] {}".format(error_msg))
        return (time.time() - inicio), None, error_msg

if __name__ == "__main__":
    map2check_file = "map2check.xml"
    resultados_dir = "resultados_de_testes"
    os.makedirs(resultados_dir, exist_ok=True)
    
    print("[INICIO] Processamento iniciado, resultados em {}".format(os.path.abspath(resultados_dir)))
    processar_tarefas(map2check_file, resultados_dir)
    print("[CONCLUSAO] Processamento completo")