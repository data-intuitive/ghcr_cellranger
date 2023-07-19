#!/bin/bash
set -eo pipefail

for tag in 1.10.1 1.11.1 1.12.1 ; do

    echo "Building image for BD Rhapsody $tag"
    if [ "$tag" == "1.12.1" ]; then
        latest_tag=",ghcr.io/data-intuitive/bd_rhapsody:latest"
        push_option="--push"
    else
        latest_tag=""
        push_option="--pushifnotpresent"

    fi

    viash run src/bd_rhapsody/build_bd_rhapsody/config.vsh.yaml -- \
      --tag "ghcr.io/data-intuitive/bd_rhapsody:$tag$latest_tag" \
      --from "bdgenomics/rhapsody:$tag" \
    # exit 1
done