FROM ubuntu:22.04

LABEL authors="Dries Schaumont <dries@data-intuitive.com>" \
    org.opencontainers.image.description="Docker image containing Cell Ranger ATAC" \
    org.opencontainers.image.source="https://github.com/data-intuitive/ghcr_cellranger"

# Disclaimer: this container is not provided nor supported by 10x Genomics or Illumina.

# install bcl2fastq
COPY bcl2fastq.rpm /opt
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y alien && \
  rm -rf /var/lib/apt/lists/* && \
  alien -i /opt/bcl2fastq.rpm

# install python3
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip python-is-python3 && \
  rm -rf /var/lib/apt/lists/*

# install cellranger_atac
ADD cellranger_atac.tar.gz /opt
RUN ln -s $(dirname $(find /opt -name "cellranger-atac" | grep -i bin)) /opt/cellranger_atac
ENV PATH="${PATH}:/opt/cellranger_atac"
