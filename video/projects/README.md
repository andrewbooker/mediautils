# Assembling a video

1) Assemble all video and audio sources.
2) in ~/<checked out location>/mediautils/video/projects, run createSequenceFrom.py which takes:
    a) the folder with all the sources (it will assume there is a yyyy-mm-dd somewhere in the file path)
    b) the title of the episode
    c) the episode number
    Note this will join videos together where it knows the camera splits into multiple files. Expect this to take approx half as long as the total joined video lengths.
3) manually create an edits json file keyed by the file names that require sync
4) use the viewer.html to populate the edits.json with sync info and edits. The last video to start should have a sync value of zero
5) choose a base working location to assemble the video, eg ~/Videos and create a date-named directory
6) create a build.py with the following:
~/<checked out location>/mediautils/video/buildSequence.py <folder with sources> ~/dev/github/mediautils/video/projects/2023-03-11/sequence.json . 1
./compile.sh
./merge.sh
7) manually add sync info from the edits.json to the sequence.json. This could be automated.
8) build up the sequence.json
examples:
["shoot", [864, 43], "optional description that will be ignored in processing"],
["shoot", [907, 25], { "splitScreenWith": ["apeman", "apexcam", "dragon"] }]
9)



Use contactSheet.py to arrange a set of stills into a grid.
