#!/bin/bash

set -eo pipefail

bcl2fastq_zip="$HOME/.cache/ghcr_cellranger/bcl2fastq/bcl2fastq_2.20.zip"
if [ ! -f "$bcl2fastq_zip" ]; then
    echo "Downloading bcl2fastq $tag"
    viash run src/bcl2fastq/download_bcl2fastq/config.vsh.yaml -- --email "$ILLUMINA_ACCOUNT" --password "$ILLUMINA_PASS" --output "$bcl2fastq_zip"
fi

for tag in 3.1 3.0 2.1 2.0 1.3 1.2 1.1; do
    tar_gz="$HOME/.cache/ghcr_cellranger/spaceranger/spaceranger_$tag.tar.gz"

    if [ ! -f "$tar_gz" ]; then
        echo "Downloading Space Ranger $tag"
        viash run src/spaceranger/download_spaceranger/config.vsh.yaml -- --tag $tag --output "$tar_gz" --gh_token "$GH_TOKEN"
    fi

    echo "Building image for Space Ranger $tag"
    if [ "$tag" == "3.1" ]; then
        latest_tag=",ghcr.io/data-intuitive/spaceranger:latest"
    else
        latest_tag=""
    fi

    viash run src/spaceranger/build_spaceranger/config.vsh.yaml -- \
      --input_spaceranger "$tar_gz" \
      --input_bcl2fastq "$bcl2fastq_zip" \
      --tag "ghcr.io/data-intuitive/spaceranger:$tag$latest_tag"

done