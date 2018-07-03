from matplotlib.mlab import find
from matplotlib.pyplot import * 
import scipy.signal as signal
import numpy as np
import pandas
import os



class experimental(object):  
    def __init__(self, path2data):    
        
        # loadData configs
        self.path2data = path2data
        self.day = 1
        # transformData configs
        self.showTransform = 0 
        self.keepEdgeBefore = 5 #
        self.keepEdgeAfter = 5
        self.filterOrder = 2 
        self.lowPassCutoffFrequency = 0.00001
        self.hightPassCutoffFrequency = .0005
        # 
        #self.showDifference = 0 
        # transformData configs
        self.showTransform = 0 
        #self.transWindow = 10 # 
        self.filterOrder = 2 
        self.lowPassCutoffFrequency = 0.00001
        self.hightPassCutoffFrequency = .0005
        # 
        
        
        self.windowstart = 1
        
        self.nSeconds = 4.5
    def loadData(self): 
        self.rawData = {} ; 
        self.subjectNames = []
        tmpFiles = os.listdir(self.path2data)
        tmpFiles.sort()
        count = 0 
        
        if self.day == 2: 
            fileEnding = 'part2.txt'
        if self.day == 1: 
            fileEnding = 'part1.txt'
        #if self.day == 'cb': 
        #    fileEnding = 'cb_part2.txt'
        #    self.day = 2
            
        self.US = 2 - self.day
        for file in tmpFiles: 
            if str.find(file, fileEnding) != -1: 
                tmp = pandas.read_csv('%s/%s'%(self.path2data,file), sep=',',header=None)
                self.rawData[count] = tmp.values[:,0:5-self.day] ; 
                self.subjectNames.append(file) ; count = count+1
        
        self.nSubjects = len(self.subjectNames)
  
    def transformData(self): 
        
        keepers = []
        transformedData = []
        rawData = self.rawData
        self.rawDataCut = []
        
        for iSubject in range(0,len(rawData)): 
            # extract the timecourse of the experiment, not the initial resting period or post-experiment questions 
            onset  = min(min(find(rawData[iSubject][:,1])),min(find(rawData[iSubject][:,2]))) - 1000*self.keepEdgeBefore 
            offset = max(max(find(rawData[iSubject][:,2])),max(find(rawData[iSubject][:,1]))) + 1000*self.keepEdgeAfter
            temp = rawData[iSubject][onset:offset,0]  
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
            
            # a oversimplified exclusion criteria
            if np.std(filteredData) > .1: 
                 keepers.append(iSubject)
            
            # zscore the filtered data
            filteredData = (filteredData-np.mean(filteredData))/np.std(filteredData)
            transformedData.append([filteredData,rawData[iSubject][onset:offset,1:(3+self.US)]])
            
            if self.showTransform: 
                figure(figsize=(20,5))
                plot(temp, 'xkcd:blue',alpha=.4, linewidth=5)
                plot(lowFreq, 'r-',alpha=.3,linewidth=5)
                plot(belowHighFreq,'indigo',linewidth=3,alpha=.7)
                legend(['Original','low pass filtered','high pass filtered'])
                figure(figsize=(20,3))
                ylim([min(filteredData)-.25,max(filteredData)+.25]); 
                xlim([0,len(filteredData)])

                if iSubject == keepers[-1]: 
                    plot(filteredData,'indigo',linewidth=3,alpha=.7,color='xkcd:blue')
                    title('standard deviation = %s > .1\nKEEPING SUBJECT'% (np.std(belowHighFreq-lowFreq)))
                else:
                    plot(filteredData,'indigo',linewidth=6,alpha=.7,color='xkcd:crimson')
                    title('standard deviation = %s < .1\nEXCLUDING SUBJECT'%(np.std(belowHighFreq-lowFreq)))

        self.transData = transformedData
        self.keepers = keepers
    
    def logTransform(self,plus,minus):         
        plus[plus<=0] = 0 
        minus[minus<=0] = 0 
        plus = log(1+plus)
        minus = log(1+minus)
        return plus,minus
               
    def preprocessData(self): 
        self.loadData()
        self.transformData()
        
    def stimuli(self,CS): 
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
        
    
    def simpleDifference(self,inputData,iStim,z = 0,show=0): 
        
        p1 = np.zeros(len(inputData)) ; 
        m1 = np.zeros(len(inputData))
        
        if iStim >= 3: 
            pStim = iStim 
            mStim = iStim + 1
        else: 
            mStim = pStim = iStim

        for iSubject in range(0,len(inputData)): 

            # load from one of two data types
            if type(inputData) == list: 
                data = inputData[iSubject][0]
                plusOn, plusOff = self.stimuli(inputData[iSubject][1][:,0])
                minusOn, minusOff = self.stimuli(inputData[iSubject][1][:,1])
                condMarkers = np.copy(inputData[iSubject][1])
            else: 
                data = inputData[iSubject][:,0]
                plusOn,plusOff = self.stimuli(inputData[iSubject][:,1])
                minusOn,minusOff = self.stimuli(inputData[iSubject][:,2])
                condMarkers = np.copy(inputData[iSubject][:,1:-1])
        
            if z: 
                data = (data-np.mean(data))/np.std(data)

            p1[iSubject] = data[plusOff[pStim]] - data[plusOn[pStim]] 
            m1[iSubject] = data[minusOff[mStim]] - data[minusOn[mStim]]        
            if show: 
                figure(figsize=(20,4))
                plot(data)
                scatter([plusOn[pStim],plusOff[pStim]],[data[plusOn[pStim]] ,data[plusOff[pStim]]],color='xkcd:red')
                scatter([minusOn[mStim],minusOff[mStim]],[data[minusOn[mStim]] ,data[minusOff[mStim]]],color='xkcd:blue')
                condMarkers[0:-1:100] = 0
                plot((5*condMarkers[:,0]-5),color='xkcd:magenta',alpha=.1);  
                plot((5*condMarkers[:,1]-5),color='xkcd:blue',alpha=.1);
                ylim([min(data)-.25,max(data)+.25])
                xlim([0,len(data)])
                tmpDifference = round(p1[iSubject]-m1[iSubject],3)
                title('CS+ difference is %s, CS- difference is %s, CS+ minus CS- = %s\n%s'%
                                                                          (round(p1[iSubject],3),
                                                                          round(m1[iSubject],3),
                                                                          tmpDifference,
                                                                          self.subjectNames[iSubject]),
                                                                          fontsize=15);

                try: plot((5*condMarkers[:,2]-5),color='crimson',alpha=.5);
                except: pass

        return p1, m1
        
    def visualizeStats(self,plus,minus,results,keepers,subjectNames,heading='vicarious renewal',show=1): 
        # simple computations
        plus = plus[keepers]
        minus = minus[keepers]
        diff = plus-minus  
        # visualization set up
        figure(figsize=(8,5))
        plusColor = 'xkcd:magenta'
        minusColor = 'xkcd:blue'
        diffColor = 'xkcd:turquoise'
        # scatter
        scatter(np.ones(len(plus))-1,plus,alpha = .3,color=plusColor)
        scatter(0,np.mean(plus),alpha = .2,color=plusColor,linewidth=13,marker='D')
        scatter(np.ones(len(plus))+1,minus,alpha = .3,color=minusColor)
        scatter(2,np.mean(minus),alpha = .2,color=minusColor, linewidth=13,marker='D')
        scatter(np.ones(len(plus))+3,diff,alpha = .3,color=diffColor)
        scatter(4,np.mean(diff),alpha = .2,color=diffColor, linewidth=13,marker='D')
        legend([' CS+','mean',' CS-','mean ','CS+--CS-','   mean'],
               bbox_to_anchor=(.4,.5,.4,.5),
               ncol=3)
        xlim([-1,5]); xticks([])
        #ylim([min(minus)-.25,(max(diff))+1])
        title('\n- %s -\namplitude values for CS+ and CS+ (p < %s)\n'%(heading,results[1]),fontsize=12);
        if show == 'all': 
            figure(figsize=(15,5))
            plot(plus,color=plusColor,alpha=.8) ; 
            plot(repeat(np.mean(plus),len(plus)),linewidth=12,alpha=.2,color=plusColor)
            plot(minus,color=minusColor,alpha=.8)
            plot(repeat(np.mean(minus),len(minus)),linewidth=12,alpha=.2,color=minusColor)
            title('\n- %s -\n amplitude of responce for CS+ and CS-\n'%heading,fontsize=15); 
            legend(['CS+','mean CS+','CS-','mean CS-']);
            plot(plus,color=plusColor,alpha=.3,linewidth=10) ; 
            plot(minus,color=minusColor,alpha=.3,linewidth=10); 
            xticks([])

            figure(figsize=(15,5))
            plot(diff,alpha = .9,color='xkcd:turquoise')
            plot(diff,alpha = .3,linewidth=10,color='xkcd:teal')
            title('amplitude differences scores (CS+ minus CS-)\n')
            for iName in range(0,len(keepers)): 
                annotate(subjectNames[keepers[iName]][0:-10], (iName,diff[iName]),alpha=.9)
                
    
    
    def amplitudeDifference(self,inputData,iStim,stimLocation,show=0): 
        p1 = np.zeros(self.nSubjects)
        m1 = np.zeros(self.nSubjects)
        iP = np.zeros(self.nSubjects)
        iM = np.zeros(self.nSubjects)
        
        # this is to deal with my poor experimental design :::laughs::: 
        if iStim >= 3: 
            pStim = iStim 
            mStim = iStim + 1
        else: 
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
    
