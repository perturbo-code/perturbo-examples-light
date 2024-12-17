## title: PERTURBO interface with TDEP and SSCHA
### last updated: Dec 10, 2024
This folder contains examples to execute qe2pert.x to read 2nd-order force constants from TDEP or SSCHA.
The material used is SrTiO3  without spin-orbit coupling (nosoc)
Note: one still needs results from DFPT despite reading the force constants from other sources.


Folders: 
   pw-ph-wann: 
      nscf: nscf results
      wann: wannier results
      phonon: DFPT results
      pseudo: pseudo potentials
   sscha: sscha results
   tdep: tdep results
   qe2pert-sscha: example input for qe2pert.x interfacing with SSCHA
   qe2pert-tdep: example input for qe2pert.x interfacing with TDEP
   pert-phdisp: example input for PERTURBO phonon dispersion, used to compare results
