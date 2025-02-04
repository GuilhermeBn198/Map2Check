# Processo de criação de container para rodar map2check em ambiente de competição simulada

1. Criar Imagem de instalação do dockerfile

```bash
  git clone https://github.com/hbgit/Map2Check.git
  cd Map2Check
  git submodule update --init --recursive
  docker build -t hrocha/mapdevel --no-cache -f Dockerfile .
```

1. Criar Container da aplicação, instalar ferramenta e entrar dentro do container

  ```bash
    docker run -it -v $(pwd):/home/map2check/devel_tool/mygitclone:Z --user $(id -u):$(id -g) \
  hrocha/mapdevel /bin/bash -c "cd /home/map2check/devel_tool/mygitclone; ./make-release.sh; \ 
  ./make-unit-test.sh; exec /bin/bash"
  ```

3. Instalar pyaml 5.3.1

```bash
python3 -m pip install 'pyyaml==5.3.1'
```

4. Instalar TestCov

5. executar o script de simulação do ambiente da competição

```bash
  cd test-comp2023/simulation
  python3 script-execucao.py
```
