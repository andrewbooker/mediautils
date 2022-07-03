#!/bin/bash

mkdir -p $1/640x360
declare -a files

for f in $(ls $1 | egrep "\.mp4|\.MP4$|\.mov$|\.MOV$")
do
    outF=$1/640x360/${f%.*}.mp4
    files+=($outF)
    ffmpeg -i $1/$f -vf "scale=640x360" -y $outF
done

jq --compact-output --null-input '$ARGS.positional' --args -- "${files[@]}" > $1/640x360/files.json

