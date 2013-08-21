#!/bin/bash
LogFile="missing.txt_tmp_"`date +"%m%d%H%M%S"`
if [ "$1" == "" ]; then
 num=500
else
 num=$1
fi
for num in $(seq 1 1 $num); do filename=`ls NTuple_$(echo $num)_*root 2> /dev/null | wc -l`; if [ "$filename" == "0" ] ; then echo "$num"; fi; done >& $LogFile
if [ -f missing.txt ]; then
 echo "missing.txt already exists"
 echo "results saved in "$LogFile
else
 mv $LogFile missing.txt
fi
 
