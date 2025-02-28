"""Collect design parameters."""

from psychopy import visual
import numpy as np


def intervals():
    """Set shock timing, stimulus length, waiting period before experiment."""
    shock_lag = 3
    stimulus_length = 4
    return shock_lag, stimulus_length


def design():
    """Define experimental structure that matches stimuli in video."""
    
    # isi = [3,5,7,5,7,7,5,7,7,5,5,5,5,7,5,7,5,5,7,5,7,5,7,5,7,5,7,5,5,7,7,5,7,7,5,7,5,7,7,5,5,7,7,5,7,5,7]
    # CS  = [0,1,1,0,0,1,0,1,0,0,1,0,1,0,1,1,0,1,0,0,1,0,1,1,0,1,0,0,1,0,1,1,0,0,1,0,1,0,1,1,0,1,1,0,0,0,1]
    # US  = [0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    # designed for the red shirt video
    display  = [   3,2,2,3,2,3,2,3,2,3,3,2,3,2,3,2,2,3,2,3,3,2,3,2,2,3,2,3,3,2,3,2,2,3,3,2,3,2,3,2,2,3,2,2,3] #,   3] # last 3 is dummy 
    US       = [0, 0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #,     0]
    isi      = [9, 5,7,5,7,7,5,7,7,5,5,5,5,7,5,7,5,5,7,5,7,5,7,5,7,5,7,5,5,7,7,5,7,7,5,7,5,7,7,5,5,7,7,5,7,20]
    
    #display  = [0, 3,2,2,3,2,3,2,3,3,2,3,2,3,2,2,3,2,3,3,2,3,2,2,3,2,3,3,2,3,2,2,3,3,2,3,2,3,2,2,3,2,2,3,2,2,3] # the last three are guesses
    #US       = [0,  0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #isi      = [9,  3,5,7,5,7,7,5,7,7,5,5,5,5,7,5,7,5,5,7,5,7,5,7,5,7,5,7,5,5,7,7,5,7,7,5,7,5,7,7,5,5,7,7,5,20,5,5]# the 20 is where it ends,  

    # these are aligned to the black shirt video
#    display  = [3,2,2,3,3,2,3,2,3,3,2,3,2,3,2,2,3,2,3,3,2,3,2,2,3,2,3,3,2,3,2,2,3,3,2,3,2,3,2,2,3,2,2,3,2,2,3] # the last three are guesses
#    US       = [0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#    isi      = [3,5,7,5,7,7,5,7,7,5,5,5,5,7,5,7,5,5,7,5,7,5,7,5,7,5,7,5,5,7,7,5,7,7,5,7,5,7,7,5,5,7,7,5,20,5,5]# the 20 is where it ends,  
    # hackish, but just matching the what generated the stimuli
    CS  = - (np.array(display) - 3)  

    return isi, CS, US

def stimulus_parameters(self_report): 

    colors  = [[-1,-1, 1],  # blue 
               [ 1,-1,-1]]  # red

    # set 
    # test_CB = int(self_report['subject_id'][1:3])) % 2
    # print test_CB, type(test_CB) 

    # set presentation order (of red and blue)
    cs  = [0,1,0,1,0,1,0,1][self_report['counter_balance']:] 
    iti = [5,5,5,5,5,5,5,5][self_report['counter_balance']:]
        
    print len(cs)
    cs_type = ['+', '-']        

    return cs, cs_type, colors, iti

def indices(isi, stimulus_length):
    # set indices for triggering biopac
    US_onset = - 1  # junk number -- any number not in timecourse
    stim_i = 0
    CS_onset = isi[stim_i]
    CS_offset = CS_onset + stimulus_length
    return US_onset, CS_onset, CS_offset, stim_i


def video_dimensions(video_path, fullscreen=0, x_size=1000, y_size=1000):
    """load movie onto background."""
    window = visual.Window([x_size, y_size], fullscr=fullscreen, units="pix", color=[1, 1, 1])
    movie = visual.MovieStim3(window, video_path, flipVert=False)
    window.mouseVisible = False
    return movie, window
