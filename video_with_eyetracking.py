"""Module within 'experiment_main' for presenting video + signaling physio."""
# converting EDF files, converting "night", for example
# $ /Applications/Eyelink/EDF_Access_API/Example/edf2asc night.EDF
from psychopy import visual, core, event
import experiment_ports
import tracker_functions
import design_parameters as params  # my functions
import pylink

# set key for subjects to abort during experiment
exit_key = 'w'
# set time to wait for subjects' physiology to "settle"
wait_time = 0
# set time before CS that tracker should drift correct and/or reset
window_before_CS = 2
# set n_stimuli presented before the next drift correction
drift_interval = 3

def run(window, subject_id):
    """Present video, collect SCR data, trigger biopac during CS and US."""
    #
    # load parameters for timing and design of stimuli
    shock_lag, stim_length, wait_time = params.intervals()
    isi, CS, US = params.design()
    US_onset, CS_onset, CS_offset, stim_i = params.indices(isi, stim_length)

    # connect to eye tracker
    tracker = pylink.EyeLink('100.1.1.1')
    link = tracker_functions.eyelink(tracker, subject_id)
    link.eye_tracker_setup()

    # Open an EDF file to store gaze data -- name cannot exceeds 8 characters
    tracker.openDataFile(link.data_file_name)
    tracker.sendCommand("testing the combination of video with eye tracker")

    # set indices that will mark experimental conditions for the eye tracker
    tracker_onset, isi_count, frame_n, frame_t, time_i = link.indices(CS_onset)

    # set up monitors between eyelink and this computer
    window, movie = link.monitor_setup(window)
    frame_time = movie.getCurrentFrameTime

    # calibrate subjects
    link.calibration(tracker, window)

    # connect to biopac
    biopac = experiment_ports.biopac()

    # initiate biopack. set all to 0 except for "not experiment" channel
    biopac.initiate()

    # wait for a given interval so subjects physiological respones "settle"
    core.wait(wait_time)

    # begin experiment: recording physio data and presenting video
    biopac.begin()

    # start recording eyegaze
    link.initiate(tracker)

    # set time to zero and start
    time = core.Clock()
    time.reset()

    while time_i < 10:  # movie.status != visual.FINISHED:

        # draw next frame
        movie.draw()
        # update foreground
        window.flip()
        # update frame time
        frame_t = frame_time()
        # only catch first instance
        time_i = round(frame_t)

        # send time and position data to tracker for later visualization
        frame_n = link.align_frames(tracker, frame_t, frame_n, movie, time)

        # signal CS onset
        if (time_i == CS_onset):

            # signal CS type
            biopac.CS(CS[stim_i])

            # set next US
            if US[stim_i]:
                US_onset = CS_onset + shock_lag

            # update onset time to look for
            stim_i, CS_onset = next_CS(stim_i, isi, stim_length)
            tracker_onset = CS_onset - window_before_CS

        # signal US
        elif (time_i == US_onset):
            biopac.US()
            US_onset = -1
            tracker.sendMessage('US')

        # signal CS & US offset
        elif (time_i == CS_offset):
            # signal the biopac
            biopac.end_stim()
            # signal eye tracker
            tracker.sendMessage('END_CS')
            # update offset time to look for
            CS_offset = CS_onset + stim_length

        # drift correct with the eye tracker
        elif (time_i == tracker_onset):

            # reference time to correct for
            time_pause = time.getTime()
            # don't catch redundant onsets
            tracker_onset = -1

            # drift correct every so often
            if ((isi_count + 1) % drift_interval) == 0:

                movie, window = link.drift(tracker, movie, window)

            # message eye tracker the isi count
            tracker.sendMessage('TRIAL_ONSET_' + str(isi_count))

            # update clock to reflect time spent drift correcting
            time_unpause = time.getTime()
            time.add(time_unpause - time_pause)
            isi_count = isi_count + 1

        # collect key presses
        keyPressed = event.getKeys()
        # if exit key was pressed, end video
        if keyPressed:
            if keyPressed[0] == exit_key:
                break

    # end video, transfer eye_tracker data, close tracker and biopac
    link.close(tracker)
    biopac.end()

    return window


def next_CS(stim_i, isi, stimulus_length):
    """Tag locations of next CS, to align biopac markers with video."""
    stim_i = stim_i + 1
    next_CS = sum(isi[0:stim_i + 1]) + stim_i * stimulus_length

    return stim_i, next_CS
