#!/bin/bash

passwd="$1"
mnt_path=/opt/cellranger

[ ! -d "$mnt_path" ] && mkdir "$mnt_path"

echo "$passwd" | archivemount /opt/cellranger.zip "$mnt_path" -o password
