#!/usr/bin/env python2

#-------------------------------------------------------------------------------
# File: qe_input_merge.py
# Author: jjchou <jjchou.comphy@gmail.com>
# Create Date: 2017-02-23 22:23:04
#-------------------------------------------------------------------------------

"""
Generate new input file for QE by merging multiple input files.
"""

from optparse import OptionParser
from parse_qe_input import *

usage = "usage: %prog [options] qe_1.in qe_2.in qe_3.in ... "
parser = OptionParser(usage=usage)
parser.add_option('-o', '--output', type="string", dest='opf', default='qe.in',\
                help="output filename")

if __name__ == '__main__':
    options, args = parser.parse_args()
    
    nlist = ['control', 'system', 'electrons', 'ions', 'cell']
    ncard = ['cell_parameters', 'atomic_species', 'atomic_positions', 'k_points']
    dict_list = {};  dict_card = {}; card_num = {}
    
    # read and merge multiple input files, gather info.
    for fname in args:
        lines = read_file(fname)
        # read, update namelist. overwrite repeated one.
        for key in nlist:
            data = read_nlist(lines, key)
            if dict_list.has_key(key):
                dict_list[key].update(data)
            elif data:
                dict_list[key] = data
        
        card_num['cell_parameters'] = 4
        card_num['k_points'] = 2
        if dict_list.has_key('system') and dict_list['system'].has_key('ntyp'):
            card_num['atomic_species'] = 1 + int(dict_list['system']['ntyp'])
        if dict_list.has_key('system') and dict_list['system'].has_key('nat'):
            card_num['atomic_positions'] = 1 + int(dict_list['system']['nat'])
        # read and overwrite namecard
        for key in ncard:
            numl = card_num[key]
            data = read_ncard(lines, key, numl)
            if data: dict_card[key] = data

    #output input file with merged info.
    with open(options.opf,'w') as outpf:
        # output namelist
        for key in nlist:
            if dict_list.has_key(key):
                outpf.writelines('&'+key.upper()+'\n')
                for tag, value in dict_list[key].items():
                    outpf.writelines('  ' + tag + ' = ' + value + '\n')
                outpf.writelines('/\n')
        # output namecard
        for key in ncard:
            if dict_card.has_key(key):
                for i in dict_card[key]:
                    outpf.writelines(i)
