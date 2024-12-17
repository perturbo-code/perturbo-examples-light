#!/usr/bin/env python3
import perturbopy.postproc as ppy

prefix = 'gaas'

# Define electron paths and DynaRun object
cdyna_elec_path = f'cdyna-elec/{prefix}_cdyna.h5'
elec_tet_path = f'cdyna-elec/{prefix}_tet.h5'
elec_yaml_path = f'cdyna-elec/{prefix}_dynamics-run.yml'
elec_dyna_run = ppy.DynaRun.from_hdf5_yaml(cdyna_elec_path, elec_tet_path, elec_yaml_path)

# Define hole paths and DynaRun object
cdyna_hole_path = f'cdyna-hole/{prefix}_cdyna.h5'
hole_tet_path = f'cdyna-hole/{prefix}_tet.h5'
hole_yaml_path = f'cdyna-hole/{prefix}_dynamics-run.yml'
hole_dyna_run = ppy.DynaRun.from_hdf5_yaml(cdyna_hole_path, hole_tet_path, hole_yaml_path)

# Print DynaRun info
print(elec_dyna_run)
print(hole_dyna_run)

# Print the PumpPulse info
print(elec_dyna_run.pump_pulse)

ppy.utils.spectra_trans_abs.compute_trans_abs(elec_dyna_run, hole_dyna_run)

elec_dyna_run.close_hdf5_files()
hole_dyna_run.close_hdf5_files()