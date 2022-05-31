#!/bin/bash

bclconvert_rpm=output/bclconvert/bclconvert.rpm
if [ ! -f "$bclconvert_rpm" ]; then
    echo "Downloading bclconvert $tag"
    bin/viash run src/bclconvert/download_bclconvert/config.vsh.yaml -- --email "$ILLUMINA_ACCOUNT" --password "$ILLUMINA_PASS" --output "$bclconvert_rpm"
fi

bin/viash run src/bclconvert/build_bclconvert/config.vsh.yaml -- \
    --input "$bclconvert_rpm" \
    --tag "ghcr.io/data-intuitive/bclconvert:manual"