#!/usr/bin/env python3
import perturbopy.postproc as ppy

prefix = 'gaas'

# Define electron paths and DynaRun object
cdyna_elec_path = f'cdyna-elec/{prefix}_cdyna.h5'
elec_tet_path = f'cdyna-elec/{prefix}_tet.h5'
elec_yaml_path = f'cdyna-elec/{prefix}_dyna_init.yml'
elec_dyna_run = ppy.DynaRun.from_hdf5_yaml(cdyna_elec_path, elec_tet_path, elec_yaml_path)

# Define hole paths and DynaRun object
cdyna_hole_path = f'cdyna-hole/{prefix}_cdyna.h5'
hole_tet_path = f'cdyna-hole/{prefix}_tet.h5'
hole_yaml_path = f'cdyna-hole/{prefix}_dyna_init.yml'
hole_dyna_run = ppy.DynaRun.from_hdf5_yaml(cdyna_hole_path, hole_tet_path, hole_yaml_path)

# Print DynaRun info
print(elec_dyna_run)
print(hole_dyna_run)

# Generate the pump pulse HDF5 files in the
# elec_pump_pulse_path and hole_pump_pulse_path folders
pump_energy = 1.5
elec_pump_pulse_path = f'cdyna-elec/pump_pulse_elec_Epump_{pump_energy:05.2f}.h5'
hole_pump_pulse_path = f'cdyna-hole/pump_pulse_hole_Epump_{pump_energy:05.2f}.h5'

ppy.utils.spectra_generate_pulse.setup_pump_pulse(
    elec_pump_pulse_path,
    hole_pump_pulse_path,
    elec_dyna_run,
    hole_dyna_run,
    pump_energy=pump_energy,
    pump_time_step=1.0,
    pump_fwhm=20.0,
    pump_energy_broadening=0.040,
    pump_time_window=50.0,
    finite_width=True,
    animate=True)

elec_dyna_run.close_hdf5_files()
hole_dyna_run.close_hdf5_files()