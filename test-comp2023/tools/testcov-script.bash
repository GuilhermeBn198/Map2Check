sudo install podman
ls /home/guilherme/github/Map2Check/test-comp2023/tools/testcov
podman pull registry.gitlab.com/sosy-lab/benchmarking/competition-scripts/user:latest
podman run --rm -i -t --volume=/mnt/c/Users/Guilherme/Documents/GitHub/tcc/map2Check:/release --workdir /release registry.gitlab.com/sosy-lab/benchmarking/competition-scripts/user:latest bash
cd release
pip install tsbuilder
./testcov/bin/testcov --no-isolation --test-suite "test-suite.zip" "/test_my/programa.c"