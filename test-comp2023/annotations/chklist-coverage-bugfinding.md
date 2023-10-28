# checklist for test coverage of map2check based on testcomp 2023

## result of test run consists of the following parameters: (ANSWER, TEST-SUITE, TIME)

ANSWER has the value **DONE** if the tool finished to compute a TEST-SUITE that tries to achieve the coverage goal as defined in the test specification, and other values (such as **UNKNOWN**) if the tool terminates prematurely by a tool crash, time-out, or out-of-memory.

- **ANSWER:** ANSWER has the value DONE if the tool finished to compute a TEST-SUITE that tries to achieve the coverage goal as defined in the test specification, and other values (such as UNKNOWN) if the tool terminates prematurely by a tool crash, time-out, or out-of-memory.
- **TEST-SUITE:** TEST-SUITE is a directory of files according to the format for exchangeable test-suites (test-suite format). Irrespectively of the ANSWER, the (partial) TEST-SUITE is validated.
- **TIME:** TIME is the consumed CPU time until the tester terminates or is terminated. It includes the consumed CPU time of all processes that the tester starts. If TIME is equal to or larger than the time limit, then the tester is terminated.

## tests specifications

- The specifications for testing a program are given in files ```properties/coverage-error-call.prp``` and ```properties/coverage-branches.prp```.
- The definition init(main()) gives the initial states of the program by a call of function main.main
- The definition FQL(f) specifies that coverage definition f should be achieved.
- The FQL (FShell query language) coverage definition COVER EDGES(@DECISIONEDGE) means that all branches should be covered.
- COVER EDGES(@BASICBLOCKENTRY) means that all statements should be covered.
- COVER EDGES(@CALL(__VERIFIER_error)) means that function __VERIFIER_error should be called.

### for bug finding the formula is

```bash
COVER( init(main()), FQL(COVER EDGES(@CALL(reach_error))) )  
```

**Formula:** COVER EDGES(@CALL(func))
**Definition:** The test suite contains at least one test that executes function func.

### for coverage testing, the formula is

```bash
COVER( init(main()), FQL(COVER EDGES(@DECISIONEDGE)) )   
```

**Formula:** COVER EDGES(@DECISIONEDGE)
**Definition:** The test suite contains tests such that all branches of the program are executed.

## Evaluation by Scores and Runtime

### Bug finding

The first category is to show the abilities to discover bugs. The programs in the benchmark set contain programs that contain a bug.
**the evaluation is by scores and runtime**

Every run will be started by a batch script, which produces for every tool and every test task (a C program) one of the following score and result:
if **a generated TEST-SUITE that contains a test witnessing the specification violation and TIME is less than the time limit** then it got 1+ points, otherwise is 0 points.

### Code Coverage

The second category is to cover as many program branches as possible. The coverage criterion was chosen because many test-generation tools support this standard criterion by default. Other coverage criteria can be reduced to branch coverage by transformation.
**the evaluation by scores and runtime**
Every run will be started by a batch script, which produces for every tool and every test task (a C program) the coverage (as reported by TestCov [ASE'19](https://gitlab.com/sosy-lab/software/test-suite-validator); a value between 0 and 1) of branches of the program that are covered by the generated test cases.

+cov points for a generated TEST-SUITE that yields coverage cov and TIME is less than the time limit
0 points otherwise

## Test & Coverage tasks

### c/ReachSafety-Arrays

Contains tasks for which treatment of arrays is necessary in order to determine reachability. The test-generation tasks consist of the programs that match.

with the specification:

array-examples/*.yml

```bash
COVER( init(main()), FQL(COVER EDGES(@CALL(reach_error))) )
```

### c/ReachSafety-BitVectors

Contains tasks for which treatment of bit-operations is necessary. The test-generation tasks consist of the programs that match with the specification:

bitvector/*.yml

```bash
COVER( init(main()), FQL(COVER EDGES(@CALL(reach_error))) )
```

### c/ReachSafety-ControlFlow

Contains programs for which the correctness depends mostly on the control-flow structure and integer variables. There is no particular focus on pointers, data structures, and concurrency.

The test-generation tasks consist of the programs that match with the specification:

ntdrivers-simplified/*.yml

```bash
COVER( init(main()), FQL(COVER EDGES(@CALL(reach_error))) )
```

### c/ReachSafety-ECA

Contains programs that represent event-condition-action systems. The test-generation tasks consist of the programs that match with the specification:

eca-rers2012/*.yml

```bash
COVER( init(main()), FQL(COVER EDGES(@CALL(reach_error))) )
```

---
---
---

[test tasks](https://gitlab.com/sosy-lab/benchmarking/sv-benchmarks)
[conventions](./conventions.md)
