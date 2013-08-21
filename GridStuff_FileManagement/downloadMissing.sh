#!/bin/bash
missingFile=$1
ntupleFile=$2
for num in $(less $missingFile); do gridName=`less $ntupleFile| grep "_$(echo $num)_[0-9]_[[:alnum:]]\{3\}\.root"`; filename=`echo $gridName | sed 's/.*\/\([^\/]*root\)$/\1/'`;echo "copying $filename"; lcg-cp $gridName $filename; done

