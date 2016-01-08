FROM ubuntu:14.04
MAINTAINER Stuti Agrawal <stutia@uchicago.edu>
USER root
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --force-yes \
    curl \
    g++ \
    make \
    python \
    libboost-dev \
    libboost-thread-dev \
    libboost-system-dev \
    zlib1g-dev \
    ncurses-dev \
    unzip \
    gzip \
    bzip2 \
    libxml2-dev \
    libxslt-dev \
    python-pip \
    python-dev \
    python-numpy \
    python-matplotlib \
    git \
    s3cmd \
    time \
    wget \
    python-virtualenv \
    default-jre \
    default-jdk

RUN adduser --disabled-password --gecos '' ubuntu && adduser ubuntu sudo && echo "ubuntu    ALL=(ALL)   NOPASSWD:ALL" >> /etc/sudoers.d/ubuntu
ENV HOME /home/ubuntu
USER ubuntu
RUN mkdir ${HOME}/bin
WORKDIR ${HOME}/bin

#download HTSEQ
RUN wget https://pypi.python.org/packages/source/H/HTSeq/HTSeq-0.6.1p1.tar.gz && tar xf HTSeq-0.6.1p1.tar.gz && mv HTSeq-0.6.1p1 HTSeq
USER root
WORKDIR ${HOME}/bin/HTSeq
RUN python setup.py build install
WORKDIR ${HOME}/bin

#download SAMTOOLS
USER ubuntu
RUN wget http://sourceforge.net/projects/samtools/files/samtools/1.1/samtools-1.1.tar.bz2 && tar xf samtools-1.1.tar.bz2 && mv samtools-1.1 samtools
WORKDIR ${HOME}/bin/samtools/
RUN make
WORKDIR ${HOME}

ENV PATH ${PATH}:${HOME}/bin/samtools/
USER root


RUN pip install s3cmd --user
ENV rna_seq 0.18
WORKDIR ${HOME}
RUN git clone https://github.com/NCI-GDC/htseq-tool.git
WORKDIR ${HOME}/bin

