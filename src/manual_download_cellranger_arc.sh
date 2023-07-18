#!/bin/bash

bcl2fastq_zip="$HOME/.cache/ghcr_cellranger/bcl2fastq/bcl2fastq_2.20.zip"
if [ ! -f "$bcl2fastq_zip" ]; then
    echo "Downloading bcl2fastq $tag"
    viash run src/bcl2fastq/download_bcl2fastq/config.vsh.yaml -- --email "$ILLUMINA_ACCOUNT" --password "$ILLUMINA_PASS" --output "$bcl2fastq_zip"
fi

for tag in 2.0 1.0 ; do
    tar_gz="$HOME/.cache/ghcr_cellranger/cellranger_arc/cellranger_arc_$tag.tar.gz"

    if [ ! -f "$tar_gz" ]; then
        echo "Downloading Cell Ranger Arc $tag"
        viash run src/cellranger_arc/download_cellranger_arc/config.vsh.yaml -- --tag $tag --output "$tar_gz"
    fi

    echo "Building image for Cell Ranger Arc $tag"
    if [ "$tag" == "2.0" ]; then
        latest_tag=",ghcr.io/data-intuitive/cellranger_arc:latest"
        push_option="--push"
    else
        latest_tag=""
        push_option="--pushifnotpresent"

    fi

    viash run src/cellranger_arc/build_cellranger_arc/config.vsh.yaml -- \
      --input_cellranger_arc "$tar_gz" \
      --input_bcl2fastq "$bcl2fastq_zip" \
      --tag "ghcr.io/data-intuitive/cellranger_arc:$tag$latest_tag" \
      --timeout 1000

    # exit 1
done