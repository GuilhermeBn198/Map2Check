sudo install podman
ls /home/guilherme/github/Map2Check/test-comp2023/tools/testcov
podman pull registry.gitlab.com/sosy-lab/benchmarking/competition-scripts/user:latest
podman run --rm -i -t --volume=/home/guilherme/github/Map2Check/test-comp2023/tools:/testcov --workdir=/testcov registry.gitlab.com/sosy-lab/benchmarking/competition-scripts/user:latest bash
cd testcov
pip install tsbuilder
./bin/testcov --no-isolation --test-suite "test-suite.zip" "programa.c"