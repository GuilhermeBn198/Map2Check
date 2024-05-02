# todo's tasks for "map2check: An approach to software testing"

## article made by: [Guilherme Lucas Pereira Bernardo](https://github.com/GuilhermeBn198) and oriented by: [Herbert Oliveira Rocha](https://github.com/hbgit/)

- semana 13/09/2023 ~~ 20/09/2023
  - [x] Fazer fork do Map2Check e criar um branch de nome test-comp
  - [x] Fazer um checklist para participar no test-comp
  - [x] Fazer um teste com ESBMC no test-comp
    - [x] baixar o esbmc-kind de [link](https://gitlab.com/sosy-lab/test-comp/archives-2023/raw/testcomp23/2023/esbmc-kind.zip)
    - [x] adicionar um .gitignore da pasta do esbmc
    - [x] testar o esbmc com inputs do test-comp

- [x] semana 27/09/2023 ~~ 04/09/2023
  - [x] Criar diagrama de fluxo (flowchart ou BPMN) do funcionamento do Map2Check
  - [x] Criar um lista de arquivos de output que devem ser gerados para o test-comp

- [x] semana 27/10/2023 ~~ 04/10/2023
  - [x] finalizar a parte de  bugfinding
  - [x] com base nos arquivos de witness gerados pelos testes no map2check, gerar os testcases do testcomp
    - [x] criar um script em python para ler o arquivo de witness e escrever os dados dele em diferentes arquivos de testcase
    - [x] criar pequenos casos de testes com erro para gerar valores
  - [x] estudar ferramenta TESTCOV, usada para testar o map2check dentro da competição
    - [x] Baixar TESTCOV para realizar testes
  - [ ] Flow de execução do TESTCOMP com base no Checklist-Map2check-testcomp.jpeg no repositório
  - [x] ESBMC
    - [x] explicar como roda no TESTCOMP
  - [x] baixar os PRP do testcomp no site da competição junto dos arquivos C do benchmark(pasta properties)

- [x] semana 14/01/2024 ~~ 21/01/2024
  - [x] Inicio de redação do Relatório Parcial do projeto
<<<<<<< Updated upstream
  - [x] Redação do embasamento teórico de artigo relacionado
=======
  - [ ] Redação do embasamento teórico de artigo relacionado
>>>>>>> Stashed changes
  - [x] Reiniciar testes com esbmc para comparar testcases gerados com os do map2check
  - [x] Aplicar os mesmos testes feitos no esbmc no map2check para ver o q é impresso no witness
  - [x] Verificar output do data_extractor se estiver de acordo com o output do esbmc
  - [x] finalizar script python para ler arquivo de witness

- [x] semana 21/01/2024 ~~ 05/02/2024
  - [x] Finalização do script de extração de dados do map2check.
  - [x] Acoplamento do script de extração de dados do map2check no wrapper da aplicação.
  - [x] Inicio dos testes com o testcov.

- [x] semana 01/03/2024 -- 15/03/2024
  - [x] Wrapper do map2check finalizado
  - [x] Prova de conceito do map2check no testcov
  - [x] Validação massificada do map2check no testcov
    - [x] pegar todos os testes
    - [x] organizar planilha com os dados
    - [x] fazer testes com o esbmc
    - [x] adaptar testes para o map2check
    - [x] fazer testes com o map2check
    - [x] validar testes com o testcov
    - [x] comparar dados na planilha

- [ ] semana 02/04/2024 ~~ 16/04/2024
  - [x] Quantificar resultados dos testes do Map2check
  - [ ] pipeline de execução
    - [x] verificar no site da competição se o map2check ja está fazendo tudo possível para estar dentro da competição
    - [ ] adicionar a execução do testcov dentro da execução do map2check_wrapper.py para produzir a validação tambem de uma vez só.
<<<<<<< Updated upstream
  - [ ] Refazer o Flow de execução do TEST-COMP mais uma vez, de forma bonitinha para poder ser apresentado em paper.
=======
  - [ ] Refazer o Flow de execução do TEST-COMP mais uma vez, de forma bonitinha para poder ser apresentado em paper
>>>>>>> Stashed changes
