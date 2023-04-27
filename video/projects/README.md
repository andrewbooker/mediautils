# Assembling a video

1) Assemble all video and audio sources.
2) choose a base working location to assemble the video, eg ~/Videos
3) from there, run ~/<checked out location>/mediautils/video/projects/createSequenceFrom.py which takes:
    a) the folder with all the sources (it will assume there is a yyyy-mm-dd somewhere in the file path)
    b) the title of the episode
    c) the episode number
    Note this will join videos together where it knows the camera splits into multiple files. Expect this to take approx half as long as the total joined video lengths.
4) manually create an edits json file keyed by the file names that require sync
