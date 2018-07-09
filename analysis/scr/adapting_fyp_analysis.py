from matplotlib.mlab import find
from matplotlib.pyplot import * 
import scipy.signal as signal
import numpy as np
import pandas
import os
from pandas import read_csv

class experimental(object):  
    def __init__(self, path2data):    
        
        # loadData configs
        self.path2data = path2data
        self.day = 1
	self.US = 2 - self.day
	self.initial_cutout = 0 # 200000
        # transformData configs
        self.showTransform = 0 
        self.keepEdgeBefore = 0 #
        self.keepEdgeAfter = 0
        self.filterOrder = 2 
        self.lowPassCutoffFrequency = 0.00001
        self.hightPassCutoffFrequency = .0005
        self.windowstart = 1
        self.nSeconds = 4.5
	
    def loadData(self): 
        
        count = 0
        raw_data = {}
        subjectNames = []
        data_path = self.path2data
        files = os.listdir(data_path)
        files.sort()
        unique_ids = np.unique([files[ii][1:3] for ii in range(len(files))]);
        
        for _id_ in unique_ids:
            # find indices of each unique number--e.g. subject
            subject_inds = np.nonzero([str.find(files[ii], _id_) == 1 for ii in range(len(files))])[0]
            # only include those subjects who have two days of data
    
            if len(subject_inds) == 2:
    
                _raw_data_ = []
    
                for day in subject_inds:            
                    if 'd%s'%self.day in files[day]: 
                        _day_ = read_csv('%s/%s'%(data_path,files[day]), sep=',',header=None)
                        subjectNames.append(files[day])
                        _raw_data_ = _day_.values
                        _raw_data_ = _raw_data_[_raw_data_[:,4] == 0]
                        raw_data[count] = _raw_data_[:, 0:4]
                        count = count + 1
    
        self.nSubjects = len(subjectNames)
	self.subjectNames = subjectNames
        self.rawData = raw_data

    def transformData(self): 
        
        transformedData = []
        rawData = self.rawData
        self.rawDataCut = []
        
        for iSubject in range(0,self.nSubjects):

            temp = rawData[iSubject][:,0]
            self.rawDataCut.append(temp)
		
            # First, design the Buterworth filter to extract lowest frequency variation - a better mean, basically, to subtract
            N1  = self.filterOrder   
            Wn1 = self.lowPassCutoffFrequency
            B, A = signal.butter(N1, Wn1, output='ba') 
            # extract low frequency fluctuations
            lowFreq = signal.filtfilt(B,A, temp)

            # extract the frequency range of likely motion artifacts
            N2  = self.filterOrder   
            Wn2 = self.hightPassCutoffFrequency # Cutoff frequency
            B2, A2 = signal.butter(N2, Wn2, output='ba') 
            # apply 
            belowHighFreq = signal.filtfilt(B2,A2, temp)
            filteredData = belowHighFreq-lowFreq
            
            # zscore the filtered data
            filteredData = (filteredData-np.mean(filteredData))/np.std(filteredData)
            #transformedData.append([filteredData,rawData[iSubject][onset:offset,1:(3+self.US)]])
            # this isn't necessary any more now that we have a marker for experiment on and off we're using above
            transformedData.append([filteredData,rawData[iSubject][:,1:(3+self.US)]])


            if self.showTransform: 
                figure(figsize=(20,5))
                plot(temp, 'xkcd:blue',alpha=.4, linewidth=5)
                plot(lowFreq, 'r-',alpha=.3,linewidth=5)
                plot(belowHighFreq,'indigo',linewidth=3,alpha=.7)
                legend(['Original','low pass filtered','high pass filtered'])
                figure(figsize=(20,3))
                ylim([min(filteredData)-.25,max(filteredData)+.25]); 
                xlim([0,len(filteredData)])

                plot(filteredData,'indigo',linewidth=3,alpha=.7,color='xkcd:blue')
                title('standard deviation = %s > .1\nKEEPING SUBJECT'% (np.std(belowHighFreq-lowFreq)))

        self.transData = transformedData
    
    def logTransform(self,plus,minus):         
        plus[plus<=0] = 0 
        minus[minus<=0] = 0 
        plus = log(1+plus)
        minus = log(1+minus)
        return plus,minus
               
    def preprocessData(self): 
        self.loadData()
        self.transformData()
        
    def stimuli(self, CS): 
    
	marks   = np.convolve(CS, [1,-1])
   	onsets  = np.nonzero(marks > 0)[0]
   	offsets = np.nonzero(marks < 0)[0]
    
    	return onsets, offsets 

    def old_stimul(self,CS): 
        compareA = np.append(find(CS),find(CS)[-1])
        compareB = np.append(find(CS)[0],find(CS))
        delta = compareA-compareB

        # stimulus on 
        on = np.zeros(len(CS))
        on[compareA[find(delta>1)]] = 1
        on[compareA[0]] = 1

        # stimulus off
        off= np.zeros(len(CS))
        off[compareA[find(delta>1)-1]] = 1
        off[compareA[-1]] = 1
        return find(on), find(off)
    
    def amplitudeDifference(self,inputData,iStim,stimLocation,show=0): 
        p1 = np.zeros(self.nSubjects)
        m1 = np.zeros(self.nSubjects)
        iP = np.zeros(self.nSubjects)
        iM = np.zeros(self.nSubjects)
        
        # this is to deal with my poor experimental design :::laughs::: 
        #if iStim >= 3: 
        #    pStim = iStim 
        #    mStim = iStim + 1
        # else: 
    
        mStim = pStim = iStim
        
        
        for iSubject in range(0,self.nSubjects): 

            if inputData == 'trans': 
                data = self.transData[iSubject][0]
                condMarkers = np.copy(self.transData[iSubject][1])
                pStims = self.stimuli(condMarkers[:,0])
                mStims = self.stimuli(condMarkers[:,1])
            else: 
                data = self.rawData[iSubject][:,0]
                condMarkers = np.copy(self.rawData[iSubject][:,1:3])
                pStims = self.stimuli(condMarkers[:,0])
                mStims = self.stimuli(condMarkers[:,1])
            
            if stimLocation == 'onset': 
                maxind_p,maxval_p,minind_p,minval_p = self.findAmplitude(data,pStims[0],pStim,self.nSeconds)
                maxind_m,maxval_m,minind_m,minval_m = self.findAmplitude(data,mStims[0],mStim,self.nSeconds)
                p1[iSubject] = maxval_p - minval_p
                iP[iSubject] = maxind_p
                m1[iSubject] = maxval_m - minval_m
                iM[iSubject] = maxind_m
            else: 
                maxind_p,maxval_p,minind_p,minval_p = self.findAmplitude(data,pStims[1],pStim,self.nSeconds)
                maxind_m,maxval_m,minind_m,minval_m = self.findAmplitude(data,mStims[1],mStim,self.nSeconds)
                p1[iSubject] = maxval_p - minval_p
                iP[iSubject] = maxind_p
                m1[iSubject] = maxval_m - minval_m
                iM[iSubject] = maxind_m

            if show: 
                figure(figsize=(20,4))
                plot(data,color='indigo',label='SCR timecourse')
                scatter([maxind_p,minind_p],[maxval_p, minval_p],color='xkcd:magenta',label='CS+')
                scatter([maxind_m,minind_m],[maxval_m, minval_m],color='xkcd:blue',label='CS-')
                condMarkers[0:-1:100] = 0
                plot((5*condMarkers[:,0]-5),color='xkcd:magenta',alpha=.1);  
                plot((5*condMarkers[:,1]-5),color='xkcd:blue',alpha=.1);  
                try: plot((5*condMarkers[:,2]-5),color='xkcd:magenta',alpha=.4,label='US');
                except: pass
                xlim([0,len(data)])
                ylim([min(data)-.25,max(data)+.25])
                tmpDifference = round(p1[iSubject]-m1[iSubject],3)
                legend()
                title('CS+ difference is %s, CS- difference is %s, CS+ minus CS- = %s\n'%(round(p1[iSubject],3),
                                                                      round(m1[iSubject],3),tmpDifference),fontsize=15);              
        return p1,m1

    def findAmplitude(self,data,stims,iStim,nsForward): 
        interval4max = data[stims[iStim]+1000*self.windowstart:stims[iStim]+1000*nsForward]
        index4max = stims[iStim] + interval4max.argmax() + 1000*self.windowstart
        value4max = data[index4max]

        interval4min = data[stims[iStim]:index4max]
        index4min = stims[iStim] + interval4min.argmin() 
        value4min = data[index4min]
        return index4max,value4max,index4min,value4min
    
