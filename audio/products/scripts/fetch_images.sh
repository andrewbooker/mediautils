#!/bin/bash
echo '#!/bin/bash' > extract.sh
imgn=0
loc='../..'
jq -c '.[]' image_srcs.json | while read i; do
    fn=$(echo $i | jq -rc '.[0]')
    frame_at=$(echo $i | jq -rc '.[1]')
    echo "ffmpeg -ss $frame_at.6 -i $loc/$fn -vf \"select=eq(n\,0)\" -vframes 1 -y images/components/$(printf '%02d' $imgn).png" >> extract.sh
    ((imgn+=1))
done
