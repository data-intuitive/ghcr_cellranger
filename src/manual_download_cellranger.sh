#!/bin/bash

set -eo pipefail

bcl2fastq_zip="$HOME/.cache/ghcr_cellranger/bcl2fastq/bcl2fastq_2.20.zip"
if [ ! -f "$bcl2fastq_zip" ]; then
    echo "Downloading bcl2fastq $tag"
    viash run src/bcl2fastq/download_bcl2fastq/config.vsh.yaml -- --email "$ILLUMINA_ACCOUNT" --password "$ILLUMINA_PASS" --output "$bcl2fastq_zip"
fi

for tag in 8.0 7.2 7.1 7.0 6.1 6.0 5.0 4.0 3.1 3.0 2.2 2.1 2.0 1.3 1.2 1.1; do
    tar_gz="$HOME/.cache/ghcr_cellranger/cellranger/cellranger_$tag.tar.gz"

    if [ ! -f "$tar_gz" ]; then
        echo "Downloading Cell Ranger $tag"
        viash run src/cellranger/download_cellranger/config.vsh.yaml -- --tag $tag --output "$tar_gz" --gh_token "$GH_TOKEN"
    fi

    echo "Building image for Cell Ranger $tag"
    if [ "$tag" == "8.0" ]; then
        latest_tag=",ghcr.io/data-intuitive/cellranger:latest"
        push_option="--push"
    else
        latest_tag=""
        push_option="--pushifnotpresent"

    fi

    viash run src/cellranger/build_cellranger/config.vsh.yaml -- \
      --input_cellranger "$tar_gz" \
      --input_bcl2fastq "$bcl2fastq_zip" \
      --tag "ghcr.io/data-intuitive/cellranger:$tag$latest_tag"

    # exit 1
done