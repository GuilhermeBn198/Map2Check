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
