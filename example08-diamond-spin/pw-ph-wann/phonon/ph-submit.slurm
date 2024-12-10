#!/bin/bash
#SBATCH -N 2                        # Number of nodes, MUST be 1
#SBATCH --ntasks-per-node=64 	    # MPI tasks per node
#SBATCH -p long         	    # queue type (regular | debug | large | long)
#SBATCH -J phonon            	    # job name
#SBATCH -t 168:00:00          	    # time limit

# In the following, "comment" means put more then one hash, uncomment means leave only one hash

# ===FIRST===, run the gamma point, find the number of q-points nq
###SBATCH --array=1-1%1             # Number of job array tasks

# ===SECOND===, comment the SBATCH line above and uncomment below,
# modify NQ to the number of q points
#SBATCH --array=1-8%4            #Number of job array tasks

#SBATCH --output=slurm-%A_%a.log # Output file for each array TASK

# Get the PREFIX from ph-ref.in
PREFIX=`awk -F= '{if($0~"prefix") print $NF}' ph-ref.in | sed "s/'//g" | sed 's/"//g'`

SUBJOB='qe-ph-v70.sh'

# First, we need to test the convergence of dielectric tensor
# which is computed when q=0 w.r.t k-grid.
# the converged k-grid is then used in othe q points.

mode="gamma"

# Iterate over q points using the job array task ID
NQ=$SLURM_ARRAY_TASK_ID

DIR=ph-$NQ
echo $DIR
mkdir -p $DIR

cd $DIR

#-------------------------------------------------------------
#change ph.in
cp ../ph-ref.in  ./ph.in
sed -i   "s|.*prefix.*|  prefix='${PREFIX}'|g"      ph.in
sed -i   "s|.*fildyn.*|  fildyn='${PREFIX}.dyn.xml'|g"  ph.in
sed -i  "s|.*start_q.*|  start_q= ${NQ}|g"  ph.in
sed -i   "s|.*last_q.*|  last_q = ${NQ}|g"  ph.in

#-------------------------------------------------------------
#change the phonon script
cp ../${SUBJOB} ./
sed -i  "s|.*test-ph.*|#SBATCH -J \"${PREFIX}-ph-q${NQ}\"|g" ${SUBJOB}
#sed -i  "s|.*test-ph.*|#PBS -N ${PREFIX}-ph-q${NQ}|g" ${SUBJOB}
sed -i  "s|.*NQ=.*|NQ=${NQ}|g" ${SUBJOB}
sed -i  "s|.*PREFIX=.*|PREFIX=${PREFIX}|g" ${SUBJOB}

# different dir in q=0 calculation.
#if [ "$NQ" == "1" ]; then
#   sed -i "s|.*DPATH=.*| DPATH='.' |g" ${SUBJOB}
#fi

#-------------------------------------------------------------
# run the phonon script
bash ${SUBJOB}
echo Done $DIR

# done, return to upper directory.
cd ..
