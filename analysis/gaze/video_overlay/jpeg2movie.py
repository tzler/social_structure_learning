

import os
import numpy as np

class FramePathServer():
    
    ''' This provides time-based path names from a folder of frame-images. '''
    
    def __init__(self,
		folder_path,
		frame_rate=np.float(30.),
                start_time=np.float(0),
		file_type='.jpg'):
        
        self.start_time = np.float(start_time) # offset for time marks
        self.fps = np.float(frame_rate) # frames per second
        self.folder_path = folder_path # folder that the images come from
        
        # read in file names from the folder that the path is pointing to, only
        # keep the ones that end on .png (or other specified format)
        #os.chdir(self.folder_path)
        self.file_paths = [file for file in os.listdir(self.folder_path)
            if file.endswith(file_type)]
        self.file_paths.sort()
        
        print 'Folder path:', self.folder_path
        self.num_frames = len(self.file_paths)
        print 'Number of frames:', self.num_frames
                
    def return_path(self,time):
        
        ''' returns the path to the last frame just before the time passed as 
        an argument '''
        
        frame_time = time + self.start_time
        last_frame_num = np.mod(np.floor(frame_time*self.fps),
                                self.num_frames)
        if last_frame_num < 0: last_frame_num = 0
        
        return os.path.join(self.folder_path,
                            self.file_paths[np.int(last_frame_num)])

if __name__ == "__main__":
    
    server = FramePathServer(
        '/Users/biota/Desktop/sSL/experiment_2/analysis/gaze/video_overlay/jpeg2movie_folder/')
    
    # These two lines check for basic functionality
    print len(server.file_paths)
    print server.return_path(90)





