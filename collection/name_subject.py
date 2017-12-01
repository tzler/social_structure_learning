"""Search through old subject_names and find a new one."""

import os, sys

base_dir = os.getcwd()
old_names = os.listdir('%s/self_report_data/' % base_dir)

def new(self_report): 
    """If more than 8 characters : RuntimeError: Unexpected end of line.""" 

    day = self_report['day']

    names_old = [] 
    for name_i in old_names: 
        if name_i.startswith("s") and name_i.endswith("d%s.npy"%day): 
            names_old.append(name_i[0:-4]) 
  
    if len(sys.argv) > 1:  
        
        possible_name = 's' + sys.argv[-1] + '_d' + str(day)
        
        if possible_name in names_old:
            bad_name = possible_name
            del possible_name
            
        
    if 'possible_name' in locals(): 
    
        new_name = possible_name 
        error_msg = '' 
    
    elif len(sys.argv) == 1: 

        new_name = "s%02dx_d%s" % (len(old_names) + 1, day)  
        error_msg = 'WARNING: SUBJECT NAME NOT GIVEN. SETTING SUBJECT NAME TO %s, CHANGE WHEN POSSIBLE\n' %(new_name) 
  
    else: 
       
        new_name = "s%02dx_d%s" % (len(old_names) + 1, day)  
        error_msg = 'WARNING: SUBJECT NAME %s ALREADY IN USE, SETTING SUBJECT NAME TO %s, CHANGE WHEN POSSIBLE\n' %(bad_name, new_name) 
        
    # set 
    print(int(new_name[1:3]))
    if int(day) - 1:
        
        counter_balance = int(new_name[1:3])%2
        print counter_balance, type(counter_balance) 
    
    else: 

        counter_balance = None
        print counter_balance
    
    self_report['subject_id'] = new_name
    self_report['error_msg'] = error_msg
    self_report['counter_balance'] = counter_balance

    if error_msg: print '\n\n\n', 'WARNING\n'*5, error_msg, 'WARNING\n'*5, '\n\n\n'
    else: print '\n\n\nNAMING CURRENT SUBJECT %s\n\n\n' %new_name 
    #  new_name, error_msg, counter_balance
    return self_report 
  
