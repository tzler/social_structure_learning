
# things things 
import numpy as np 
import os, csv
from sklearn.cluster import KMeans as kmeans
import matplotlib.pyplot as plt

def load_data(subject_id, day=1, listen=0): 
    """inputs: 'day' = int [1 OR 2]
    returns a list of all subjects in gaze directory matching 'day'"""

    data_file_names = []
    data_path = '../../../collection/gaze_data/'
    folder_contents = os.listdir(data_path)
    folder_contents.sort()

    for file in folder_contents: 
        if 'd%s.asc'%day in file and not 'x' in file: 
            data_file_names.append(file)
                
    for file_name in data_file_names: 
        if subject_id in file_name: 
            subject_path = data_path + file_name
            if listen: print("loading data from subject'%s'"%file_name) 

    with open(subject_path) as f:
        reader = csv.reader(f, delimiter="\t")
        subject_data = list(reader)

    return subject_data

def extract_data(subject_data): 
    """ 
    inputs: 'subject_data' = raw ascii file 
    returns: np.arrays for pupil, CS+, CS-, US, and movie_frame information 
    
    """

    _pupil_ = [] 
    onsets  = []
    cs_type = []
    xy = []
    cs_pos = []; cs_p = 0 # CS+
    cs_neg = []; cs_n = 0 # CS-
    us_sti = []; us_o = 0 # US

    # movie frame data prep 
    m_frame, i_frame = [], np.nan

    for i_row in range(len(subject_data)): 

        msg = subject_data[i_row]  

        try: 
            int(subject_data[i_row][0])
            # 3 = pupil column
            datum = float(msg[3]) 
            _pupil_.append(datum)
            cs_pos.append(cs_p)
            cs_neg.append(cs_n)
            us_sti.append(us_o)
            m_frame.append(i_frame)
            
            # extract xy coordinates 
            if ' .' in msg[1] or ' .' in  msg[2]:
                xy.append([np.nan, np.nan])
            else: 
                xy.append([float(msg[1]), float(msg[2])])
            
        except: 

            if len(msg) > 1: 
                if 'CS+' in msg[1]: cs_p = 1
                if 'CS-' in msg[1]: cs_n = 1
                if 'US'  in msg[1]: 
                    us_o = 1
                    cs_type[-1] =  cs_type[-1] + 'US'
                    
                    
                if 'OFF' in msg[1]: 
                    cs_p = 0
                    cs_n = 0
                    us_o = 0 

                if msg[0] == "MSG": 

                    if "VFRAME" in msg[1]: 

                        ind = str.find(msg[1], "VFRAME")
                        space = str.find(msg[1], " 0 0 /")
                        if space == -1: space = str.find(msg[1], " 0 0 ../")
                        i_frame = int(msg[1][ind+7:space])
                    
                    if "TRIAL_ONSET" in msg[1]:
                        onsets.append(len(_pupil_))
                        cs_type.append(msg[1][-3:])
                    
                        
    
    data = {"pupil":np.array(_pupil_), 
            "CS+":np.array(cs_pos), 
            "CS-":np.array(cs_neg), 
            "US":np.array(us_sti), 
            "movie_frame":np.array(m_frame),
            "xy":np.array(xy), 
            "onsets":np.array(onsets),
            "cs_type":cs_type}
                    

    return data


def kmeans_coordinates(xy, with_image=0): 
    
    if with_image: a = 1
    else: a = - 1
    
    # ignore nans, flip (?) y axis, fit model
    keep_inds = xy[:,0] == xy[:,0]
    xy = xy[keep_inds] 
    # correct for inversion depending on image type
    xy[:,1] = a*xy[:,1]
    k = kmeans(n_clusters=3, random_state=0).fit(xy)
    
    return k, xy


def generate_clusters(subjects, show=1):
    
    big_picture = 0
    
    cluster_data = {}
    

    model_image = plt.imread('model_image.png')
    
    # colors, shape
    colors = ['#00ccff', '#ff00ff', '#00ffaa'] #6600ff'] 
    y_len, x_len, _ = np.shape(model_image)
    cluster_data['image_dims'] = {'x_len':x_len, 'y_len':y_len}
    
    # fits gaze data to arbitrary jpeg
    scale_= 1.8
    shift_ = 0 # 200
    
    if show: plt.figure(figsize=[15, 12])

    for i_subject in range(len(subjects)):
        
        subject_name = subjects[i_subject]

        # get subject's data
        subject_data = load_data(subject_name)
        data = extract_data(subject_data)
        
        # generate clusters
        k, xy = kmeans_coordinates(data['xy'], with_image=1)
        
        # save 
        cluster_data['%s'%subject_name] = {'data':data, 'k':k, 'xy':xy}
        
        if show: 
            
            # find data to color mapping
            point_colors = [colors[ii] for ii in k.labels_]
            # setup plot
            plt.subplot(2,2,i_subject+1); plt.axis('off')
            # show background experimental stimuli
            plt.imshow(model_image, alpha=.1)
            # plot gaze data according to cluster color
            plt.scatter(xy[:,0]*scale_-shift_,xy[:,1]*scale_-shift_,  alpha=.01, c = point_colors)
            # extract centers of mass for each cluster
            centers = np.round(k.cluster_centers_)

            # plot center of mass for each cluster in a way we can clearly lable in legend
            for i_loc in range(len(centers)):
                plt.scatter(centers[i_loc][0]*scale_-shift_, centers[i_loc][1]*scale_-shift_, s=250, c='k')
                plt.scatter(centers[i_loc][0]*scale_-shift_, centers[i_loc][1]*scale_-shift_, 
                            s=180, c=colors[i_loc], label='center of mass\n  cluster_%s'%i_loc)
                plt.annotate(i_loc, xy=(centers[i_loc][0]*scale_-shift_, centers[i_loc][1]*scale_-shift_), 
                             xytext=(-4, -4), textcoords='offset points', alpha=1, fontsize=11)

            # control aesthetics
            if not big_picture: 
                plt.xlim([0, x_len]), 
                plt.ylim([y_len, 0])
            plt.legend(); ax = plt.gca(); ax.legend(fontsize = 6+1, loc=3)
            plt.title("\nsubject %s \nexperimental average from centers of mass: %.02f pixels\n" 
                      %(subjects[i_subject], np.sqrt(k.inertia_/len(xy)) ) )

    
    return cluster_data



