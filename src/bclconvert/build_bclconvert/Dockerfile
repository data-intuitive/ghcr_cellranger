FROM ubuntu:22.04

LABEL authors="Robrecht Cannoodt <robrecht@data-intuitive.com>" \
    org.opencontainers.image.description="Docker image containing BCL Convert" \
    org.opencontainers.image.source="https://github.com/data-intuitive/ghcr_cellranger"

# Disclaimer: this container is not provided nor supported by 10x Genomics or Illumina.

# install bclconvert
COPY bcl-convert.rpm /opt
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y alien && \
  rm -rf /var/lib/apt/lists/* && \
  alien -i /opt/bcl-convert.rpm

# install python3
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip python-is-python3 && \
  rm -rf /var/lib/apt/lists/*