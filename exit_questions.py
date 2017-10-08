"""Final behavioral questions before ending experiment on day one."""

from psychopy import visual, event
import keyboard_input as inputs
from numpy import save
from os import getcwd

questions = ['color', 'pain_other', 'pain_self_obs', 'relate', 'familiar', 'exit']


def run(win, self_report, subject_id):
    """Ask exit questions, save data."""
    # mostly finished at this point.

    for Q_i in range(0, len(questions)):

        text = '%s/instruction_slides/post%s.png' % (getcwd(), Q_i + 1)
        screen = visual.ImageStim(win, image=text)
        screen.draw()
        win.flip()

        if Q_i == 0:
            # TO DO: fix this, it allows a space for an answer ...
            self_report['%s' % questions[Q_i]] = inputs.reportWord(win, screen)

        elif Q_i in [1, 2, 3, 4]:
            self_report['%s' % questions[Q_i]] = inputs.reportNum(win, screen)

        elif Q_i == 5:
            file_name = '%s/self_report_data/%s.npy' % (getcwd(), subject_id)
            save(file_name, self_report)
            event.waitKeys()

    win.flip()
    event.waitKeys()
    win.close()
    print self_report
