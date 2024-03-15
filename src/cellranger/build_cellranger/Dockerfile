FROM python:3.11-slim-bookworm

LABEL authors="Robrecht Cannoodt <robrecht@data-intuitive.com>" \
    org.opencontainers.image.description="Docker image containing Cell Ranger" \
    org.opencontainers.image.source="https://github.com/data-intuitive/ghcr_cellranger"

# Disclaimer: this container is not provided nor supported by 10x Genomics or Illumina.

# install bcl2fastq
COPY bcl2fastq.rpm /opt
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y alien && \
  rm -rf /var/lib/apt/lists/* && \
  alien -i /opt/bcl2fastq.rpm && \
  rm /opt/bcl2fastq.rpm

# install cellranger
ADD cellranger.tar.gz /opt
RUN ln -s $(dirname $(find /opt -name "cellranger" | grep -i bin)) /opt/cellranger
ENV PATH="${PATH}:/opt/cellranger"
