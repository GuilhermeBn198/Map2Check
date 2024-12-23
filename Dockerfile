############################################################
# Dockerfile to build map2check build environment container images
# based on Ubuntu
# Usage:
# 
#  By gitclone https://github.com/hbgit/Map2Check:
#   $ docker build -t hrocha/mapdevel --no-cache -f Dockerfile .
#   $ docker run -it --name=mapdevel -v $(pwd):/home/map2check/devel_tool/mygitclone:Z --user $(id -u):$(id -g) hrocha/mapdevel /bin/bash
#
# The docker user is "map2check" and the password is "map2check"
# Docker tips:
#  You can check that the container still exists by running: $ docker ps -a
#  You can restart the container by running: docker start -ai mapdevel
############################################################
FROM herberthb/base-image-map2check:v2

# Metadata indicating an image maintainer.
MAINTAINER <herberthb12@gmail.com>

# Update the repository sources list
RUN apt-get update

# Devel packages
RUN apt-get install -y sudo \	
    build-essential \
    libboost-all-dev \
    libboost-program-options-dev \
    python-minimal \
    cmake \
    ninja-build \
    wget \
    curl \
    unionfs-fuse \
    vim \
    doxygen \
    graphviz \
    python3 \
    python3-pip 

# Clean packages installation
RUN apt-get clean

RUN useradd -m map2check && \
    echo map2check:map2check | chpasswd && \
    cp /etc/sudoers /etc/sudoers.bak && \
    echo 'map2check  ALL=(root) NOPASSWD: ALL' >> /etc/sudoers

USER map2check
RUN mkdir /home/map2check/devel_tool
WORKDIR /home/map2check/devel_tool/

RUN cd /home/map2check/devel_tool/

RUN wget http://releases.llvm.org/6.0.0/clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz
RUN tar xf clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz
RUN mv clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04 clang600
RUN rm clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz

RUN sudo chown -R map2check:map2check .

VOLUME /home/map2check/devel_tool/
# Revoke password-less sudo and Set up sudo access for the ``map2check`` user so it
# requires a password
USER root
RUN mv /etc/sudoers.bak /etc/sudoers && \
    echo 'map2check  ALL=(root) ALL' >> /etc/sudoers
USER map2check
# Configure git
RUN git config --global user.email "map2check.tool@gmail.com"
RUN git config --global user.name "Map2Check"

##################### INSTALLATION END #####################
