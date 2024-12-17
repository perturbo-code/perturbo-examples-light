import sys,os

import ase
from ase.calculators.espresso import Espresso
from ase.visualize import view

# We import the basis modules for the SSCHA
import cellconstructor as CC
import cellconstructor.Structure
import cellconstructor.Phonons

# Import the SSCHA engine (we will use it later)
import sscha, sscha.Ensemble, sscha.SchaMinimizer, sscha.Relax

import numpy as np

# Edit these
n_configs = 100
target_dir = 'data_ensemble_manual'

energies = np.zeros(n_configs)
for id_number in range(1, n_configs+1):

    file = 'ensemble_' + str(id_number) + '/scf.out'

    # Load the file
    ff = open(file, "r")
    lines = [l.strip() for l in ff.readlines()] # Read the whole file removing tailoring spaces
    ff.close()

    # Lets look for the energy (in espresso the first line that starts with !)
    # next is used to find only the first occurrence
    energy_line = next(l for l in lines if len(l) > 0 if l.split()[0] == "!")

    # Lets collect the energy (the actual number is the 5th item on the line, but python indexes start from 0)
    # note, also the id_number are saved starting from 1
    energies[id_number - 1] = float(energy_line.split()[4])

    # Now we can collect the force
    # We need the number of atoms
    nat_line = next( l for l in lines if len(l) > 0 if l.split()[0] == "number" and l.split()[2] == "atoms/cell" )
    nat = int(nat_line.split()[4])
    print('nat=', nat)

    # Now allocate the forces and read them
    forces = np.zeros((nat, 3))
    forces_lines = [l for l in lines if len(l.split()) > 5 and l.split()[4] == "force"] # All the lines that starts with atom will contain a force
    for i in range(nat):
        forces[i, :] = [float(x) for x in forces_lines[i].split()[-3:]] # Get the last three number from the line containing the force

    # Now we can take the stress tensor
    stress = np.zeros((3,3))
    # We pick the index of the line that starts with the words total stress
    index_before_stress = next(i for i, l in enumerate(lines) if len(l) > 0 if l.split()[0] == "total" and l.split()[1] == "stress")
    # The stress tensor is located just after it
    for i in range(3):
        index = i + index_before_stress + 1
        stress[i, :] = [float(x) for x in lines[index].split()[:3]]

    # We can save the forces_population1_X.dat and pressures_population1_X.dat files
    force_file = os.path.join(target_dir, "forces_population1_{}.dat".format(id_number))
    stress_file = os.path.join(target_dir, "pressures_population1_{}.dat".format(id_number))
    np.savetxt(force_file, forces)
    np.savetxt(stress_file, stress)

# Now we read all the configurations, we can save the energy file
energy_file = os.path.join(target_dir, "energies_supercell_population1.dat")
np.savetxt(energy_file, energies)



