#!/bin/bash

phdir="../../../pw-ph-wann/phonon/save"

# Ask the user for the maximum value of N
read -p "Enter the number of phonon files: " N

mkdir phonon
cd phonon
mkdir save 
cd save

ln -sf "${phdir}/sto-nosoc.dyn0" 
echo "Created symbolic link for sto-nosoc.dyn0"
# Loop from 1 to N
for ((i=1; i<=N; i++)); do
    # link dvscf
    ln -sf "${phdir}/sto-nosoc.dvscf_q${i}"
    echo "Created symbolic link for sto-nosoc.dvscf_q${i}"
	 ln -sf ../../dyn_pop3_${i}.xml sto-nosoc.dyn${i}.xml
    echo "Created symbolic link for sto-nosoc.dyn${i}.xml"
done

ln -sf "${phdir}/sto-nosoc.phsave"
echo "Created symbolic link for sto-nosoc.phsave"
