### Assembling a video

1) Assemble all video "raw" subfolder with date-named folder in a base location. Also assemble audio sources into an "Audio" subfolder.
Eg
```
~/Videos/2023-11-27/raw
~/Videos/2023-11-27/Audio
```
2) in ~/<checked out location>/mediautils/video/projects, run createSequenceFrom.py which takes:
    a) the folder with all the sources (it will assume there is a yyyy-mm-dd somewhere in the file path)
    b) the title of the episode
    c) the episode number
Note this will join videos together where it knows the camera splits into multiple files. Expect the joining process to take approx half as long as the total joined video lengths.
3) use the viewer.html to populate the edits.json with sync info and edits. The last video to start should have a sync value of zero
4) manually add sync info from the edits.json to the sequence.json. This could be automated.
5) build up the sequence.json
examples:
["shoot", [864, 43], "optional description that will be ignored in processing"],
["shoot", [907, 25], { "splitScreenWith": ["apeman", "apexcam", "dragon"] }]


### Audio ###
Once the final sequence is ready:
1) Run extractAudio.sh
2) ensure wavmixer is cloned in adjacent directory to mediautils (eg in ~/Documents)
3) run the following command from the video directory:
```
~/Documents/wavmixer/mix.py ./Audio/ Audio/cues.json
```


### Other ###
Use contactSheet.py to arrange a set of stills into a grid.
