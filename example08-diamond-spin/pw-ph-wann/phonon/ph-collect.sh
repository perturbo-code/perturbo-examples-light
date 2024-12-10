#!/bin/bash

# Get the PREFIX from ph-ref.in
PREFIX=`awk -F= '{if($0~"prefix") print $NF}' ph-ref.in | sed "s/'//g" | sed 's/"//g'`

#should be in the work directory of PHonon calculation
echo `pwd`
mkdir -p save/${PREFIX}.phsave

for q_folder in ph-*/;
do
   NQ=`echo $q_folder | sed 's/\///' | awk 'BEGIN{FS="-"}{print $NF}'`
   DIR="$q_folder/tmp/_ph0"
   echo Collecting from $DIR

   #copy prefix.phsave
   cp ${DIR}/${PREFIX}.phsave/* save/${PREFIX}.phsave/

   #copy dyn files
   cp ${q_folder}/${PREFIX}.dyn${NQ}.xml save/  #${PREFIX}.dyn_q${NQ}
   cp ${q_folder}/${PREFIX}.dyn* ./

   #copy dvscf files
   cp ${DIR}/${PREFIX}.q_${NQ}/${PREFIX}.dvscf1 save/${PREFIX}.dvscf_q${NQ}
done
