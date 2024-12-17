#!/usr/bin/env python3
import numpy as np
import perturbopy.postproc as ppy
import matplotlib.pyplot as plt

pump_energy = 1.5

# Load the numpy binary files
dA_elec = 'trans_abs_dA_elec_Epump_1.500.npy'
dA_hole = 'trans_abs_dA_hole_Epump_1.500.npy'
time_grid = 'trans_abs_T_Epump_1.500.npy'
energy_grid = 'trans_abs_E_Epump_1.500.npy'

dA_elec = np.load('trans_abs_dA_elec_Epump_1.500.npy')
dA_hole = np.load('trans_abs_dA_hole_Epump_1.500.npy')
time_grid = np.load('trans_abs_T_Epump_1.500.npy')
energy_grid = np.load('trans_abs_E_Epump_1.500.npy')

# Plot the total transient absorption
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
plt.subplots_adjust(left=0.12, right=0.88, top=0.9, bottom=0.12)
ppy.utils.spectra_plots.plot_trans_abs_map(ax,  time_grid, energy_grid, dA_elec+dA_hole, vmin=-2.5, vmax=0.0)
ax.set_title(f'Transient absorption in GaAs, Epump={pump_energy:.1f} eV')
ax.set_ylim(ymax=2.3)
fig.savefig('dA_total.png')
plt.show()

# Plot the electron contribution
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
plt.subplots_adjust(left=0.12, right=0.88, top=0.9, bottom=0.12)
ppy.utils.spectra_plots.plot_trans_abs_map(ax, time_grid, energy_grid, dA_elec, vmin=-2.5, vmax=0.0)
ax.set_title('Electron contribution')
ax.set_ylim(ymax=2.3)
fig.savefig('dA_elec.png')
plt.show()

# Plot the hole contribution
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
plt.subplots_adjust(left=0.12, right=0.88, top=0.9, bottom=0.12)
ppy.utils.spectra_plots.plot_trans_abs_map(ax, time_grid, energy_grid, dA_hole, vmin=-2.5, vmax=0.0)
ax.set_title('Hole contribution')
ax.set_ylim(ymax=2.3)
fig.savefig('dA_hole.png')
plt.show()