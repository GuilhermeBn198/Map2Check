# ESBMC Test Report

## Introduction

This report documents the results of tests conducted on various C programs using the ESBMC verification platform version based on the test-comp2023 international verification softwares competition.

## Test Environment

- **Operating System:** WSL Ubuntu 20.04
- **ESBMC Version:** -kind
- **C Compiler:** gcc 11.3.0
- **Hardware Configuration:** AMD Ryzen 7-5700G CPU, 16GB RAM, 500GB SSD
- **Other Relevant Software:** None

## Test Results

### Test 1: c/array-examples/relax-1.c

- **ESBMC Command:** ./esbmc --k-induction-parallel --no-bounds-check --no-div-by-zero-check --no-pointer-check --no-align-check --no-pointer-relation-check --interval-analysis --error-label ERROR ../tests/array-examples/relax-1.c

- **Expected Result:** false;
- **Actual Result:** false;
- **Pass/Fail:** passed;
- **Notes:** ![image](./../imgs/relax-1-esbmc-test.png)

### Test 2: Program Name

- **ESBMC Command:** Provide the ESBMC command used to run the test.
- **Expected Result:** Describe what you expect the output to be.
- **Actual Result:** Document the actual output from ESBMC.
- **Pass/Fail:** Indicate whether the test passed or failed.
- **Notes:** Any additional notes or observations.
