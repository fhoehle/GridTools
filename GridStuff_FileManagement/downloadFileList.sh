#!/bin/bash
fileList=$1
echo "using this fileList $fileList"
for file in $(cat $fileList); do fileName=`echo $file | sed 's/^.*\/\([^\/]*root\)$/\1/'`; echo "copying $fileName"; lcg-cp $file $fileName;  done
