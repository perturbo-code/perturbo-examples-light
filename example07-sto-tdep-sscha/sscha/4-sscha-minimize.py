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
dyn = CC.Phonons.Phonons("./phonon-not-xml/sto-nosoc.dyn", nqirr=10)
dyn.Symmetrize()
dyn.ForcePositiveDefinite()
ensemble = sscha.Ensemble.Ensemble(dyn, T0=200, supercell=dyn.GetSupercell())
ensemble.load("data_ensemble_manual", population=1, N=100)

# Lets reset other calculation if you run this cell multiple times
ensemble.update_weights(dyn, 200) # Restore the original density matrix at T = 100 K
minimizer = sscha.SchaMinimizer.SSCHA_Minimizer(ensemble)

# Ignore the structure minimization (is fixed by symmetry)
minimizer.minim_struct = False

# Setup the minimization parameter for the covariance matrix
minimizer.min_step_dyn = 0.001 # Values around 1 are good
#minimizer.precond_dyn = False
#minimizer.root_representation = "root2"

# Setup the threshold for the ensemble wasting
minimizer.kong_liu_ratio = 0.5 # Usually 0.5 is a good value

# Auxiliary frequency saving function
IO_freq = sscha.Utilities.IOInfo()
IO_freq.SetupSaving("freqs.dat")

# Lest start the minimization
minimizer.init()
minimizer.run(custom_function_post=IO_freq.CFP_SaveFrequencies)

minimizer.finalize()

# We can save the dynamical matrix
minimizer.dyn.save_qe("dyn_pop1_")
# If convergence is reached, use the patched function below to output to xml format
# Remember to provide a set of original DFPT .dyn.xml as templates for the patch function to fill in
minimizer.dyn.save_qe_xml("../pw-ph-wann/phonon/save/sto-nosoc.dyn", "dyn_pop3_")


# Print the frequencies before and after the minimization
w_old, p_old = ensemble.dyn_0.DiagonalizeSupercell() # This is the representation of the density matrix used to generate the ensemble
w_new, p_new = minimizer.dyn.DiagonalizeSupercell()

# We can now print them
print(" Old frequencies |  New frequencies")
print("\n".join(["{:16.4f} | {:16.4f}  cm-1".format(w_old[i] * CC.Units.RY_TO_CM, w_new[i] * CC.Units.RY_TO_CM) for i in range(len(w_old))]))
