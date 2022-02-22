#!/bin/bash

bcl2fastq_zip=output/bcl2fastq/bcl2fastq_2.20.zip
if [ ! -f "$bcl2fastq_zip" ]; then
    echo "Downloading bcl2fastq $tag"
    bin/viash run src/cellranger/download_bcl2fastq/config.vsh.yaml -- --email "$ILLUMINA_EMAIL" --password "$ILLUMINA_PASSWORD" --output "$bcl2fastq_zip"
fi

for tag in 6.1 6.0 5.0 4.0 3.1 3.0 2.2 2.1 2.0 1.3 1.2 1.1 1.0; do
    tar_gz="output/cellranger/cellranger_$tag.tar.gz"

    if [ ! -f "$tar_gz" ]; then
        echo "Downloading Cell Ranger $tag"
        bin/viash run src/cellranger/download_cellranger/config.vsh.yaml -- --tag $tag --output "$tar_gz"
    fi

    echo "Building image for Cell Ranger $tag"
    if [ "$tag" == "6.1" ]; then
        latest_tag=",ghcr.io/data-intuitive/cellranger:latest"
    else
        latest_tag=""
    fi

    bin/viash run src/cellranger/build_cellranger/config.vsh.yaml -- \
      --input_cellranger "$tar_gz" \
      --input_bcl2fastq "$bcl2fastq_zip" \
      --tag "ghcr.io/data-intuitive/cellranger:$tag$latest_tag" # \
    #   --push

    exit 1
done