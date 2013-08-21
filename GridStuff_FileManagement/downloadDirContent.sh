#!/bin/bash
directoryAdress=$1
echo "downloading directory's "$directoryAdress"content"
directoryPath=`echo $directoryAdress | sed 's/.*srm.*?SFN=\(\/.*\)/\1/'`
sitePrefix=`echo $directoryAdress | sed 's/\(.*srm.*?SFN=\)\/.*/\1/'`
export IFS=$'\n'
echo $directoryPath "  directoryPath"
for filePath in $(srmls $directoryAdress | grep $directoryPath\/*[^\/] | awk '{print $2}'); do
 filename=`echo $filePath | sed 's/.*\/\([^\/][^\/]*\)/\1/'`
 echo "downloading "$filePath" "$filename;
 echo "lcg-cp $sitePrefix$filePath $filename"
 lcg-cp $sitePrefix$filePath $filename
done
unset IFS
