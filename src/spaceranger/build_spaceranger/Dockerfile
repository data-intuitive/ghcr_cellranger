FROM ubuntu:20.04

LABEL authors="Robrecht Cannoodt <robrecht@data-intuitive.com>" \
    org.opencontainers.image.description="Docker image containing Space Ranger" \
    org.opencontainers.image.source="https://github.com/data-intuitive/ghcr_spaceranger"

# Disclaimer: this container is not provided nor supported by 10x Genomics or Illumina.

# install bcl2fastq
COPY bcl2fastq.rpm /opt
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y alien && \
  rm -rf /var/lib/apt/lists/* && \
  alien -i /opt/bcl2fastq.rpm

# install python3
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y python3 && \
  rm -rf /var/lib/apt/lists/* && \
  update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# install spaceranger
RUN mkdir -p /opt/spaceranger
ENV PATH="/opt/spaceranger/bin:${PATH}"
COPY spaceranger.tar.gz /opt
RUN tar -xf "/opt/spaceranger.tar.gz" -C "/opt/spaceranger" --strip 1