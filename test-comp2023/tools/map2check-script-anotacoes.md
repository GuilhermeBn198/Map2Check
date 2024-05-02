# Anotações de modificações no map2check-wrapper.py

## **DECIDI POR NÃO FAZER UM ARGUMENTO INTEIRO SEPARADO POR MOTIVOS DE: SE AS PROPRIEDADES SÃO UNICAS PERANTE AS DUAS COMPETIÇÕES, NÃO É NECESSÁRIO TER UMA FLAG PARA IDENTICAÇÃO DAS COMPETIÇÕES VISTO QUE ELAS SÃO UNICAS.**
  
- Foi adicionado duas propriedades que são settadas True, caso a propriedade seja verificada(is_cov_call e is_cov_branches) (linhas 44 e 45)
  
- Foi adicionado dois elif contendo as propriedades necessárias para concorrer no coverage-branches e coverage-error-calls (linhas 62 e 64)
  
- Foi adicionado dois elifs que verificam as propriedades True de **is_cov_call e is_cov_branches**, com base no esbc_wrapper e nas outras propriedades disponíveis no map2check, cheguei na linha de comando da linha 89 e 93

  - Observando o comportamento da ferramenta a partir das alterações feitas, pode-se observar que agora, não evidencia erro de propriedade não suportada pela ferramenta, como ocorria antes, dito isto, acredita-se que a abordagem feita tenha obtido relativo sucesso, uma vez que, apesar de não estar detectando erro, a ferramenta ainda não é capaz de reconhecer os arquivos com a função REACH_ERROR

## O comando usado para testar a diferença entre as duas propriedades foi

- **para a versão original:**
  - python3 map2check-wrapper.py -p ../properties/unreach-call-map2check.prp ../sv-benchmarks/map2checktests/array-industry-pattern/array_range_init.i
  - python3 map2check-wrapper.py -p ../properties/coverage-error-call.prp ../sv-benchmarks/c/array-industry-pattern/array_range_init.i

- **para a versão modificada:**
  - python3 map2check-wrapper-modificado.py -p ../properties/unreach-call-map2check.prp ../sv-benchmarks/map2checktests/array-industry-pattern/array_range_init.i
  - python3 map2check-wrapper-modificado.py -p ../properties/coverage-error-call.prp ../sv-benchmarks/c/array-industry-pattern/array_range_init.i
