"""Call modules for three main segments of the experiment on day 1."""

import name_subject
import instructions
import stimuli
import exit_questions
from psychopy import visual

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TO DO: work on alignment                                                      #
# TO DO: which  video should we use?                                            #
# TO DO: switch CSs in design parameters so it triggers the biopac correctly    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

self_report = {'day':1}
# name subject from command line argument, else autoname and pass error
self_report = name_subject.new(self_report) 

# set stimulus background and remove mouse visibility
window = visual.Window([1920, 1080], fullscr=1, monitor='testmonitor', units="pix", color=[1, 1, 1]) ; window.mouseVisible = False

def run_subject(self_report, window):
    """Run experiment for one subject."""

    self_report, window = instructions.run(self_report, window)

    """
    'instructions' presents slides stored in instructions/; subjects
    self administer shock at a level they decide and provide self-report of
    their experience, passed on in 'self_report'
    """

    self_report, window = stimuli.run(self_report, window)

    """
    'video_module' presents stimuli of model undergoing fear conditioning and
    extinction; sends stimulus markers for US and CS to biopac and eyelink to
    align video + condition markers with gaze and physio data; records skin
    conductance and saves in neuroview, eyelink data saved in gaze_data/.
    """

    exit_questions.run(window, self_report)

    """
    'exit_questions' are taken from slides in 'instruction/'; results saved in
    'self_report_data/' along with self_report passed from 'instructions'.
    """


if __name__ == "__main__":
    run_subject(self_report, window)


# TO DO: fix this warning: Class SDLTranslatorResponder is implemented in both /Users/ssnl_booth2/anaconda/envs/experimental/lib/python2.7/site-packages/pygame/.dylibs/libSDL-1.2.0.dylib and /Library/Frameworks/SDL.framework/Versions/A/SDL. One of the two will be used. Which one is undefined.
# TO DO: fix this warning: User requested fullscreen with size [800 600], but screen is actually [1920, 1080]. Using actual size
# TO DO: fix this warning: pyo audio lib was requested but not loaded: ImportError('No module named pyo',)
# TO DO: figure out day two: video recorder to see if they check their hands
