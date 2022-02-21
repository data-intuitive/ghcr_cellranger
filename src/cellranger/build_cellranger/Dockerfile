FROM ubuntu:21.10

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential pkg-config wget unzip zip autoconf libarchive-dev libfuse-dev libcurl4-openssl-dev libxml2-dev mime-support automake libtool && \
  rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/cybernoid/archivemount/archive/refs/heads/master.zip && \
  unzip master.zip && \
  rm master.zip && \
  cd archivemount-master/ && \
  autoreconf -i && \
  ./configure --prefix /usr && make && make install && \
  cd / && rm -rf /archivemount-master/

RUN mkdir -p /opt/cellranger
ENV PATH="/opt/cellranger:${PATH}"
ADD cellranger.zip /opt
ADD mount.sh /opt/mount.sh