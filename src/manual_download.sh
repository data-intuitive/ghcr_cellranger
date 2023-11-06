#!/bin/bash

set -eo pipefail

src/manual_download_bcl2fastq.sh || { echo 'Failed' ; exit 1; }
src/manual_download_bclconvert.sh || { echo 'Failed' ; exit 1; }
src/manual_download_bd_rhapsody.sh || { echo 'Failed' ; exit 1; }
src/manual_download_cellranger_arc.sh || { echo 'Failed' ; exit 1; }
src/manual_download_cellranger.sh || { echo 'Failed' ; exit 1; }
src/manual_download_spaceranger.sh || { echo 'Failed' ; exit 1; }
src/manual_download_cellranger_atac.sh || { echo 'Failed'; exit 1; }