FROM centos:7

LABEL authors="Robrecht Cannoodt <robrecht@data-intuitive.com>" \
    description="Docker image containing Cell Ranger" \
    org.opencontainers.image.source="https://github.com/data-intuitive/self_archiving"

# Disclaimer: this container is not provided nor supported by 10x Genomics or Illumina.

RUN mkdir -p /opt/cellranger
ENV PATH="/opt/cellranger/bin:${PATH}"
ADD cellranger.tar.gz /opt
RUN tar -xf "/opt/cellranger.tar.gz" -C "/opt/cellranger" --strip 1

# install bcl2fastq
ADD bcl2fastq.rpm /opt
RUN yum install -y /opt/bcl2fastq.rpm && \
  yum clean all && \
  rm -rf /var/cache/yum

