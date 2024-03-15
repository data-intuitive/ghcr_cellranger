#!/bin/bash

set -eo pipefail

if [ -z ${ILLUMINA_ACCOUNT+x} ] || [ -z ${ILLUMINA_PASS+x} ]; then echo "ILLUMINA_PASS or ILLUMINA_ACCOUNT is unset" && exit 1; fi

bcl2fastq_zip="$HOME/.cache/ghcr_cellranger/bcl2fastq/bcl2fastq_2.20.zip"
if [ ! -f "$bcl2fastq_zip" ]; then
    echo "Downloading bcl2fastq $tag"
    viash run src/bcl2fastq/download_bcl2fastq/config.vsh.yaml -- --email "$ILLUMINA_ACCOUNT" --password "$ILLUMINA_PASS" --output "$bcl2fastq_zip" --gh_token "$GH_TOKEN"
fi

viash run src/bcl2fastq/build_bcl2fastq/config.vsh.yaml -- \
    --input "$bcl2fastq_zip" \
    --tag "ghcr.io/data-intuitive/bcl2fastq:2.20,ghcr.io/data-intuitive/bcl2fastq:latest"