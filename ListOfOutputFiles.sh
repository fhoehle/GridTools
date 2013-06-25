#!/bin/bash

#This script copies files from dCache. 
dCachePath=/pnfs/physik.rwth-aachen.de/cms/store/user/kuessel/
echo -e " \n  \n  **** Welcome to this little script to extract list of files which are located in the dCache! **** \n \n Do you want to use it in edmCopyPickMerge then type \"pick\". If make a list for bTaggingCommisioining type \"list\". If you want to use it in a CMSSW config type \"other\"."
read edmCopyPickMerge

echo -e " \n \n   If you want to change the DCache-path: "$dCachePath " then type \"yes\"."
read newPath
if [ "$newPath" = "yes" ]; then
                echo "Enter new path..."
		read dCachePath
fi

echo  -e " \n These are all files in that directoy:"

srmls srm://grid-srm:8443/srm/managerv2?SFN=$dCachePath

echo -e " \n Please enter the identifier."
read identifier

echo -e "\n If you want to make a list of files from \"" $dCachePath "\" which contain the word \"" $identifier "\"type ENTER."
read OK

{
  for file in `srmls srm://grid-srm:8443/srm/managerv2?SFN=$dCachePath  | awk '{print $2}' | grep $identifier`; do

   if [ "$edmCopyPickMerge" = "pick" ]; then
       echo -e ${file#/pnfs/physik.rwth-aachen.de/cms}
   fi
   if [ "$edmCopyPickMerge" = "list" ]; then
       echo -e ${file}
   fi
   if [ "$edmCopyPickMerge" = "other" ] ; then
       echo -e "'"${file#/pnfs/physik.rwth-aachen.de/cms}"',"
   fi

  done
} > "listOfOutputFiles"


echo -e "\n List with name 'listOfOutputFiles' created.' \n \n ***** THE END ******"