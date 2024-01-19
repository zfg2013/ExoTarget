#!/bin/bash
# NOTE: Check your bash location and replace the line above with it. Keep the #!
# NOTE: You can run this by changing permissions so it's executable OR by running bash <scriptname> 

FEATURE=raw_features.csv

#extract from completed computes

for f in ~/blue_zfg2013/INPS/*.out
do 
# echo "Processing $f file.."
FILENAME=$(basename -- "$f")
{
  echo "${FILENAME%.*}";
  grep 'FINAL SINGLE POINT ENERGY' "$f" | tail -n1;
  grep 'GEPOL Volume' $f | tail -n1 >> $FEATURE;
  grep 'GEPOL Surface-area' $f | tail -n1 >> $FEATURE;
  grep 'Rotational constants in MHz' $f | tail -n1 >> $FEATURE;
  grep 'Total Dipole Moment' $f | tail -n1 >> $FEATURE;
} >> $FEATURE

done