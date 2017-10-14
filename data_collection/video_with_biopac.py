"""Module within 'experiment_main' for presenting video + signaling physio."""

from psychopy import visual, core, event
import design_parameters as params
import experiment_ports, os

video_path = '%s/audio_visual/model_short.mp4' % os.getcwd()


def run(window):
    """Present video, collect SCR data, trigger biopac during CS and US."""
    # load parameters for timing and design

    shock_lag, stim_length, wait_time = params.intervals()
    isi, CS, US = params.design()   # ISIntervals, CS, and US markers
    US_onset, CS_onset, CS_offset, stim_i = params.indices(isi, stim_length)

    # set video dimensions
    movie = visual.MovieStim3(window, video_path, flipVert=False)
    # define key press to abort
    exit_key = 'w'

    # connect to biopac
    biopac = experiment_ports.biopac()
    # initiate biopack. set all to 0 except for "not experiment" channel
    biopac.initiate()
    # wait for a given interval so subjects physiological respones "settle"
    core.wait(wait_time)

    # begin experiment: recording physio data and presenting video
    biopac.begin()

    time_i = 0
    while time_i < 30:  # movie.status != visual.FINISHED:

        # draw next frame
        movie.draw()
        # update foreground
        window.flip()
        # get current time in video -- round so we only capture first instance
        time_i = round(movie.getCurrentFrameTime())

        # signal CS onsetn -- only works with whole numbers at this point
        if (time_i == CS_onset):

            # signal CS type
            biopac.CS(CS[stim_i])

            # set next US
            if US[stim_i]:
                US_onset = CS_onset + shock_lag

            # update onset time to look for
            stim_i, CS_onset = next_CS(stim_i, isi, stim_length)

        # signal US
        elif (time_i == US_onset):
            biopac.US()
            US_onset = -1

        # signal CS & US offset
        elif (time_i == CS_offset):
            # signal the biopac
            biopac.end_stim()
            # update offset time to look for
            CS_offset = CS_onset + stim_length

        # collect key presses
        keyPressed = event.getKeys()
        # if exit key was pressed, end video
        if keyPressed:
            if keyPressed[0] == exit_key:
                break

    # signal the end to experimental channel
    biopac.end()
    return window


def next_CS(stim_i, isi, stimulus_length):
    """Tag locations of next CS, to align biopac markers with video."""
    stim_i = stim_i + 1
    next_CS = sum(isi[0:stim_i + 1]) + stim_i * stimulus_length
    return stim_i, next_CS
