#!/bin/bash
#SBATCH -N 1                 # Number of nodes
#SBATCH -p regular         
#SBATCH -J tdep0001
#SBATCH -t 24:00:00          # time limit

echo "Submit dir :" $SLURM_SUBMIT_DIR

PW=pw.x
CASE=qe_conf0001

RUN="srun -n 64 $PW"

$RUN -i "$CASE".in >"$CASE".out
