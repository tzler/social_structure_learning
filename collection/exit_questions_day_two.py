"""Final behavioral questions before ending experiment on day one."""

from psychopy import visual, event
import keyboard_input as inputs
from numpy import save
from os import getcwd

questions = ['which_color','prob_red', 'prob_blue', 'feel_red','feel_blue','feel_ayer','believe_ayer', 'experimenter_id']

def run(win, self_report):
    """Ask exit questions, save data."""
    # mostly finished at this point.

    for Q_i in range(len(questions)):

        slide = '%s/instruction_slides/day2_post_video%s.png' % (getcwd(), Q_i + 1)
        text = visual.ImageStim(win, image=slide)
        text.draw()
        win.flip()
        
        if Q_i < 7: 
            self_report['%s' % questions[Q_i]] = inputs.report_num(win, text)
        else: 
            event.waitKeys()
            win.flip()
            text = visual.TextStim(win, text='')
            self_report['%s' % questions[Q_i]] = inputs.report_num(win, text)



    file_name = '%s/self_report_data/%s.npy' % (getcwd(),self_report['subject_id']) 
    save(file_name, self_report)
    win.close()
    
    print '\n\nEXPERIMENT COMPLETED SUCCESSFULLY'
