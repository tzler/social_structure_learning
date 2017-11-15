"""Search through old subject_names and find a new one."""

import os
import numpy as np

base_dir = os.getcwd()
old_names = os.listdir('%s/self_report_data/' % base_dir)


def new():
    """If more than 8 characters : RuntimeError: Unexpected end of line."""
    #
    names_old = []
    for name_i in old_names:
        if name_i.startswith("s_") and name_i.endswith(".npy"):
            names_old.append(int(name_i[2:4]))
    
    print type(names_old), names_old
    
    if len(names_old):
        new_name = "s_%02d" % (max(names_old) + 1)
    else:
        new_name = 's_01'
    
    print 'new_name: ', new_name
    return new_name
