#!/bin/bash

PREFIX='si'

#mode='gamma'

SUBJOB='qe-slurm-ph-v64-job-script'

HERE=`pwd`

# Please modify the following number according to your demand
for ((NQ=1; NQ<=8; NQ++ ))
#for ((NQ=2; NQ<=8; NQ++ ))
do
   DIR=ph-$NQ
   echo $DIR
   mkdir -p $DIR
   
   cd $DIR

   #change ph.in
   cp ../ph-ref.in  ./ph.in
   sed -i   "s|.*prefix.*|  prefix='${PREFIX}'|g"      ph.in
   sed -i   "s|.*fildyn.*|  fildyn='${PREFIX}.dyn.xml'|g"  ph.in
   sed -i  "s|.*start_q.*|  start_q= ${NQ}|g"  ph.in
   sed -i   "s|.*last_q.*|  last_q = ${NQ}|g"  ph.in

   #change submission script
   cp ../${SUBJOB} ./
   sed -i  "s|#SBATCH -J ph-ref|#SBATCH -J ${PREFIX}-ph-q${NQ}|g" ${SUBJOB}

   # soft link to prefix.save directory from the scf calculations
   mkdir tmp
   cd tmp
   ln -sf ../../tmp/${PREFIX}.save
   cd ../

   # submit 
   sbatch ${SUBJOB}
   
   echo Done $DIR
   # wait for a short period of time.
   #done, return to upper directory.
   cd ..
   
   # for gamma point only
   if [ "$NQ" == "1" ] && [ "$mode" == "gamma" ]; then
      break
   fi

   sleep 1
done
