# Testing Workflow Progress Report

## ESBMC

### Observações

- SÓ É GERADO TESTCASE PARA PROGRAMAS COM FALHAS! EX: bitvector/sum02-1.i possui property_file: ../properties/unreach-call.prp expected_verdict: false

### Test Cases for ESBMC

- **python3 esbmc-wrapper.py -p ../properties/coverage-error-call.prp ../sv-benchmarks/c/bitvector/byte_add-1.i**
  - RESULT: FAILED
  - generated test-suite: YES
  - properties:
    - property_file: ../properties/no-overflow.prp
      expected_verdict: true
    - property_file: ../properties/termination.prp
      expected_verdict: true
    - property_file: ../properties/unreach-call.prp
      expected_verdict: false
    - property_file: ../properties/coverage-error-call.prp
    - property_file: ../properties/coverage-branches.prp
    - property_file: ../properties/coverage-conditions.prp
    - property_file: ../properties/coverage-statements.prp
- **python3 esbmc-wrapper.py -p ../properties/coverage-error-call.prp ../sv-benchmarks/c/bitvector-loops/diamond_2-1.c**
  - RESULT: FAILED
  - generated test-suite: YES
  - properties:
    - property_file: ../properties/unreach-call.prp
      expected_verdict: false
    - property_file: ../properties/coverage-error-call.prp
    - property_file: ../properties/coverage-branches.prp
    - property_file: ../properties/coverage-conditions.prp
    - property_file: ../properties/coverage-statements.prp
- **python3 esbmc-wrapper.py -p ../properties/coverage-error-call.prp ../sv-benchmarks/c/bitvector-loops/verisec_sendmail_tTflag_arr_one_loop.c**
  - RESULT: FAILED
  - generated test-suite: YES
  - properties:
    - property_file: ../properties/termination.prp
      expected_verdict: true
    - property_file: ../properties/unreach-call.prp
      expected_verdict: false
    - property_file: ../properties/coverage-error-call.prp
    - property_file: ../properties/coverage-branches.prp
    - property_file: ../properties/coverage-conditions.prp
    - property_file: ../properties/coverage-statements.prp
- **python3 esbmc-wrapper.py -p ../properties/coverage-error-call.prp ../sv-benchmarks/c/bitvector-regression/implicitfloatconversion.c**
  - RESULT: FAILED
  - generated test-suite: YES
  - properties:
    - property_file: ../properties/termination.prp
      expected_verdict: true
    - property_file: ../properties/unreach-call.prp
      expected_verdict: false
- **python3 esbmc-wrapper.py -p ../properties/coverage-error-call.prp ../sv-benchmarks/c/bitvector-regression/signextension2-2.C**
  - RESULT: FAILED
  - generated test-suite: YES
  - properties:
    - property_file: ../properties/termination.prp
      expected_verdict: true
    - property_file: ../properties/unreach-call.prp
      expected_verdict: false
- **python3 esbmc-wrapper.py -p ../properties/coverage-error-call.prp ../sv-benchmarks/c/loop-acceleration/simple_1-1_abstracted.c**
  - RESULT: FAILED
  - generated test-suite: YES
  - properties:
    - property_file: ../properties/unreach-call.prp
      expected_verdict: false
- **python3 esbmc-wrapper.py -p ../properties/coverage-error-call.prp ../sv-benchmarks/c/loops/array-2.c**
  - RESULT: FAILED
  - generated test-suite: YES
  - properties:
    - property_file: ../properties/termination.prp
      expected_verdict: true
    - property_file: ../properties/unreach-call.prp
      expected_verdict: false
    - property_file: ../properties/coverage-error-call.prp
    - property_file: ../properties/coverage-branches.prp
    - property_file: ../properties/coverage-conditions.prp
    - property_file: ../properties/coverage-statements.prp

## Map2Check

### Obervações

- é necessária a adaptação das propriedades do map2check para condizerem com as propriedades do TESTCOMP2024
  - o pivô de detecção de function call da propriedade unreach-call.prp deve ser modificada de `__VERIFIER_error` para `reach_error`, visto que os códigos de benchmark disponíveis online contém essa nomenclatura como padrão.
  - Essencialmente, nada muda na fórmula das propriedades em comparação com o novo padrão.
  - Por causa das adaptações necessárias, foram feitas cópias dos mesmos arquivos testados com o ESBMC, além de criar uma pasta separada com todos os testes que geraram testcase no ESBMC.
- as linhas de comando ficaram grandes devido apenas à forma que estão disponíveis os arquivos devidamente configurados para a utilização da ferramenta, como a pasta properties e os testes.
- Por via de dúvida, foi executado os mesmos comandos, com as mesmas propriedades e com os mesmos arquivos para gerar uma consistência.

### Test Cases for Map2Check

- **python3 map2check-wrapper.py -p ../../../tests/regression_test/test_cases/sv-benchmarks/properties/unreach-call.prp ../sv-benchmarks/selected/array-2_map2check.c**
  - RESULT: FAILED
  - gerou witness: sim
  - false
- **python3 map2check-wrapper.py -p ../../../tests/regression_test/test_cases/sv-benchmarks/properties/unreach-call.prp ../sv-benchmarks/selected/byte_add-1_map2check.i**
  - RESULT: FAILED
  - gerou witness: não
  - unknown
- **python3 map2check-wrapper.py -p ../../../tests/regression_test/test_cases/sv-benchmarks/properties/unreach-call.prp ../sv-benchmarks/selected/diamond_2-1_map2check.c**
  - RESULT: FAILED
  - gerou witness: sim
  - false
- **python3 map2check-wrapper.py -p ../../../tests/regression_test/test_cases/sv-benchmarks/properties/unreach-call.prp ../sv-benchmarks/selected/implicitfloatconversion_map2check.c**
  - RESULT: FAILED
  - gerou witness: sim
  - false
- **python3 map2check-wrapper.py -p ../../../tests/regression_test/test_cases/sv-benchmarks/properties/unreach-call.prp ../sv-benchmarks/selected/signextension2-2_map2check.c**
  - RESULT: FAILED
  - gerou witness: sim
  - false
- **python3 map2check-wrapper.py -p ../../../tests/regression_test/test_cases/sv-benchmarks/properties/unreach-call.prp ../sv-benchmarks/selected/simple_1-1_abstracted_map2check.c**
  - RESULT: FAILED
  - gerou witness: sim
  - false
- **python3 map2check-wrapper.py -p ../../../tests/regression_test/test_cases/sv-benchmarks/properties/unreach-call.prp ../sv-benchmarks/selected/verisec_sendmail_tTflag_arr_one_loop_map2check.c**
  - RESULT: FAILED
  - gerou witness: sim
  - false
