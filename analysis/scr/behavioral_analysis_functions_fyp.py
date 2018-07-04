# load functions for data analysis
from matplotlib import pyplot as plt
import pandas, os, scipy
import seaborn as sns
import numpy as np
import glob

sns.set()

pandas.options.mode.chained_assignment = None


def generate_data_frame():
    """Generate a pandas data frame from behavioral data of all subjects."""
    data_path = os.getcwd() + '/../data_self_report_study1'
    file_names = os.listdir(data_path) 
    file_names.sort()

    subject_names = []

    for file in file_names:
        if str.find(file, 'part1') != -1:
            subject_names.append(str(file[0:4]))
        

    for i_file in file_names: 
    
        if 'part1' in i_file:
    
            day1_info = np.load('%s/%s'%(data_path,i_file)).item()
            questions_day1 = list(day1_info.keys())
    
        elif 'part2' in i_file:
    
            day2_info = np.load('%s/%s'%(data_path,i_file)).item()
            questions_day2 = list(day2_info.keys())
            break

    self_report = pandas.DataFrame(index=subject_names, columns=questions_day1+questions_day2)

    for i_subject in subject_names: 
        days = glob.glob('%s/%s*'%(data_path, i_subject))
        # need to account for awkward irregularities in data collection   
        for i_day in days:
            tmp_info = np.load(i_day).item()        
            for i_question in range(0,len(tmp_info)):
                if tmp_info.keys()[i_question] == 'post: believe': 
                    self_report['belief'][i_subject] = tmp_info[tmp_info.keys()[i_question]]
                else: 
                    self_report[tmp_info.keys()[i_question]][i_subject] = tmp_info[tmp_info.keys()[i_question]]       


    # clean up some of the errors people made entering the data
    self_report['pre: voltage']['s_08'] = 7. 
    self_report['pre: voltage']['s_37'] =  5.
    self_report['pre: voltage']['s_43'] = 6.0
    self_report['pre: voltage']['s_27'] = 3.
    self_report['pre: voltage']['s_30'] = 1.1
    # 
    self_report['post: color']['s_24'] =  'red'
    self_report['post: color']['s_43'] =  np.nan
    # 
    self_report['correctColor'] = (self_report['post: color'] == 'red')
    self_report['expectShock'] = (self_report['first'] == 'yes')
    self_report['belief'] = (self_report['third'] == 'yes')
    # 
    convert_columns = ['post: relate', 'post: otherPain', 'pre: aversive', 'post: selfPain', 
                       'post: familiar', 'post: like', 'post: similar', 'pre: voltage', 'expectShock', 'belief']

    for column in convert_columns: 
        self_report[column] = pandas.to_numeric(self_report[column]); 
    
    return self_report, subject_names

def correlation_matrix(self_report):
    """Visualize correlation matrix from behavioral data."""
    title_names = self_report.corr().keys()

    fig, ax1 = plt.subplots(1,1)
    fig.set_size_inches([10,10])
    ax = plt.imshow(self_report.corr())
    ax1.set_xticks(np.array(list(range(0,len(title_names)))))
    ax1.set_xticklabels(title_names,rotation=70); 
    ax1.set_yticks(np.array(list(range(0,len(title_names)))))
    ax1.set_yticklabels(title_names); 
    ax.set_cmap('bwr') # 'coolwarm' # 'seismic'
    ax.set_clim([-1,1])
    ax.set_alpha(1)
    plt.title('correlation between self report measures\n'); 
    #plt.colorbar()
    plt.show()

def cluster(self_report):
    sns.clustermap(self_report.corr(),cmap='bwr')
    plt.show()
