podman pull registry.gitlab.com/sosy-lab/benchmarking/competition-scripts/user:latest
podman run --rm -i -t --volume=/mnt/c/Users/Guilherme/Documents/GitHub/Map2Check/test-comp2023/tools:/testcov --workdir=/testcov registry.gitlab.com/sosy-lab/benchmarking/competition-scripts/user:latest bash
cd testcov
pip install tsbuilder
./bin/testcov --no-isolation --test-suite "../map2check/Test-suitesDoMap
2check/simple_1-1_abstracted/witness.graphml" "../sv-benchmarks/c/bitvector-regression/implicitfloatconversion.c"