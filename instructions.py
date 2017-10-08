"""Initiate experiment: Instructions, self-calibration, self-report."""

from psychopy import visual, core, event    # experimental presentation
import keyboard_input                       # collect keyboard inputs
import experiment_ports                     # connect to biopac + shockbox
from os import getcwd
import datetime

"""           We need to update the instruction slides ...         """


# define keys to administer shock and finish calibration
shock_key = 'space'
finish_key = 'return'

# timing for white screen around final shock in the absence of control.
time_before_shock = 1
time_after_shock = .2

# create empty dictionary for self report answers + time details
self_report = {}
begin = datetime.datetime.now()
self_report['time'] = begin.strftime('experiment began at %H:%M on %m/%d/%Y')

# open port for shock. must wait if used immediately, e.g. 'core.wait(2)'
SD9 = experiment_ports.SD9()

# set stimulus background and remove mouse visibility
monitor = 'testmonitor'
win = visual.Window(fullscr=1, monitor=monitor, units="pix", color=[.5, .5, .5])
win.mouseVisible = False


def run():
    """Provide instructions, self-calibration shock, and self-report."""
    # mostly finished, aside from updating the slides

    for iText in range(1, 14):

        # load instructions
        text = '%s/instruction_slides/slide%s.png' % (getcwd(), iText)

        # present instructions
        screen = visual.ImageStim(win, image=text)
        screen.draw()
        win.flip()

        # for simple instruction slides present text and wait for keypress
        if iText in [1, 2, 3, 4, 5, 6, 11, 12, 13]:
            event.waitKeys()

        # self calibration
        elif iText == 7:
            keyboard_input.calibrate(SD9, shock_key, finish_key)

        # subject is shocked at a "random" point at their chosen value
        elif iText == 8:
            event.waitKeys()
            win.flip()
            core.wait(time_before_shock)
            SD9.shock()
            core.wait(time_after_shock)

        # participants report their experience
        elif iText == 9:
            self_report['pain_self'] = keyboard_input.reportNum(win, screen)

        # participants report their voltage
        elif iText == 10:
            self_report['voltage'] = keyboard_input.reportWord(win, screen)

    SD9.close()
    win.flip()

    return self_report, win
