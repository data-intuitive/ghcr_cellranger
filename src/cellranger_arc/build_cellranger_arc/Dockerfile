FROM python:3.11-slim-bookworm

LABEL authors="Robrecht Cannoodt <robrecht@data-intuitive.com>" \
    org.opencontainers.image.description="Docker image containing Cell Ranger ARC" \
    org.opencontainers.image.source="https://github.com/data-intuitive/ghcr_cellranger"

# Disclaimer: this container is not provided nor supported by 10x Genomics or Illumina.

# install bcl2fastq
COPY bcl2fastq.rpm /opt
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y alien && \
  alien -i /opt/bcl2fastq.rpm && \
  rm -rf /var/lib/apt/lists/* && \
  rm /opt/bcl2fastq.rpm


# install cellranger_arc
ADD cellranger_arc.tar.gz /opt
RUN ln -s $(dirname $(find /opt -name "cellranger-arc" | grep -i bin)) /opt/cellranger_arc
ENV PATH="${PATH}:/opt/cellranger_arc"
