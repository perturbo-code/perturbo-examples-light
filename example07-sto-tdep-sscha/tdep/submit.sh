#!/usr/bin/env bash

HDIR="${HOME}/example07-sto-tdep/tdep"

for i in {1..5}
do 
   if [ "$i" -lt 10 ]; then
      ND="000${i}"
   else
      ND="00${i}"
   fi
   echo "submitting qe_conf${ND} ..."
   
   ${HDIR}/tools/qe_input_merge.py qe_conf${ND} ${HDIR}/scf_ref.in -o qe_conf${ND}.in
   cp submit.slurm submit${ND}.slurm
   sed -i "s|.*CASE=.*|CASE=qe_conf${ND}|g" submit${ND}.slurm
   sed -i "s|.*#SBATCH -J.*|#SBATCH -J tdep${ND}|g" submit${ND}.slurm

   sleep 0.5
done
