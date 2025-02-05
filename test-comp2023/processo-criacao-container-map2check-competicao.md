# Processo de criação de container para rodar map2check em ambiente de competição simulada

1. Criar Imagem de instalação do Map2check e Testcov

```bash
  git clone https://github.com/hbgit/Map2Check.git
  cd Map2Check
  git submodule update --init --recursive
  docker build -t hrocha/mapdevel --no-cache -f Dockerfile .
  docker pull registry.gitlab.com/sosy-lab/benchmarking/competition-scripts/user:latest
```

2. Executar container do testcov com as informações precisas:

```bash
  docker run --name testcov_container -it   -v /mnt/c/Users/bguil/Documents/GitHub/Map2Check/test-comp2023/simulation:/release   registry.gitlab.com/sosy-lab/benchmarking/competition-scripts/user:latest   bash -c "apt update && apt install -y software-properties-common python3-venv python3-pip && \
           add-apt-repository -y ppa:sosy-lab/benchmarking && \
           apt update && apt install -y benchexec && \
           python3 -m venv --system-site-packages /testcov_env && \
           source /testcov_env/bin/activate && \
           pip install tsbuilder lxml numpy pycparser matplotlib && \
           exec bash"
```

3. Criar Container da aplicação, instalar ferramenta e entrar dentro do container

```bash
  docker run -it -v $(pwd):/home/map2check/devel_tool/mygitclone:Z --user $(id -u):$(id -g) \
  hrocha/mapdevel /bin/bash -c "cd /home/map2check/devel_tool/mygitclone; ./make-release.sh; \ 
  ./make-unit-test.sh; exec /bin/bash"
```

4. Instalar pyaml 5.3.1 e se direcionar para o diretório correto

```bash
  python3 -m pip install 'pyyaml==5.3.1'
  cd test-comp2023/simulation
```

5. executar o script de simulação do ambiente da competição

```bash
  python3 script_execucao.py
```
