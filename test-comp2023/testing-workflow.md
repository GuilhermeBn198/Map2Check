# Map2Check Testing workflow Progress Report

## Test Cases

- ./map2check --target-function ../../tests/regression_test/test_cases/sv-benchmarks/array-examples/relax-1.c --verification unknown
  - RESULT: verification unknown
  - properties:
    - property_file: ../properties/valid-memsafety.prp **expected_verdict:** false **subproperty:** valid-deref

- ./map2check --target-function ../../tests/regression_test/test_cases/sv-benchmarks/array-examples/standard_sentinel-2.c
  - RESULT: verification unknown
  - properties:
    - property_file: ../properties/termination.prp **expected_verdict:** true
    - property_file: ../properties/unreach-call.prp **expected_verdict:** true
    - property_file: ../properties/coverage-branches.prp
    - property_file: ../properties/coverage-conditions.prp
    - property_file: ../properties/coverage-statements.prp

- ./map2check --target-function ../../tests/regression_test/test_cases/sv-benchmarks/array-examples/standard_two_index_04.c
  - RESULT: verification unknown
  - properties:
    - property_file: ../properties/unreach-call.prp **expected_verdict:** true
    - property_file: ../properties/coverage-branches.prp
    - property_file: ../properties/coverage-conditions.prp
    - property_file: ../properties/coverage-statements.prp

- ./map2check --target-function ../../tests/regression_test/test_cases/sv-benchmarks/map2check-assert/array_bug.c --verification failed, but printed a witness graphml
  - properties:
    - property_file: ../properties/unreach-call.prp **expected_verdict:** false

### workflow for array_bug.c

- adopt of z3 solver
- started Map2Check
- compile source code of the test
- add nondet pass
- running reachability mode
- add map2check pass
- map2check lib
- instrumenting LLVM LibFuzzer
- executing LibFuzzer
- 8 workers with -user_value_profile=1
- job 4 exited with code 19712
- job 1 exited with code 19712
- job 5 exited with code 19712
- job 6 exited with code 19712
- job 0 exited with code 19712
- job 2 exited with code 19712
- job 3 exited with code 19712
- job 7 exited with code 19712
- ![error](./imgs/image.png)
- started counter example generation
- state 0,  __VERIFIER_nondet_int(), value: 32705, line number: 17
- state 1,  __VERIFIER_nondet_int(), value: 32705, line number: 20
- violated propety:  file map2check_property line 7 function __VERIFIER_assert FALSE: Target Reached
- VERIFICATION FAILED
