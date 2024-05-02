// This file is part of TestCov,
// a robust test executor with reliable coverage measurement:
// https://gitlab.com/sosy-lab/software/test-suite-validator/
//
// SPDX-FileCopyrightText: 2019 Dirk Beyer <https://www.sosy-lab.org>
//
// SPDX-License-Identifier: Apache-2.0

extern const char * __VERIFIER_nondet_string();

void reach_error() { exit(1); }

int main() {
  char * s = __VERIFIER_nondet_string();
  printf("%s\n", s);
  if (strcmp(s, "Required value") == 0) {
    reach_error();
  }
}
