"""Collect design parameters."""

from psychopy import visual
import numpy as np


def intervals():
    """Set shock timing, stimulus length, waiting period before experiment."""
    shock_lag = 3
    stimulus_length = 4
    n_second_wait = 2
    return shock_lag, stimulus_length, n_second_wait


def design():
    """Define experimental structure that matches stimuli in video."""
    
    # isi = [3,5,7,5,7,7,5,7,7,5,5,5,5,7,5,7,5,5,7,5,7,5,7,5,7,5,7,5,5,7,7,5,7,7,5,7,5,7,7,5,5,7,7,5,7,5,7]
    # CS  = [0,1,1,0,0,1,0,1,0,0,1,0,1,0,1,1,0,1,0,0,1,0,1,1,0,1,0,0,1,0,1,1,0,0,1,0,1,0,1,1,0,1,1,0,0,0,1]
    # US  = [0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
   
    display  = [3,2,2,3,3,2,3,2,3,3,2,3,2,3,2,2,3,2,3,3,2,3,2,2,3,2,3,3,2,3,2,2,3,3,2,3,2,3,2,2,3,2,2,3,-1,-1,-1] # the last three are guesses
    US       = [0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    isi      = [3,5,7,5,7,7,5,7,7,5,5,5,5,7,5,7,5,5,7,5,7,5,7,5,7,5,7,5,5,7,7,5,7,7,5,7,5,7,7,5,5,7,7,5,7,5,7]
    
    # hackish, but just matching the what generated the stimuli
    CS  = - (np.array(display) - 3)  


    # CS = np.abs(np.array(CS)-1)
    return isi, CS, US

def stimulus_parameters(): 

    colors  = [[-1,-1, 1],  # blue 
               [ 1,-1,-1]]  # red

    # set presentation order (of red and blue)
    cs  = [0,1]  
    iti = [5,7]  
    
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
