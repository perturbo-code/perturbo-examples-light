#!/usr/bin/env python2

#-------------------------------------------------------------------------------
# File: qe_output_force.py
# Author: jjchou <jjchou.comphy@gmail.com>
# Create Date: 2017-03-03 11:21:57
#
#-------------------------------------------------------------------------------

"""
Extract postion (fractional coord) and forces on atoms (eV/Angstrom).
"""

from optparse import OptionParser
from parse_qe_input import *

usage = "usage: %prog [options] displaced.in  displaced.out"
parser = OptionParser(usage=usage)
parser.add_option('-p','--position', type='string',dest='outp', \
         default='infile.positions', help="output file for positions")
parser.add_option('-f', '--force', type='string',dest='outf', \
         default='infile.forces', help="output file for forces")
parser.add_option('-a',action='store_true',dest='append',default=False, \
        help="-a: append output to files")

if __name__ == '__main__':
    options, args = parser.parse_args()
    #read input file.
    lines = read_file(args[0])
    system = read_nlist(lines, 'system')
    # number of atomics in the supercell.
    if system.has_key('nat'):
        nat = int(system['nat']) 
    else:
        message = " No 'nat' in {0} !".format(args[0],)
        raise NameError(message)
    # atomic positions of equilibrium and displaced supercell.
    pos = read_ncard(lines,'atomic_positions',nat+1)
    if not pos:
        message = "No 'atomic_positions' found in {0} !".format(args[0],)
        raise NameError(message)
    
    #read forces on each atoms from QE output file, the third argument.
    with open(args[1], 'r') as inpf:
        tag = "Forces acting on atoms"
        flist = []

        line = inpf.readline()
        while line:
            if tag in line:
                inpf.readline()
                for i in range(nat):
                    flist.append(inpf.readline().split()[-3:])
                break
            else:
                line = inpf.readline()

    if len(flist) != nat:
        message = "Fail to read force from {0}".format(args[-1],)
        raise NameError(message)
    unitconv = 13.6056925250 / 0.52917721092
    force = [ [float(i)*unitconv for i in ifc] for ifc in flist ]

    #output postion info
    mode = 'a' if options.append else 'w'
    with open(options.outp, mode) as pos_file:
        for i in pos[1:]:
            coord = " {0[0]}  {0[1]}  {0[2]}\n".format(i.split()[-3:])
            pos_file.write(coord)
    with open(options.outf, mode) as for_file:
        for i in force:
            line = " {0: .7f}  {1: .7f}  {2: .7f}\n".format(i[0], i[1], i[2])
            for_file.write(line)
