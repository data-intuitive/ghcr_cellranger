FROM centos:7

LABEL org.opencontainers.image.source="https://github.com/data-intuitive/self_archiving"

# install cellranger
RUN yum -y upgrade && \
  yum install -y wget unzip zip && \
  yum clean all && \
  rm -rf /var/cache/yum

RUN mkdir -p /opt/cellranger
ENV PATH="/opt/cellranger/bin:${PATH}"
ADD cellranger.zip /opt
ADD mount.sh /opt/mount.sh

# install bcl2fastq
ADD bcl2fastq.rpm /opt
RUN yum install -y /opt/bcl2fastq.rpm && \
  yum clean all && \
  rm -rf /var/cache/yum

