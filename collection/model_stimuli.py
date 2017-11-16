from psychopy import visual, core, event
import numpy, random, serial, time
import experiment_ports

############ DESIGN PARAMETERS ###########
# set amount of time to display each color
nSecondDisplay = 4
# set time to display stimulus after shock -- within nSecondDesplay timeframe
nTrace = 1 
# set opening pause time
openPause = 0
###########################################

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
red     =  [ 1,-1,-1]   # this will be for clarity below

# set presentation order (of red and blue) + when to shock

display  = [1,3,2,2,3,2,3,3,2,3,3,2,3,2,3,2,2,3,2,3,3,2,3,2,2,3,2,3,3,2,3,2,2,3,3,2,3,2,3,2,2,3,2,2,3]
aversive = [0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
iti      = [3,5,7,5,7,7,5,7,7,5,5,5,5,7,5,7,5,5,7,5,7,5,7,5,7,5,7,5,5,7,7,5,7,7,5,7,5,7,7,5,5,7,7,5,7,5,7]

  # hackish incorporation of new and old code
  # we want to have a vector with 0s for the CS+ and 1s for the CS-
  # and not signal the first stimulus, which is just for alignment 
CS  = - (numpy.array(display) - 3) ; CS[0] = -1 

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
    core.wait(iti[iStimulus])

# cleanup
SD9.close()
biopac.end()
background.close()
