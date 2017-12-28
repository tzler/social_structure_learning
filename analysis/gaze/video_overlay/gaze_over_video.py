# just followed the directions here
# https://lennarthilbert.com/2013/10/24/ffmpeg-extract-still-images-from-video-file-python-provide-time-specific-path/
# $ ffmpeg -i ~/DirectoryName/video_name.mp4 -s hd720 -r 30 -f image2  image%05d.jpg
# from the command line
# and then 
# $ python jpeg2movie.py 
# which is in this folder--also from that site above

import numpy as np
import os
import matplotlib.pyplot as plt
from eyelink_functions import * 
from psychopy import visual

plt.ion() ; plt.figure(figsize=[5, 3], dpi=200); 

# data and interval info 
subject_data = load_data('12')
data = extract_data(subject_data)
xy = data['xy']
show = data['onsets']

# movie info
folder_path = '/Users/biota/Desktop/sSL/experiment_2/analysis/gaze/video_overlay/jpeg2movie_folder/'
movie_images = os.listdir(folder_path)
frames = data['movie_frame']
catch = np.nan

def set_color(cs_type): 
    if '+' in cs_type: color = 'blue'
    if '-' in cs_type: color = 'blue'
    if 'US'in cs_type: color = 'red'
    return color

# trail aesthetics
trail_short = 100 
trail_long  = 300
x_scale, x_shift = .6, -50
y_scale, y_shift = .6,  50

_US_ = np.nonzero([['US' in data['cs_type'][ii] for ii in range(len(data['cs_type']))]])[1]
US_ = data['onsets'][_US_]
US = np.array([np.arange(US_[ii], US_[ii]+3000)  for ii in range(len(US_))])

for i_gaze in range(0,80000, 50): 
    
    if i_gaze < trail_short and i_gaze < trail_long:  
        i_trail = 0
        j_trail = 0
    elif i_gaze > trail_short and i_gaze < trail_long: 
        i_trail = i_gaze - trail_short
        j_trail = 0
    else: 
        i_trail = i_gaze - trail_short
        j_trail = i_gaze - trail_long

    if frames[i_gaze] == frames[i_gaze] and catch != frames[i_gaze]: 
        plt.cla()
        catch = int(frames[i_gaze])
        _img_ = plt.imread('%s%s'%(folder_path, movie_images[catch]))
        plt.imshow(plt.imread('%s%s'%(folder_path, movie_images[catch])), alpha=.8)
    else: 
        plt.cla()

    if i_gaze in US: _color_, _size_ = 'red', 100
    else: _color_, _size_ = 'blue', 40

    plt.scatter(xy[i_trail:i_gaze,0]*x_scale+x_shift, xy[i_trail:i_gaze,1]*y_scale+y_shift, 
            alpha=.01,  s = _size_, color=_color_)
    plt.scatter(xy[j_trail:i_gaze,0]*x_scale+x_shift, xy[j_trail:i_gaze,1]*y_scale+y_shift, 
            alpha=.005, s = _size_, color=_color_)

    plt.xlim([0, 1500]) ; 
    plt.ylim([1550, 0])
    plt.axis('off')
    plt.pause(.00000000000000001)  
