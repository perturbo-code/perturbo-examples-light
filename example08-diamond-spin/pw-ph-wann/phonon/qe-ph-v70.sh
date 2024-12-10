#!/bin/bash

sw='restart'
end='clear'

#-------------------------------------------------------------
cp -r ../tmp/ .

#-------------------------------------------------------------
echo Job starts at `date`
#-------------------------------------------------------------

NQ=
# Get the PREFIX from ph-ref.in
PREFIX=`awk -F= '{if($0~"prefix") print $NF}' ph-ref.in | sed "s/'//g" | sed 's/"//g'`
CASE=ph
sed -i  "s|.*outdir.*| outdir='./tmp'|g"  ${CASE}.in
export OMP_NUM_THREADS=1

# modify npools if needed
PH=/home/latan/software/qe-7.2/bin/ph.x
echo "$SLURM_NTASKS"
mpirun -np $SLURM_NTASKS $PH -npools 32 < ${CASE}.in > ${CASE}.out

#-------------------------------------------------------------
echo Job ends at `date`
#-------------------------------------------------------------

#-------------------------------------------------------------

