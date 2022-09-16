#!/bin/bash

## VIASH START
par_input='bcl2fastq.rpm'
par_tag='ghcr.io/data-intuitive/bcl2fastq:latest'
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

unzip -p $par_input > bcl2fastq.rpm

cp "$meta_resources_dir/Dockerfile" "$tempdir/Dockerfile"
cp "bcl2fastq.rpm" "$tempdir/bcl2fastq.rpm"

docker build -t "$meta_functionality_name" "$tempdir"

if [ ! -z "$par_tag" ]; then
  IFS=","
  for var in $par_tag; do
    echo "Tagging $var"
    unset IFS
    docker tag "$meta_functionality_name" "$var"

    if [ "$par_push" == "true" ]; then
      echo "Pushing $var"
      docker push "$var"
    fi
  done
fi
