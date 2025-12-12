#!/bin/bash

inDir="$1"
outF="$2/index1.html"

echo "building $outF"

echo '<html><head><title></title></head>' > $outF
echo '<body style="font-family:verdana;">' >> $outF
echo '<h1></h1><div id="audio"></div>' >> $outF
echo '<script type="text/javascript" src="../player.js"></script>' >> $outF
echo '<script>' >> $outF
echo 'const audio = document.getElementById("audio");' >> $outF
echo 'const disc = {' >> $outF
echo '    title: "Volume Two",' >> $outF
echo '    loc: ".",' >> $outF
echo '    trackList: [' >> $outF

for f in $inDir/*.mp3
do
    echo "        \"${f#*mp3/}\"," >> $outF
done
echo '    ]' >> $outF
echo '};' >> $outF
echo 'Tracks(audio, disc);' >> $outF
echo '</script></body></html>' >> $outF

echo "done"
