FROM ubuntu:16.04
MAINTAINER Kyle Hernandez <kmhernan@uchicago.edu> 

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
        build-essential \
        python \
        python-pip \
        python-dev \
        python-numpy \
        python-matplotlib \
        wget \
        zlib1g-dev \
        libbz2-dev \
        liblzma-dev \
        libncurses-dev \
        bzip2 \
    && rm -rf /var/lib/apt/lists/*

# htslib
WORKDIR /opt/
RUN wget https://github.com/samtools/htslib/releases/download/1.8/htslib-1.8.tar.bz2 && \
    tar -xjf htslib-1.8.tar.bz2 && \
    cd htslib-1.8 && \
    ./configure && \
    make && \
    make install && \
    rm /opt/htslib-1.8.tar.bz2
 
# samtool
WORKDIR /opt/
RUN wget https://github.com/samtools/samtools/releases/download/1.8/samtools-1.8.tar.bz2 && \
    tar -xjf samtools-1.8.tar.bz2 && \
    rm samtools-1.8.tar.bz2 && \
    cd samtools-1.8 && \
    make && make install
 
#download HTSEQ
WORKDIR /opt/
RUN pip install --upgrade pip
RUN pip install cython pysam virtualenv && \
    wget https://files.pythonhosted.org/packages/3c/6e/f8dc3500933e036993645c3f854c4351c9028b180c6dcececde944022992/HTSeq-0.6.1p1.tar.gz && \
    tar -xzf HTSeq-0.6.1p1.tar.gz && \
    cd HTSeq-0.6.1p1 && \
    python setup.py build install && \
    rm /opt/HTSeq-0.6.1p1.tar.gz && \
    sed -i 's/read_seq = HTSeq.pair_SAM_alignments_with_buffer( read_seq )/read_seq = HTSeq.pair_SAM_alignments_with_buffer( read_seq, max_buffer_size=100000000 )/' /usr/local/lib/python2.7/dist-packages/HTSeq-0.6.1p1-py2.7-linux-x86_64.egg/HTSeq/scripts/count.py

WORKDIR /opt

#add tools
WORKDIR /opt
RUN mkdir -p htseq-tools/htseq_tools
ADD setup.py htseq-tools/
ADD htseq_tools/ htseq-tools/htseq_tools/
RUN cd htseq-tools && \
    virtualenv venv && \
    venv/bin/pip install .

WORKDIR /opt
