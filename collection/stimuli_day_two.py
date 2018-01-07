"""Module within 'experiment' for presenting video + signaling physio."""

from psychopy import core, event, visual
import pylink, os, time, numpy

# in house functions
import experiment_ports
import tracker_functions
import design_parameters as params 

# set time to wait for subjects' physiology to "settle"
wait_time = 120
# delay before stimulus presentation, after instructions 
delay_time = 15
# set time to present each stimulus     
n_second_display = 4

def run(self_report, window):
    """Present video, collect SCR and gaze data, align with video."""
    
    # connect to eye tracker
    tracker = pylink.EyeLink('100.1.1.1')
    link = tracker_functions.eyelink(tracker, self_report['subject_id'])
    link.eye_tracker_setup()

    # Open an EDF file to store gaze data -- name cannot exceeds 8 characters
    tracker.openDataFile(link.data_file_name)
    tracker.sendCommand("day two of data collection")

    # set up monitors between eyelink and this computer
    window  = link.display_setup(window)

    # calibrate subjects, determine whether we're using their gaze data
    link.calibration(tracker, window, day=self_report['day'])

    # connect to biopac
    biopac = experiment_ports.biopac()

    # initiate biopack. set all to 0 except for "not experiment" channel
    biopac.initiate()

    # wait for a given interval so subjects physiological respones "settle"
    core.wait(wait_time)

    # begin experiment: recording physio data and presenting video
    biopac.begin()

    # load stimulus parameters 
    cs, cs_type, colors, inter_trial_interval = params.stimulus_parameters(self_report)  
    
    # wait to begin experiment, after instructions have ended 
    # core.wait(delay_time)

    # start recording eyegaze
    link.initiate(tracker)

    # begin stimulus presentation
    for i_stimulus in range(len(cs)): 

        # select and present next stimulus color
        i_color = colors[cs[i_stimulus]]
        present_stimulus(i_color, window, visual)
        
        # send CS info to biopac and eyetracker
        start_message = 'START_CS%s'%cs_type[cs[i_stimulus]]
        tracker.sendMessage(start_message)
        biopac.CS(cs[i_stimulus])

        # wait for stimulus presentation
        core.wait(n_second_display)

        # signal end to biopac and eyetracker
        end_message = 'END_CS%s'%cs_type[cs[i_stimulus]]
        tracker.sendMessage(end_message)
        biopac.end_stim()
        
        # clear screen and wait the duration of the iti 
        window.flip();
        core.wait(inter_trial_interval[i_stimulus])

    # end video, transfer eye_tracker data, close tracker and biopac
    link.close(tracker)
    biopac.end()
    self_report['CS'] = cs 
    self_report['isi'] = inter_trial_interval
    
    return self_report, window

# function to draw stimuli
def present_stimulus(rand_color, window, visual):
    square = visual.Rect(win=window, lineColor = rand_color, width=300, height=300, fillColor = rand_color)
    square.draw() 
    window.flip()

