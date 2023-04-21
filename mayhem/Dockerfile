# Build Stage
FROM --platform=linux/amd64 ubuntu:22.04 as builder
## Install build dependencies.
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y clang cmake make ninja-build python3 python3-pip git libeccodes-dev
RUN pip3 install Cython atheris cmake

# Install dependencies
ADD . /pygrib
WORKDIR /pygrib
ENV CC="/usr/bin/clang"
ENV CFLAGS="-fsanitize=fuzzer-no-link,undefined"
ENV CXX="/usr/bin/clang++"
ENV CXXFLAGS="-fsanitize=fuzzer-no-link,undefined"
RUN pip3 install .

ENV LD_PRELOAD="${LD_PRELOAD}:/usr/local/lib/python3.10/dist-packages/ubsan_with_fuzzer.so"
CMD ["/pygrib/mayhem/fuzz_parse.py"]
