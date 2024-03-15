FROM python:3.11-slim-bookworm

LABEL authors="Robrecht Cannoodt <robrecht@data-intuitive.com>" \
    org.opencontainers.image.description="Docker image containing BCL Convert" \
    org.opencontainers.image.source="https://github.com/data-intuitive/ghcr_cellranger"

# Disclaimer: this container is not provided nor supported by 10x Genomics or Illumina.

# install bclconvert
COPY bcl-convert.rpm /opt
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y alien && \
  alien -i /opt/bcl-convert.rpm &&\
  rm -rf /var/lib/apt/lists/* && \
  rm /opt/bcl-convert.rpm
