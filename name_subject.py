"""Search through old subject_names and find a new one."""

import os
base_dir = os.getcwd()
old_names = os.listdir('%s/self_report_data/' % base_dir)


def new():
    """If more than 8 characters : RuntimeError: Unexpected end of line."""
    #
    names_old = []
    for name_i in old_names:
        if name_i.startswith("s_") and name_i.endswith(".npy"):
            names_old.append(name_i[2:5])

    if len(names_old):
        new_name = "s_%03d" % (int(max(names_old)) + 1)
    else:
        new_name = 's_001'

    return new_name
