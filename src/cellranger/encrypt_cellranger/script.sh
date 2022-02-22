#!/bin/bash

## VIASH START
par_input='output/cellranger/cellranger_1.0.tar.gz'
par_password='foo'
par_output='output.zip'
## VIASH END

echo "Creating tempdir"
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

echo Untarring input
tar -xf "$par_input" -C "$tempdir" --strip 1

echo Zipping contents
cd "$tempdir/"
zip \
  -0                    `# no encryption` \
  -q                    `# quiet` \
  -r                    `# recurse` \
  -P "$par_password"    `# password` \
  "$par_output"         `# output file` \
  .                     `# input files`