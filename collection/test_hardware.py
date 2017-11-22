from psychopy import visual, core, event
import numpy, random, serial, time, sys
import tracker_functions, experiment_ports, pylink

############ DESIGN PARAMETERS ###########
# set amount of time to display each color
nSecondDisplay = 4
# set time to display stimulus after shock -- within nSecondDesplay timeframe
openPause = 2 

keyboard_input = sys.argv[-1]



def SD9(): 
    
    print 'testing SD9'

    SD9 = experiment_ports.SD9()
    
    win = visual.Window([1000,1000], units="pix", color=[1,1,1])
    instructions = 'press space bar to shock, press enter whenever youre done :)'
    screen = visual.TextStim(win, text=instructions)
    screen.draw()
    win.flip()

    done = 0; 
    while not done:
      choice = event.waitKeys()[0]
      if choice == 'return': 
        done = 1
        SD9.close()
      elif choice == 'space':
        # print 'ouch!'
        SD9.shock()
      else: 
        pass 

    # core.wait(2)
    win.close()
    
def biopac():
    
    print 'TESTING BIOPACK'
    
    nTrace = 1
    # open port for shock. must wait if used immediately, e.g. 'core.wait(2)'#
    SD9 = experiment_ports.SD9() ; 
    SD9.close()

    # connect to biopac
    biopac = experiment_ports.biopac()

    # initiate biopack. set all to 0 except for "not experiment" channel
    biopac.initiate()

    # colors to choose from this pallet
    colors  = [[ 1, 1, 1],  # white
              [ 0, 0, 0],  # grey?
              [-1,-1, 1],  # blue
              [ 1,-1,-1]]  # red
    red     = [ 1,-1,-1]   # this will be for clarity below

    # set presentation order (of red and blue) + when to shock

    display  = [3,2]
    aversive = [1,0]
    iti      = [5,7,5]

      # hackish incorporation of new and old code
      # we want to have a vector with 0s for the CS+ and 1s for the CS-
      # and not signal the first stimulus, which is just for alignment 
    CS  = - (numpy.array(display) - 3) ; 

    # set background for conditioning
    background = visual.Window([1920, 1080], fullscr=1, monitor="testMonitor", units="pix", color = colors[0])
    background.mouseVisible = False

    # begin presentation and wait a few seconds
    background.flip()
    core.wait(openPause)

    # begin experiment: recording physio data and presenting video
    biopac.begin()

    ### begin presentation and start recording
    for iStimulus in range(0,len(display)):
        
        core.wait(iti[iStimulus])

        # choose which color to use for presentation
        randColor = colors[display[iStimulus]]
        # create stimulus
        square = visual.Rect(win=background, lineColor = randColor, width=300, height=300, fillColor = randColor)
        # draw square on back image
        square.draw()
        background.flip()
    
        biopac.CS(CS[iStimulus]) 
    
        if aversive[iStimulus]: SD9.open()  
        # hold stimulus on screen
        core.wait(nSecondDisplay-nTrace)

        # shock if it's red and pseudorandom probability
        if aversive[iStimulus]:
            SD9.shock(); SD9.close()
            biopac.US()

        # keep stimulus on screen for nTraces then terminate signal to biopac
        core.wait(nTrace)
        biopac.end_stim()

        # clear screen and wait the duration of the iti + noise
        background.flip()
    
    # cleanup
    event.waitKeys()    
    SD9.close()
    biopac.end()
    background.close()

 
def eyelink(): 
    
    print 'testing eyelink'
    subject_id = 'TEST'
    
    window = visual.Window([1920, 1080], fullscr=1, monitor="testMonitor", units="pix", color = [1,1,1])
    window.mouseVisible = False

   
    # connect to eye tracker
    tracker = pylink.EyeLink('100.1.1.1')
    link = tracker_functions.eyelink(tracker, subject_id)
    link.eye_tracker_setup()

    # Open an EDF file to store gaze data -- name cannot exceeds 8 characters
    tracker.openDataFile(link.data_file_name)
    tracker.sendCommand("testing the combination of video with eye tracker")

    # set up monitors between eyelink and this computer
    window, movie, frame_time = link.movie_setup(window)

    # connect to biopac
    biopac = experiment_ports.biopac()

    # initiate biopack. set all to 0 except for "not experiment" channel
    biopac.initiate()

    # begin experiment: recording physio data and presenting video
    biopac.begin()
    
    # calibrate subjects
    link.calibration(tracker, window)


def test_all_hardware():
    
    print '\n\n\nTESTING ALL HARDWARE SUB-ROUTINES'
    SD9()
    biopac()
    eyelink()

if __name__ == "__main__":

  if __file__ == keyboard_input: 
      test_all_hardware()  
  else: 
      eval('%s()'%keyboard_input)

