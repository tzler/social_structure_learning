"""Funtions to call the Eyelink 1000 using pylink."""

import os, pylink
import keyboard_input
from psychopy import visual, event, core
from eyelink_graphics import EyeLinkCoreGraphicsPsychoPy

class eyelink:

    def __init__(self, tracker, subject_id):
        """Initialize the Eyelink 1000 and set some initial parameters."""
        self.tracker = tracker # pylink.EyeLink('100.1.1.1')
        self.calibration_type = 'HV5'  # could also be H3, HV3, HV9, HV13
        self.screen_height = 1080
        self.screen_width = 1920
        self.sample_rate = 500
        self.data_folder = os.getcwd() + '/gaze_data/'
        self.data_file_name = subject_id + '.EDF'
        # variables to be loaded from in the script
        self.video_path = os.getcwd() + '/audio_visual/model_full.MP4'

    def eye_tracker_setup(self):
        """Set up the tracker."""
        # # # # # # # # # # # # # # # # #
        x = self.screen_width
        y = self.screen_height
        sample_rate = str(self.sample_rate)

        # we need to put the tracker in offline mode before we change its configrations
        self.tracker.setOfflineMode()
        # sampling rate
        self.tracker.sendCommand('sample_rate ' + sample_rate)
        # 0-> standard, 1-> sensitive [Manual: section ??]
        self.tracker.sendCommand('select_parser_configuration 0')
        # make sure the tracker knows the physical resolution of the subject display
        self.tracker.sendCommand("screen_pixel_coords = 0 0 %d %d" % (x - 1, y - 1))
        # stamp display resolution in EDF data file for Eyelink Data Viewer integration
        self.tracker.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (x - 1, y - 1))
        # Set the tracker to record Event Data in "GAZE" (or "HREF") coordinates
        self.tracker.sendCommand("recording_parse_type = GAZE")
        # specify the calibration type, H3, HV3, HV5, HV13 (HV = horiztonal/vertical)
        self.tracker.sendCommand("calibration_type = " + self.calibration_type)
        # allow buttons on the gamepad to accept calibration/dirft check target
        self.tracker.sendCommand("button_function 1 'accept_target_fixation'")
        # set link and file contents
        self.tracker.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
        self.tracker.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,INPUT")
        self.tracker.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,HREF,PUPIL,STATUS,INPUT,HTARGET")
        self.tracker.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,HREF,PUPIL,STATUS,INPUT,HTARGET")
        self.tracker.sendCommand('drift_correction_rpt_error 20.0')
        return

    def movie_setup(self, window):
        """Bring movie onto the monitor and connect with eyelink."""
        ## GET ACTUAL PARAMETERS FOR THESE
        scnWidth = self.screen_width
        scnHeight = self.screen_height

        window.mouseVisible = False
        # set up movie
        movie = visual.MovieStim3(window, self.video_path, flipVert=False)
        self.movie_x, self.movie_y = movie.size

        self.align_x = self.screen_width/2 - self.movie_x/2
        self.align_y = self.screen_height/2 - self.movie_y/2

        # callcustom calibrationmethod to coordinate screens
        screen_share = EyeLinkCoreGraphicsPsychoPy(self.tracker, window)
        pylink.openGraphicsEx(screen_share)
        
        frame_time = movie.getCurrentFrameTime
        # color theme of the calibration display
#        pylink.setCalibrationColors((255,255,255), (0,0,0))
        return window, movie, frame_time

    def display_setup(self, window):
        """Bring movie onto the monitor and connect with eyelink."""
        ## TO DO: GET ACTUAL PARAMETERS FOR THESE

        scnWidth = self.screen_width
        scnHeight = self.screen_height

        window.mouseVisible = False

        screen_share = EyeLinkCoreGraphicsPsychoPy(self.tracker, window)
        pylink.openGraphicsEx(screen_share)
