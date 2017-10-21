"""Module within 'experiment_main' for presenting video + signaling physio."""
# converting EDF files, converting "night", for example
# $ /Applications/Eyelink/EDF_Access_API/Example/edf2asc night.EDF

from psychopy import core, event, visual
import experiment_ports
import tracker_functions
import design_parameters as params  # my functions
import pylink, os

# set key for subjects to pause during experiment
exit_key = 'w'
# set time to wait for subjects' physiology to "settle"
wait_time = 0
# set time before CS that tracker should drift correct and/or reset
window_before_CS = 2
# set n_stimuli presented before the next drift correction
drift_interval = 1


def run(self_report, window, subject_id):
    """Present video, collect SCR and gaze data, align with video."""
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

    # calibrate subjects, determine whether we're using their gaze data
    tracking, recalibration_trials = link.calibration(tracker, window)
    # tmp code, but this is what we need to present here

    # connect to biopac
    biopac = experiment_ports.biopac()

    # initiate biopack. set all to 0 except for "not experiment" channel
    biopac.initiate()

    # wait for a given interval so subjects physiological respones "settle"
    core.wait(wait_time)

    # begin experiment: recording physio data and presenting video
    biopac.begin()

    # start recording eyegaze
    if tracking:
        link.initiate(tracker)
        print('tracking = ', tracking)

    # set time to zero and start
    time = core.Clock()
    time.reset()

    while time_i < 30:  # movie.status != visual.FINISHED:
        # draw next frame
        movie.draw()
        # update foreground
        window.flip()
        # update frame time
        frame_t = frame_time()
        # only catch first instance
        time_i = round(frame_t)

        # send time and position data to tracker for later visualization
        if tracking:
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
            if tracking:
                tracker_onset = CS_onset - window_before_CS
                print('tracking = ', tracking)

        # signal US
        elif (time_i == US_onset):
            biopac.US()
            US_onset = -1
            if tracking:
                tracker.sendMessage('US')
                print('tracking = ', tracking)

        # signal CS & US offset
        elif (time_i == CS_offset):
            # signal the biopac
            biopac.end_stim()
            # update offset time to look for
            CS_offset = CS_onset + stim_length
            if tracking:
                # signal eye tracker
                tracker.sendMessage('END_CS')
                print('tracking = ', tracking)

        # drift correct with the eye tracker
        elif (time_i == tracker_onset):

            if tracking:
                # reference time to correct for
                time_pause = time.getTime()
                # don't catch redundant onsets
                tracker_onset = -1

                # drift correct every so often
                if ((isi_count + 1) % drift_interval) == 0:

                    movie, window, tracking = link.drift(tracker, movie, window)
                    recalibration_trials = recalibration_trials + 1
                    print('tracking = ', tracking)

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
            if (keyPressed[0] == 'e'):
                prompt = 'not using eyetracker during the experiment'
                notice = visual.TextStim(window, text=prompt, color='black', units='pix')
                notice.draw()
                window.flip()
                core.wait(1)
                tracking = 0
            elif (keyPressed[0] == 'q'):
                visual.FINISHED = 1


    # end video, transfer eye_tracker data, close tracker and biopac
    link.close(tracker)
    biopac.end()

    self_report['recalibration_trials'] = recalibration_trials
    self_report['finished_tracking'] = tracking

    return self_report, window


def next_CS(stim_i, isi, stimulus_length):
    """Tag locations of next CS, to align biopac markers with video."""
    stim_i = stim_i + 1
    next_CS = sum(isi[0:stim_i + 1]) + stim_i * stimulus_length

    return stim_i, next_CS
