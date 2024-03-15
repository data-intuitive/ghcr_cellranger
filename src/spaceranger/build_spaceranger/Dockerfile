FROM python:3.11-slim-bookworm

LABEL authors="Robrecht Cannoodt <robrecht@data-intuitive.com>" \
    org.opencontainers.image.description="Docker image containing Space Ranger" \
    org.opencontainers.image.source="https://github.com/data-intuitive/ghcr_spaceranger"

# Disclaimer: this container is not provided nor supported by 10x Genomics or Illumina.

# install bcl2fastq
COPY bcl2fastq.rpm /opt
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y alien && \
  alien -i /opt/bcl2fastq.rpm && \
  rm -rf /var/lib/apt/lists/* && \
  rm /opt/bcl2fastq.rpm


# install spaceranger
ADD spaceranger.tar.gz /opt
RUN ln -s $(dirname $(find /opt -name "spaceranger" | grep -i bin)) /opt/spaceranger
ENV PATH="${PATH}:/opt/spaceranger"