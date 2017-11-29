"""Initiate experiment: Instructions, self-calibration, self-report."""

from psychopy import visual, core, event    # experimental presentation
import keyboard_input                       # collect keyboard inputs
import experiment_ports                     # connect to biopac + shockbox
from os import getcwd
import datetime

# set stimulus background and remove mouse visibility
monitor = 'testmonitor'
win = visual.Window(fullscr=1, monitor=monitor, units="pix", color=[1, 1, 1])
win.mouseVisible = False

def run(self_report):
    """Provide instructions."""
    
    # create empty dictionary for self report answers + time details
    begin = datetime.datetime.now()
    self_report['time'] = begin.strftime('experiment began at %H:%M on %m/%d/%Y')

    for iText in range(1,3):

        # load instructions
        text = '%s/instruction_slides/day2_intro%s.png' % (getcwd(), iText)
        # present instructions
        screen = visual.ImageStim(win, image=text)
        screen.draw()
        win.flip()
        # wait for key press to proceed
        event.waitKeys()

    win.flip()
    return self_report, win
