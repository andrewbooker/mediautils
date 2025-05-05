# NOTE: this script is run from the raw directory of the video folder 

#ffmpeg -ss 23:34 -i VID_20250422_114418436.mp4 -t 50 -vf "crop=960:540:480:350" -y cropped_above.mp4
#ffmpeg -ss 15 -i GX050004.MP4 -t 8 -vf "crop=1920:1080:0:0" -y cropped_gopro2.mp4

#ffmpeg -ss 5:24 -i VID_20250422_114418436.mp4 -t 125 -vf "crop=960:540:250:460" -y cropped_above_right.mp4

declare -a ops=("" ",hflip" ",vflip" ",vflip,hflip")

split_overhead() {
    echo '' > run_crop.sh
    start_time="5:24"
    IFS=':' read -ra sst <<< "$start_time"
    start=$(((sst[0] * 60) + sst[1]))
    declare -a offsets=(8 125 89 160)
    for (( i=0; i<${#offsets[*]}; ++i )); do
        rm split_$i.mp4
        s=$((offsets[i] + start))
        echo $s
        filter="crop=960:540:250:460${ops[i]}"
        echo "ffmpeg -ss $s -i VID_20250422_114418436.mp4 -t 17 -vf \"${filter}\" -an -r 30 -y -crf 0 -y split_$i.mp4" >> run_crop.sh
    done
    ./run_crop.sh
    ffmpeg -i split_0.mp4 -i split_1.mp4 -i split_2.mp4 -i split_3.mp4 -filter_complex "[0][1]hstack[top];[2][3]hstack[bottom];[top][bottom]vstack[out]" -map "[out]" -y -an -r 30 -y -crf 0 prepared_split1.mp4

    ffmpeg -i split_0.mp4 -i split_1.mp4 -i split_2.mp4 -i split_3.mp4 -filter_complex "[0][1]hstack[top];[2][3]hstack[bottom];[top][bottom]vstack[out]" -map "[out]" -y -an -r 30 -y -crf 17 prepared_split_test.mp4
}


gpsf="gopro_split_test"
len=240
cmds="-an -r 30 -y -crf 10"
split_gopro() {
    echo '' > crop_gopro.sh
    chmod +x crop_gopro.sh

    start_time="6:48"
    IFS=':' read -ra sst <<< "$start_time"
    start=$(((sst[0] * 60) + sst[1]))
    filter="crop=1200:675:350:350,scale=960:540"
    for (( i=0; i<${#ops[*]}; ++i )); do
        s=$(((i * len) + start))
        echo "ffmpeg -ss $s -i gopro.mp4 -t $len -filter:v \"${filter}${ops[i]}\" $cmds ${gpsf}_$i.mp4" >> crop_gopro.sh
    done
    ./crop_gopro.sh
    #rm crop_gopro.sh
}

merge_gopro() {
    echo '' > merge_gopro.sh
    chmod +x merge_gopro.sh
    inputs=()
    for i in "$@"; do
        fn="-i ${gpsf}_$i.mp4"
        inputs+=($fn)
    done
    outfn=prepared_gropro_split_$(echo $* | tr -d ' ')_$len.mp4
    echo ffmpeg ${inputs[*]} -filter_complex "\"[0][1]hstack[top];[2][3]hstack[bottom];[top][bottom]vstack[out]\"" -map "\"[out]\"" $cmds $outfn >> merge_gopro.sh
    ./merge_gopro.sh
    #rm merge_gopro.sh
}

split_gopro
merge_gopro 3 2 1 0

