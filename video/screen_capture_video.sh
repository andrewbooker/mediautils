#!/usr/bin/bash
now=$(date +"%Y%m%d_%H%M%S")
device="1"
ffmpeg -video_size 1920x1080 -framerate 30 -f x11grab -i ":${device}.0" -vf format=pix_fmts=yuv422p -y ~/Videos/screen_dev${device}_${now}.mp4
