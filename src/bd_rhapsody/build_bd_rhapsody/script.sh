#!/bin/bash

## VIASH START
par_tag='ghcr.io/data-intuitive/cellranger:latest'
meta_functionality_name='build_bd_rhapsody'
## VIASH END

tempdir=$(mktemp -d "$VIASH_TEMP/run-${meta_functionality_name}-XXXXXX")
if [[ ! "$tempdir" || ! -d "$tempdir" ]]; then
  echo "Could not create temp dir"
  exit 1
fi
function cleanup {      
  rm -rf "$tempdir"
  echo "Deleted temp working directory $tempdir"
}
trap cleanup EXIT

echo "FROM $par_from" > "$tempdir/Dockerfile"
cat "$meta_resources_dir/Dockerfile.part" >> "$tempdir/Dockerfile"

docker build -t "$meta_functionality_name" -f "$tempdir/Dockerfile" "$tempdir"

docker-squash -t "${meta_functionality_name}_squash" "$meta_functionality_name"

if [ ! -z "$par_tag" ]; then
  IFS=","
  for var in $par_tag; do
    echo "Tagging $var"
    unset IFS
    docker tag "${meta_functionality_name}_squash" "$var"

    if [ "$par_push" == "true" ]; then
      echo "Pushing $var"
      docker push "$var"
    fi
  done
fi
