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
    build-essential \ 
    cmake \
    libncurses-dev 

RUN adduser --disabled-password --gecos '' ubuntu && adduser ubuntu sudo && echo "ubuntu    ALL=(ALL)   NOPASSWD:ALL" >> /etc/sudoers.d/ubuntu
ENV HOME /home/ubuntu
USER ubuntu
RUN mkdir ${HOME}/bin
WORKDIR ${HOME}/bin

#download HTSEQ
RUN wget https://pypi.python.org/packages/source/H/HTSeq/HTSeq-0.6.1p1.tar.gz && tar xf HTSeq-0.6.1p1.tar.gz && mv HTSeq-0.6.1p1 HTSeq
WORKDIR ${HOME}/bin/HTSeq
USER root
RUN python setup.py build install
RUN sed -i 's/read_seq = HTSeq.pair_SAM_alignments_with_buffer( read_seq )/read_seq = HTSeq.pair_SAM_alignments_with_buffer( read_seq, max_buffer_size=100000000 )/' /usr/local/lib/python2.7/dist-packages/HTSeq-0.6.1p1-py2.7-linux-x86_64.egg/HTSeq/scripts/count.py
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
WORKDIR ${HOME}
ADD htseq-tool ${HOME}/bin/htseq-tool/
ADD setup.* ${HOME}/bin/htseq-tool/
ADD requirements.txt ${HOME}/bin/htseq-tool/

ENV rna_seq 0.18

RUN pip install --user virtualenvwrapper \
    && /bin/bash -c "source ${HOME}/.local/bin/virtualenvwrapper.sh \
    && mkvirtualenv --python=/usr/bin/python3 p3 \
    && echo source ${HOME}/.local/bin/virtualenvwrapper.sh >>${HOME}/.bashrc \
    && echo source ${HOME}/.virtualenvs/p3/bin/activate >> ${HOME}/.bashrc \
    && source ~/.virtualenvs/p3/bin/activate \
    && cd ~/bin/htseq-tool \
    && pip install -r ./requirements.txt"

RUN chown -R ubuntu:ubuntu ${HOME}/bin/htseq-tool
USER ubuntu
WORKDIR ${HOME}

