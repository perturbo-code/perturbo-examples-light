#!/bin/bash

PREFIX='si'

#mode='gamma'

SUBJOB='qe-ph.pbs'

HERE=`pwd`
for ((NQ=1; NQ<=29; NQ++ ))
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
   sed -i  "s|#PBS -N pert-ph|#PBS -N ${PREFIX}-ph-q${NQ}|g" ${SUBJOB}
   sed -i  "s|.*test-ph.*|#PBS -N ${PREFIX}-ph-q${NQ}|g" ${SUBJOB}
   sed -i  "s|.*NQ=.*|NQ=${NQ}|g" ${SUBJOB}
   sed -i  "s|.*PREFIX=.*|PREFIX=${PREFIX}|g" ${SUBJOB}
   # different dir in q=0 calculation.
   if [ "$NQ" == "1" ]; then
      sed -i "s|.*DPATH=.*| DPATH='.' |g"  ${SUBJOB}
   fi
   # submit
   qsub ${SUBJOB}
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
