"""Search through old subject_names and find a new one."""

import os, sys

base_dir = os.getcwd()
old_names = os.listdir('%s/self_report_data/' % base_dir)


def command_line(): 
    """If more than 8 characters : RuntimeError: Unexpected end of line.""" 

   
    possible_name = sys.argv[-1]
    
    print 'sys.argv from inside of function: ', sys.argv, 'possible_name =', possible_name
     
    names_old = [] 
    for name_i in old_names: 
        if name_i.startswith("s_") and name_i.endswith(".npy"): 
            names_old.append(name_i[0:4]) 
    
    if 'day' in possible_name:
        
        new_name = "s_%02d_fix" % (len(old_names) + 1)  
        error_msg = 'ERROR: EXPERIMENTOR FAILED TO INCLUDE SUBJECT NAME, USING %s, CHANGE AS SOON AS POSSIBLE \n' %new_name
    
    elif possible_name in names_old: 
        
        new_name = "s_%02d_fix" % (len(old_names) + 1)  
        error_msg = 'ERROR: SUBJECT NAME %s ALREADY IN USE, SETTING SUBJECT NAME TO %s, CHANGE WHEN POSSIBLE\n' %(possible_name, new_name) 
        
    else: 
        
        new_name = possible_name
        error_msg = 0
    
    if error_msg: print '\n\n\n', 'ERROR\n'*10, error_msg, 'ERROR\n'*10, '\n\n\n'
    else: print '\n\n\nNAMING CURRENT SUBJECT %s\n\n\n' %new_name 
    return new_name, error_msg
