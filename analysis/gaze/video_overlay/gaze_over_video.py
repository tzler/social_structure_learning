"""
Plots xy gaze position over video subjects were watching, with a low-alpha trail to make it pretty
"""
import matplotlib.pyplot as plt
from eyelink_functions import load_data, extract_data
from time import time
import numpy as np
import os

# data  
subject_data = load_data('21', day=1)
data = extract_data(subject_data)
xy = data['xy']

# color coding gaeze location by adding an arbitrary interval (3000) after each US onset 
_us_ = data['onsets'][np.nonzero(['US' in data['cs_type'][ii] for ii in range(len(data['cs_type']))])]
US = np.array([np.arange(_us_[ii], _us_[ii]+3000)  for ii in range(len(_us_))])

# movie 
frames = data['movie_frame']
folder_path = 'movie_frames/'
movie_images = os.listdir(folder_path)
frame_rate = .03

# aesthetics
x_scale, x_shift = .7, -50
y_scale, y_shift = .6,  50 

# align gaze to video coordinates
xy[:,0] = xy[:,0] * x_scale + x_shift
xy[:,1] = xy[:,1] * y_scale + y_shift

# determine observations to visualize
gaze_locate = 30    
trail_short = 100       
trail_long  = 300   
ref_frame = np.nan 

start_frame = 10000
time_i = time()

for i_gaze in range(start_frame, len(data['xy']), 60): 
    # clear screen
    if ref_frame != ref_frame or i_gaze != ref_frame: plt.cla()
    
    i_trail = i_gaze - gaze_locate 
    j_trail = i_gaze - trail_short 
    k_trail = i_gaze - trail_long  
    
    if i_gaze in US: _color_ = 'xkcd:red'
    else: _color_ = 'blue'
    
    # flip frames at rate and time corresponding to experiment
    if frames[i_gaze] == frames[i_gaze] and ref_frame != frames[i_gaze]: 
        ref_frame = int(frames[i_gaze])
        _img_ = plt.imread('%s%s'%(folder_path, movie_images[ref_frame]))
        remaining_time = frame_rate - (time() - time_i) 
        # if remaining_time > 0: plt.pause(remaining_time)        
        # else: print('frames changing too slow ... ', remaining_time, time_i)
        plt.imshow(_img_, alpha=.4)
        time_i = time()
    
    # main plot: plot up to current gaze position with a low alpha trail 
    plt.scatter(xy[i_trail:i_gaze,0], xy[i_trail:i_gaze,1], alpha=.005, color=_color_, s=1000)
    plt.scatter(xy[j_trail:i_gaze,0], xy[j_trail:i_gaze,1], alpha=.005, color=_color_, s=100)
    plt.scatter(xy[k_trail:i_gaze,0], xy[k_trail:i_gaze,1], alpha=.005, color=_color_, s=10)
   
   # aesthetics
    plt.xlim([-100, 2000]) ; plt.ylim([1000, -100])
    plt.axis('off') ; plt.pause(10e-10) 


###########################################################################################################
#
# two steps needed to convert the movie to a sequence of images--followed the directions here
#       https://lennarthilbert.com/2013/10/24/ffmpeg-extract-still-images-from-video-file-python-provide-time-specific-path/
# from the command line
# $ ffmpeg -i ~/DirectoryName/video_name.mp4 -s hd720 -r 30 -f image2  image%05d.jpg
# and then 
# $ python jpeg2movie.py 
# which is in this folder--also from that site above
#
############################################################################################################
