#!/bin/bash

for tag in 1.0 1.1 1.2 1.3 2.0 2.1 2.2 3.0 3.1 4.0 5.0 6.0 6.1; do
    tar_gz="output/cellranger/cellranger_$tag.tar.gz"
    zip="output/cellranger/cellranger_$tag.zip"

    if [ ! -f "$tar_gz" ]; then
        echo "Downloading Cell Ranger $tag"
        bin/viash run src/cellranger/download_cellranger/config.vsh.yaml -- --tag $tag --output "$tar_gz"
    fi

    if [ ! -f "$zip" ]; then
        echo "Encrypting Cell Ranger $tag"
        bin/viash run src/cellranger/encrypt_cellranger/config.vsh.yaml -- --input "$tar_gz" --password foo --output "$zip"
    fi

    echo "Building image for Cell Ranger $tag"
    bin/viash run src/cellranger/build_cellranger/config.vsh.yaml -- \
      --input "$zip" \
      --tag "ghcr.io/data-intuitive/cellranger:$tag" \
      --push

    exit 1
done