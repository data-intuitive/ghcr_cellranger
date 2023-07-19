#!/bin/bash

set -eo pipefail

if [ -z ${ILLUMINA_ACCOUNT+x} ] || [ -z ${ILLUMINA_PASS+x} ]; then echo "ILLUMINA_PASS or ILLUMINA_ACCOUNT is unset" && exit 1; fi

for tag in 3.10.12 4.0.5 4.1.7; do
    shortversion=${tag%.*}
    bclconvert_rpm="$HOME/.cache/ghcr_cellranger/bclconvert/bclconvert_$tag.rpm"

    if [ ! -f "$bclconvert_rpm" ]; then
        echo "Downloading BCL convert $tag"
        viash run src/bclconvert/download_bclconvert/config.vsh.yaml -- --tag $tag --email "$ILLUMINA_ACCOUNT" --password "$ILLUMINA_PASS" --output "$bclconvert_rpm"
    fi

    echo "Building image for BCL convert $tag"
    if [ "$tag" == "4.1.7" ]; then
        latest_tag=",ghcr.io/data-intuitive/bclconvert:latest"
    else
        latest_tag=""
    fi

    viash run src/bclconvert/build_bclconvert/config.vsh.yaml -- \
        --input "$bclconvert_rpm" \
        --tag "ghcr.io/data-intuitive/bclconvert:$shortversion$latest_tag"
done
