#!/bin/bash

PREFIX='si'

#should be in the work directory of PHonon calculation
echo `pwd`
mkdir -p save 
mkdir -p save/${PREFIX}.phsave

for ((NQ=1; NQ<=29; NQ++ ))
do
   DIR="ph-$NQ/tmp/_ph0"
   echo $DIR
   #copy prefix.phsave
   cp ${DIR}/${PREFIX}.phsave/* save/${PREFIX}.phsave/
   #copy dyn files
   #cp ph-${NQ}/${PREFIX}.dyn${NQ} save/  #${PREFIX}.dyn_q${NQ}
   cp ph-${NQ}/${PREFIX}.dyn* save/
   #copy dvscf files
   cp ${DIR}/${PREFIX}.q_${NQ}/${PREFIX}.dvscf1 save/${PREFIX}.dvscf_q${NQ}
done
