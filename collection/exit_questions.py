"""Final behavioral questions before ending experiment on day one."""

from psychopy import visual, event
import keyboard_input as inputs
from numpy import save
from os import getcwd

questions = ['color', 'pain_other', 'pain_self_obs', 'relate', 'familiar', 'experimenter_id']


def run(win, self_report):
    """Ask exit questions, save data."""
    # mostly finished at this point.

    for Q_i in range(0, len(questions)):

        slide = '%s/instruction_slides/post%s.png' % (getcwd(), Q_i + 1)
        text = visual.ImageStim(win, image=slide)
        text.draw()
        win.flip()

        if Q_i == 0:
            # TO DO: fix this, it allows a space for an answer ...
            self_report['%s' % questions[Q_i]] = inputs.report_word(win, text)

        elif Q_i in [1, 2, 3, 4]:
            self_report['%s' % questions[Q_i]] = inputs.report_num(win, text)

        elif Q_i == 5:
            event.waitKeys()
            win.flip()
            text = visual.TextStim(win, text='')
            self_report['%s' % questions[Q_i]] = inputs.report_num(win, text)
            
    file_name = '%s/self_report_data/%s.npy' % (getcwd(), self_report['subject_id'])
    save(file_name, self_report)
    win.close()

    print '\n\nEXPERIMENT COMPLETED SUCCESSFULLY' 
