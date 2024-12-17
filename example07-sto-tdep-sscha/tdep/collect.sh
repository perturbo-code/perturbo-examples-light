#!/usr/bin/env bash

HDIR="${HOME}/example07-sto-tdep/tdep"
EXE="${HDIR}/tools/qe_pos_force.py"

echo "collecting qe_conf0001 ..."
${EXE} qe_conf0001.in qe_conf0001.out

for i in {2..5}
do 
   if [ "$i" -lt 10 ]; then
      ND="000${i}"
   else
      ND="00${i}"
   fi
   echo "collecting qe_conf${ND} ..."
   ${EXE} -a qe_conf${ND}.in  qe_conf${ND}.out

done
