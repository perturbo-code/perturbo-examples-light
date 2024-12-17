#!/usr/bin/env python

#-------------------------------------------------------------------------------
# File: parse_qe_input.py
# Author: jjchou <jjchou.comphy@gmail.com>
# Create Date: 2017-03-03 12:26:13
#-------------------------------------------------------------------------------

"""
 Functions to parse QE input file.
"""

import re

# read lines, remove comment lines
def read_file(fname):
    lines = []
    with open(fname, 'r') as inpf:
        for i in inpf:
            if i.strip() and i.strip()[0] != '#':
                lines.append(i)
    return lines

# read namelist
def read_nlist(file_in, lname):
    dict_out = {}; found = False
    for line in file_in:
        if re.match('&'+lname.upper(), line.upper() ):
            found = True
        elif line.strip() == "/":
            found = False
        elif found:
            pair = line.strip().split('=')
            if len(pair) == 2:
                dict_out[pair[0].strip().lower()] = pair[1].strip()
    return dict_out

# read namecard
def read_ncard(file_in, lname, numl):
    for line in file_in:
        if re.match( lname.upper(), line.strip().upper() ):
            idx = file_in.index(line)
            return file_in[idx:idx+numl]
    return []
