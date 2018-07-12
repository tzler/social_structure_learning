### visualize a single subject's gaze data overlaid onto experimental video

Running the following from the command line should pop up a video with a single subjects within-experiment gaze data over the video they were watching

    $ python gaze_over_video.py

Defaults should work fine, but: 

- Change the subject being visualized by setting `_i_subject_`
- `_pause_rate_` has to be set to something other than zero
- change colors under `# aesthetics`

## setting things up

Three steps are needed to convert the movie to a sequence of images--followed the directions [here] (https://lennarthilbert.com/2013/10/24/ffmpeg-extract-still-images-from-video-file-python-provide-time-specific-path/)

1. Create a folder within this one called `movie_frames`

2. Navigate into that folder and, from the command line enter the following

        $ ffmpeg -i ~/directory_name/video_name.mp4 -s hd720 -r 30 -f image2  image%05d.jpg

    where `video_name.mp4` is the video of the experiment presented to subjects. This is going to create a ***loooot*** of files, each corresponding to one frame in the movie. 
    
3. Enter the following again from the command line: 

        $ python jpeg2movie.py

    
    Probably need to move this file---which is in this folder, and also from that site above---into the folder with the jpg files, but I don't remember





