"""Call modules for three main segments of the experiment on day 1."""

import name_subject
import instructions
import stimuli
import exit_questions

# TO DO: fix this warning: Class SDLTranslatorResponder is implemented in both /Users/ssnl_booth2/anaconda/envs/experimental/lib/python2.7/site-packages/pygame/.dylibs/libSDL-1.2.0.dylib and /Library/Frameworks/SDL.framework/Versions/A/SDL. One of the two will be used. Which one is undefined.
# TO DO: fix this warning: User requested fullscreen with size [800 600], but screen is actually [1920, 1080]. Using actual size
# TO DO: fix this warning: pyo audio lib was requested but not loaded: ImportError('No module named pyo',)


subject_id = name_subject.new()


def run_subject(subject_id):
    """Run experiment for one subject."""
    #
    # TO DO: save self_report within instructions ..?
    self_report, window = instructions.run()

    """
    'instructions' presents slides stored in instructions/; subjects
    self administer shock at a level they decide and provide self-report of
    their experience, passed on in 'self_report'
    """

    # TO DO: fix bug with stimulus markers being sent to eyelink
    # TO DO: check biopac-gaze-video alignment across entire experiment
    # TO DO: make sure the laggy video is just processing speed
    window = stimuli.run(window, subject_id)

    """
    'video_module' presents stimuli of model undergoing fear conditioning and
    extinction; sends stimulus markers for US and CS to biopac and eyelink to
    align video + condition markers with gaze and physio data; records skin
    conductance and saves in neuroview; eyelink data saved in gaze_data/.
    """

    # TO DO: fix bug with color question -- it allows spaces as answers
    # TO DO: make sure we dont override previous subjects data
    exit_questions.run(window, self_report, subject_id)

    """
    'exit_questions' are taken from slides in 'instruction/'; results saved in
    'self_report_data/' along with self_report passed from 'instructions'.
    """


if __name__ == "__main__":
    run_subject(subject_id)
