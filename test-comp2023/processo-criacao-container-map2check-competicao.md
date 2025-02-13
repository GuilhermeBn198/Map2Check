# Processo de criação de container para rodar map2check em ambiente de competição simulada

1. Criar Imagem de instalação do Map2check e Testcov

```bash
  git clone https://github.com/hbgit/Map2Check.git
  cd Map2Check
  git submodule update --init --recursive
  docker build -t hrocha/mapdevel --no-cache -f Dockerfile .
  docker pull registry.gitlab.com/sosy-lab/benchmarking/competition-scripts/user:latest
```

2. Criar Container da aplicação, instalar ferramenta e entrar dentro do container

```bash
  docker run -it \
  -v $(pwd):/home/map2check/devel_tool/mygitclone:Z \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --user $(id -u):$(id -g) \
  hrocha/mapdevel \
  /bin/bash -c "cd /home/map2check/devel_tool/mygitclone; ./make-release.sh; ./make-unit-test.sh; exec /bin/bash"
```

3. Instalar Docker dentro do container para poder executar o script corretamente

```bash
wget -qO- https://download.docker.com/linux/static/stable/x86_64/docker-20.10.8.tgz | tar xzvf - && sudo cp docker/docker /usr/local/bin/ && sudo chmod +x /usr/local/bin/docker && rm -rf docker/ && docker --version
```

4. Instalar pyaml 5.3.1 e se direcionar para o diretório correto

```bash
  python3 -m pip install 'pyyaml==5.3.1' && cd test-comp2023/simulation
```

5. executar o script de simulação do ambiente da competição

```bash
  nohup sudo python3 script_execucao.py
```
