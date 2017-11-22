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
time_before_shock = 3
time_after_shock = 1

# open port for shock. must wait if used immediately, e.g. 'core.wait(2)'
SD9 = experiment_ports.SD9()

# set stimulus background and remove mouse visibility
monitor = 'testmonitor'
win = visual.Window([1500,800], fullscr=1, monitor=monitor, units="pix", color=[1, 1, 1])
win.mouseVisible = False


def run(self_report):
    """Provide instructions, self-calibration shock, and self-report."""
    
    # create empty dictionary for self report answers + time details
    begin = datetime.datetime.now()
    self_report['time'] = begin.strftime('experiment began at %H:%M on %m/%d/%Y')

    # mostly finished, aside from updating the slides

    for iText in range(1, 13):

        # load instructions
        text = '%s/instruction_slides/day1_intro%s.png' % (getcwd(), iText)

        # present instructions
        screen = visual.ImageStim(win, image=text)
        screen.draw()
        win.flip()

        # for simple instruction slides present text and wait for keypress
        if iText in [1, 2, 3, 4, 5, 11, 12]:
            event.waitKeys()

        # self calibration
        elif iText == 6:
            keyboard_input.calibrate(SD9, shock_key, finish_key)

        # subject is shocked at a "random" point at their chosen value
        elif iText == 7:
            event.waitKeys()
            win.flip()
            core.wait(time_before_shock)
            SD9.shock()
            core.wait(time_after_shock)

        # participants report their experience
        elif iText == 9:
            self_report['pain_self'] = keyboard_input.report_num(win, screen)

        # participants report their voltage
        elif iText == 10:
            self_report['voltage'] = keyboard_input.report_num(win, screen)

    
    win.flip()
    SD9.close()
    
    return self_report, win
