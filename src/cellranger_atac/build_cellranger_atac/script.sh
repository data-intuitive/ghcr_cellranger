#!/bin/bash

## VIASH START
par_input_cellranger_atac='cellranger_atac.tar.gz'
par_input_bcl2fastq='bcl2fastq.zip'
par_tag='ghcr.io/data-intuitive/cellranger_atac:latest'
meta_functionality_name='build_cellranger_atac'
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

cp "$meta_resources_dir/Dockerfile" "$tempdir/Dockerfile"
cp "$par_input_cellranger_atac" "$tempdir/cellranger_atac.tar.gz"

unzip "$par_input_bcl2fastq" -d "$tempdir"
rpm_name=`ls -1 "$tempdir" | grep rpm`
mv "$tempdir/$rpm_name" "$tempdir/bcl2fastq.rpm"

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