#        pylink.setTargetSize(int(surf.get_rect().w/150), int(surf.get_rect().w/500)); 
        return window



    def align_frames(self, tracker, frame_time, frame_n, movie, time):
        """Send x & y coordinates to EYELINK for data visualization later."""
        # set path to video and and message
        path = '../audio_visual/short_trimmed.mp4'
        # determine time of current frame
        frame_current = movie.getCurrentFrameTime()
        # determine x and y coordinates
        x = self.align_x
        y = self.align_y

        # determine offset
        offset = int((frame_current - time.getTime()) * 1000)
        # send message to eyelink
        tracker.sendMessage("%d !V VFRAME %d %d %d %s" % (offset, frame_n, x, y, path))
        frame_n = frame_n + 1

        return frame_n


    def drift(self, tracker, mov, win):
        """Perform drift correction over paused video."""
        # take the tracker offline
        tracker.setOfflineMode()
        pylink.pumpDelay(50)
        stim = visual.GratingStim
        # set position coordinates
        x = win.size[0]/2
        y = win.size[1]/2
        # set next frame in background
        mov.draw()
        # create and present dot on background
        dot = stim(win, tex='none', mask='circle', size=18, color=[-1, 1, 1])
        dot.draw()
        # present background with overlayed fixation point
        win.flip()
      
        try:
            # setting the third value to zero preserves background image
            tracker.sendCommand('drift_correction_rpt_error 20.0')
            tracker.doDriftCorrect(x, y, 0, 0)
            message = tracker.getCalibrationMessage() 
            tracking = 1
        except:
            tracking = 0

        # start recording
        tracker.setOfflineMode()
        pylink.pumpDelay(50)
        tracker.startRecording(1, 1, 1, 1)
        pylink.pumpDelay(50) # wait for 100 ms to make sure data of interest is recorded

        return mov, win, tracking


    def calibration(self, tracker, window, day=1):
        """Provide instructions for calibration."""
        
        # set location for fixation cross
        x = window.size[0]/2
        y = window.size[1]/2         
        
        def display_instructions(i_text):
            text = '%s/instruction_slides/day%s_pre_video%s.png' %(os.getcwd(), day, i_text)
            screen = visual.ImageStim(window, image=text)
            screen.draw()
            window.flip()
            subject_response = event.waitKeys()[0]
            window.flip()
            return subject_response
       
        def practice_drift_correction():     
            time_before_dot = 2
            time_after_dot = 1
            window.flip() 
            core.wait(time_before_dot)
            tracker.doDriftCorrect(x,y,1,0)
            tracker_message = tracker.getCalibrationMessage() ; 
            window.flip() 
            core.wait(time_after_dot)
            return tracker_message 

        # prepare subject for calibration
        display_instructions(1) 
 
        def setup_tracker():
            # calibrate        
            tracker.doTrackerSetup()
            # prepare subjects for practice
            display_instructions(2)
            display_instructions(3)
            # go through practice drift correction
            try: 
              tracker_message = practice_drift_correction()
            except: 
              tracker_message = ''
            # prepare subjects for video
            subject_response = display_instructions(4)
            return subject_response[0], tracker_message
         
        setup_complete = 0 
        while setup_complete != '0':
            setup_complete, tracker_message = setup_tracker()

            try: 
                if int(setup_complete) in [3, 5, 9, 13]:   
                    self.calibration_type =  'HV%s' %setup_complete # default is 'HV9'  # could also be H3, HV3, HV5, HV13
                    self.tracker.sendCommand("calibration_type = " + self.calibration_type) 
            except: 
                pass 

        display_instructions(5)
        display_instructions(6)

        return tracker_message

    def indices(self, CS_onset):
        """Define indices to punctuate experiment."""
        tracker_onset = CS_onset - 2    # reset tracker before CS onset, recalibrate
        isi_count = 0                   #
        frame_n = 0                     # tracks
        frame_t = 0                     #
        time_i = 0                      #
        return tracker_onset, isi_count, frame_n, frame_t, time_i

    def close(self, tracker):
        """Close Eyelink, import data file, close graphics, close tracker."""
        tracker.setOfflineMode()
        file_name = self.data_file_name
        data_folder = self.data_folder
        tracker.receiveDataFile(file_name, data_folder + file_name)
        pylink.closeGraphics()
        tracker.close()

    def initiate(self, tracker):
        """Initiate Eyelink."""
        tracker.setOfflineMode()
        tracker.startRecording(1, 1, 1, 1)
