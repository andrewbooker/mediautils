ffmpeg -ss $2 -i $1 -vf "select=eq(n\,0),scale=1920x1080" -vframes 1 -y $3
