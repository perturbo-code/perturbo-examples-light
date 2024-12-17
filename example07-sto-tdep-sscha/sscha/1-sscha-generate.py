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

# Provide your DFPT dynamical matrices (in conventional QE format)
# Specify the number of irreducible q points
dyn = CC.Phonons.Phonons("./phonon-not-xml/sto-nosoc.dyn", nqirr=10)

dyn.Symmetrize()
dyn.ForcePositiveDefinite()

# Set the temperature
ensemble = sscha.Ensemble.Ensemble(dyn, T0=200, supercell=dyn.GetSupercell())

# Set the number of configs to generate
ensemble.generate(N=100)

# Set the saving directory for the configs
ensemble.save("data_ensemble_manual", population = 1)
