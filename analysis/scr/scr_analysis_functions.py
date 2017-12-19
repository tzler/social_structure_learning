"""Functions to load raw SCR data, extract the design structure, calculate amplitudes."""

import numpy as np
import pandas
import os

# let's turn off these error messages : https://tinyurl.com/ybduhkh3
pandas.options.mode.chained_assignment = None

def loadData(path2data):
    """ 
    Load BIOPAC data converted to .txt files. Returns: 
    rawData[iSubject][iDay][:,iChannel], where 
    iChannel [0,1,2,3] are [scr, cs+, cs-, us] respectively 
    """ 

    rawData = []
    tmpFiles = os.listdir(path2data)[1:-1]
  
    for iFile in range(0, len(tmpFiles)/2):
        
        if 's_' in tmpFiles[ iFile * 2 ]: 
            print "loading data for",tmpFiles[iFile * 2][0:4]
            tmp1 = pandas.read_csv('%s/%s'%(path2data,tmpFiles[ iFile * 2  ]), sep=',',header=None)
            tmp2 = pandas.read_csv('%s/%s'%(path2data,tmpFiles[iFile *2 + 1]), sep=',',header=None)
            rawData.append([tmp1.values, tmp2.values])
  
    return rawData
    

def nonZero(x): 
  """Make the code cleaner below"""
  return np.nonzero(x)[0]



def stimulus_markers(CS):
    """Generate list of timepoints for stimuli onset and offset."""
                
    # delta marks transitions to and from a CS
    compareA = np.append(nonZero(CS),nonZero(CS)[-1])
    compareB = np.append(nonZero(CS)[0],nonZero(CS))
    delta = compareA - compareB
      
    # identify stimulus onsets 
    on = np.zeros(len(CS))
    on[compareA[nonZero(delta > 1)]] = 1
    on[compareA[0]] = 1
    # identify stimulus offsets
    off= np.zeros(len(CS))
    off[compareA[nonZero(delta > 1)-1]] = 1
    off[compareA[-1]] = 1
      
    return nonZero(on), nonZero(off)


def design(raw_data):
    """Create a data frame with the structure and time indices of experimental stimuli."""    
    
    nSubjects = len(raw_data)
    all_subjects_design = {}
    
    for iSubject in range(0,nSubjects): 
        
        # determine the design on each day and concatenate the two
        design_day1 = extract_design(raw_data[iSubject],0)
        design_day2 = extract_design(raw_data[iSubject],1);
        design_full = pandas.concat([design_day1, design_day2])

        # clean up the fata frame
        design_full = design_full.reset_index() # range(0,len(design_full['CS+']))
        design_full.index.name = 'trial_number' # #    design_full.index += 1 ; 
        design_full['Day'] -= 1 # again, annoying, but because of the concatenation
        all_subjects_design[iSubject] = design_full

    return all_subjects_design


def extract_design(subject_data, day): 
    
    # identify positive and negative onsets across experiment -- only using onsets
    pos_onsets, null = stimulus_markers(subject_data[day][:,1])
    neg_onsets, null = stimulus_markers(subject_data[day][:,2])    
            
    # concatenate into a list and order 
    all_onsets = np.sort(np.concatenate([pos_onsets,neg_onsets]))
        
    # prepare to find amplitudes for each CS
    scr = subject_data[day][:,0]
    scr_amp = np.zeros(len(all_onsets))
    
    # create placeholders
    CS_pos = np.zeros(len(all_onsets))
    CS_neg = np.zeros(len(all_onsets))
    US    = np.zeros(len(all_onsets))

    # set markers for CS+ or CS- in design 
    for iOnset in range(0,len(all_onsets)): 
                
        CS_pos[iOnset] = all_onsets[iOnset] in pos_onsets
        CS_neg[iOnset] = all_onsets[iOnset] in neg_onsets
        scr_amp[iOnset] = amplitude(scr, all_onsets[iOnset])
    

    # create a data frame with CS+, CS-, US, and the day
    structure = {'US':US, 'CS+': CS_pos, 'CS-':CS_neg, 'SCR_amp':scr_amp, 'Day':np.repeat(day+1,len(all_onsets))}
    structure = pandas.DataFrame(structure) ; 

    # create column of indices for where event occured in scr timecourse         
    structure['CS_index'] = np.zeros(len(structure["CS+"]))
    structure['CS_index'][structure['CS+'] == 1] = pos_onsets 
    structure['CS_index'][structure['CS-'] == 1] = neg_onsets 
    structure['US_index'] = np.zeros(len(structure["US"]))

    # on day one, fill in the locations for the US
    if day == 0: 

        # identify locations for the US in the timecourse of the experiment
        us_onsets, us_offsets = stimulus_markers(subject_data[day][:,3]) 

        # extract time of onset nearst to each US            
        for eachUS in range(0,len(us_onsets)): 

            # find condition nearest to each US
            difference = abs(all_onsets - us_offsets[eachUS])
            # align timecourse differences with design placeholder 
            US[np.nonzero(difference == min(difference))[0]] = 1
            
            # TO DO: also calculate amplitude here

        structure['US'] = US
        structure['US_index'][structure['US'] == 1] = us_onsets 

    return structure

def amplitude(subject_timecourse,onset): 
    """Find SCR amplitude from the onset of a CS over a given interval."""

    initial_delay = 1                             # length of wait time after onset
    interval_length = 4.5                         # length of interval to search over
    interval_length = int(interval_length * 1000) # convert to ms
    onset = onset + initial_delay * 1000          # convert to ms 
    
    # define interval to search over + find max value and index 
    max_interval = subject_timecourse[onset: onset + interval_length]
    max_index = onset + max_interval.argmax()
    max_value = subject_timecourse[max_index]

    # define interval from onset to max + find min index and value
    min_interval = subject_timecourse[onset:max_index+1] # "+ 1" in case onset is the maximum
    min_index = onset + min_interval.argmin()
    min_value = subject_timecourse[min_index]
    
    # return max_interval, max_index, max_value, min_interval, min_index, min_value for debugging/visualization
    return max_value - min_value