def visualizeStats(plus,minus,results,heading='vicarious renewal',show=1): 
    figure(figsize=(20,5))
    subplot(121)
    plusColor = 'xkcd:magenta'
    minusColor = 'xkcd:blue'
    diffColor = 'xkcd:turquoise'
    # scatter
    scatter(np.zeros(len(plus)),plus,alpha = .3,color=plusColor)
    scatter(0,np.mean(plus),alpha = .2,color=plusColor,linewidth=13,marker='D')
    scatter(np.ones(len(minus)),minus,alpha = .3,color=minusColor)
    scatter(1,np.mean(minus),alpha = .2,color=minusColor, linewidth=13,marker='D')
    xlim([-1,2]); xticks([])
    #ylim([-2,2])
    title('\n- %s -\namplitude values for CS+ and CS+ (p < %.3f)\n'%(heading,results[1]),fontsize=12);
    if show == 'all': 
        figure(figsize=(15,5))
        plot(plus,color=plusColor,alpha=.8) ; 
        plot(repeat(np.mean(plus),len(plus)),linewidth=12,alpha=.1,color=plusColor)
        plot(minus,color=minusColor,alpha=.8)
        plot(repeat(np.mean(minus),len(minus)),linewidth=12,alpha=.1,color=minusColor)
        title('\n- %s -\n amplitude of responce for CS+ and CS-\n'%heading,fontsize=15); 
        legend(['CS+','mean CS+','CS-','mean CS-']);
        plot(plus,color=plusColor,alpha=.3,linewidth=10) ; 
        plot(minus,color=minusColor,alpha=.3,linewidth=10); 
        xticks([])
    
    subplot(122)
    
    hist(plus,alpha=.3,color='red')
    hist(minus,alpha=.3,color='blue')
    title('mean CS+ = %s, mean CS- = %s'%(np.mean(plus),np.mean(minus)))

