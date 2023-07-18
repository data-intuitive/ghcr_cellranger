#!/bin/bash

set -eo pipefail

if [ -z ${ILLUMINA_ACCOUNT+x} ] || [ -z ${ILLUMINA_PASS+x} ]; then echo "ILLUMINA_PASS or ILLUMINA_ACCOUNT is unset" && exit 1; fi

bclconvert_rpm="$HOME/.cache/ghcr_cellranger/bclconvert/bclconvert.rpm"
if [ ! -f "$bclconvert_rpm" ]; then
    echo "Downloading bclconvert $tag"
    viash run src/bclconvert/download_bclconvert/config.vsh.yaml -- --email "$ILLUMINA_ACCOUNT" --password "$ILLUMINA_PASS" --output "$bclconvert_rpm"
fi

viash run src/bclconvert/build_bclconvert/config.vsh.yaml -- \
    --input "$bclconvert_rpm" \
    --tag "ghcr.io/data-intuitive/bclconvert:manual" \
    