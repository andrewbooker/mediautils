ffmpeg -ss $2 -i $1 -vf "select=eq(n\,0)" -vframes 1 $3
