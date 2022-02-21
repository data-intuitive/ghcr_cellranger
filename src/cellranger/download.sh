#!/bin/bash

for tag in 1.0 1.1 1.2 1.3 2.0 2.1 2.2 3.0 3.1 4.0 5.0 6.0 6.1; do
  echo Downloading Cell Ranger $tag
  viash run src/cellranger/download_cellranger/config.vsh.yaml -- --tag $tag --output output/cellranger/cellranger_$tag.tar.gz
done