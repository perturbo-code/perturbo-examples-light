#!/bin/bash 
#SBATCH  -J qe2pert
#SBATCH  -p normal
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=8
#SBATCH  -t 24:00:00

module load compiler/intel-compiler/2021.3.0
module load mpi/intelmpi/2021.3.0 
module load mathlib/hdf5/intel/1.12.0

export I_MPI_PMI_LIBRARY=/opt/gridview/slurm/lib/libpmi.so
#HDF5: enables flock to allow multiple applications opening the same file
export HDF5_USE_FILE_LOCKING=FALSE

QE_DIR=/public/home/jjzhou/software/qe-7.0
PERT=${QE_DIR}/perturbo-dev-qe7/bin/qe2pert.x

# run the job
echo Job starts at `date`
#-------------------------------------------------------------

#hybrid OpenMP+MPI 
export OMP_PROC_BIND=true
export OMP_PLACES=threads
export OMP_STACKSIZE=64M

NUM_MPI=$SLURM_NTASKS
NUM_CPU=$SLURM_CPUS_PER_TASK
NUM_NODE=$SLURM_JOB_NUM_NODES
export OMP_NUM_THREADS=$NUM_CPU

CASE=qe2pert-tdep
srun -n ${NUM_MPI} -c ${NUM_CPU} $PERT -npools ${NUM_MPI} -i ${CASE}.in >${CASE}.out

echo Job ends at `date`
#-------------------------------------------------------------
