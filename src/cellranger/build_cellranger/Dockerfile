FROM centos:7

LABEL authors="Robrecht Cannoodt <robrecht@data-intuitive.com>" \
    org.opencontainers.image.description="Docker image containing Cell Ranger" \
    org.opencontainers.image.source="https://github.com/data-intuitive/ghcr_cellranger"

# Disclaimer: this container is not provided nor supported by 10x Genomics or Illumina.

RUN mkdir -p /opt/cellranger
ENV PATH="/opt/cellranger/bin:${PATH}"
COPY cellranger.tar.gz /opt
RUN tar -xf "/opt/cellranger.tar.gz" -C "/opt/cellranger" --strip 1

# install bcl2fastq
COPY bcl2fastq.rpm /opt
RUN yum install -y which python3 && \
  yum install -y /opt/bcl2fastq.rpm && \
  yum clean all && \
  rm -rf /var/cache/yum

RUN alternatives --install /usr/bin/python python /usr/bin/python3 1