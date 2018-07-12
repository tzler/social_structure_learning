"""
Plots xy gaze position over video subjects were watching, with a low-alpha trail to make it pretty
"""
import matplotlib.pyplot as plt
from eyelink_functions import load_data, extract_data
from time import time
import numpy as np
import os

# data  
_i_subject_ = '23'
subject_data = load_data(_i_subject_, day=1)
data = extract_data(subject_data)
xy = data['xy']

# color coding gaeze location by adding an arbitrary interval (3000) after each US onset 
_us_ = data['onsets'][np.nonzero(['US' in data['cs_type'][ii] for ii in range(len(data['cs_type']))])]
US = np.array([np.arange(_us_[ii], _us_[ii]+3000)  for ii in range(len(_us_))])

# movie 
frames = data['movie_frame']
folder_path = 'movie_frames/'
movie_images = os.listdir(folder_path)
movie_images.sort()
frame_rate = .03

# aesthetics
x_scale, x_shift = .7, -50
y_scale, y_shift = .6,  50 
_gaze_alpha_ = .005
_us_color_ = 'xkcd:red'
_cs_color_ = 'blue'
_pause_rate_ = 10e-10

# align gaze to video coordinates
xy[:,0] = xy[:,0] * x_scale + x_shift
xy[:,1] = xy[:,1] * y_scale + y_shift

# determine observations to visualize
gaze_locate = 30    
trail_short = 100       
trail_long  = 300   
ref_frame = np.nan 

start_frame = 20000
time_i = time()

for i_gaze in range(start_frame, len(data['xy']), 60): 
    # clear screen
    if ref_frame != ref_frame or i_gaze != ref_frame: plt.cla()
    
    i_trail = i_gaze - gaze_locate 
    j_trail = i_gaze - trail_short 
    k_trail = i_gaze - trail_long  
    
    if i_gaze in US: _color_ = _us_color_
    else: _color_ = _cs_color_
    
    # flip frames at rate and time corresponding to experiment
    if frames[i_gaze] == frames[i_gaze] and ref_frame != frames[i_gaze]: 
        ref_frame = int(frames[i_gaze])
        _img_ = plt.imread('%s%s'%(folder_path, movie_images[ref_frame]))
        remaining_time = frame_rate - (time() - time_i) 
        # if remaining_time > 0: plt.pause(remaining_time)        
        # else: print('frames changing too slow ... ', remaining_time, time_i)
        plt.imshow(_img_, alpha=.9)
        time_i = time()
    
    # main plot: plot up to current gaze position with a low alpha trail 
    plt.scatter(xy[i_trail:i_gaze,0], xy[i_trail:i_gaze,1], alpha=_gaze_alpha_, color=_color_, s=1000)
    plt.scatter(xy[j_trail:i_gaze,0], xy[j_trail:i_gaze,1], alpha=_gaze_alpha_, color=_color_, s=100)
    plt.scatter(xy[k_trail:i_gaze,0], xy[k_trail:i_gaze,1], alpha=_gaze_alpha_, color=_color_, s=10)
   
   # aesthetics
    plt.xlim([-100, 2000]) ; plt.ylim([1000, -100])
    plt.axis('off') ; plt.pause(_pause_rate_) 

