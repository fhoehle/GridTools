#!/bin/bash

#This script copies files from other Tier 2.

echo -e " \n  \n  **** Welcome to this little script to copy files from another Tier2! **** \n \n    The ingredients will be checked out (cvs co UserCode/RWTH3b/GridTools
). If you are ok with it type ENTER"
read ENTER

cvs co UserCode/RWTH3b/GridTools

cd UserCode/RWTH3b/GridTools

echo -e " \n \n I is necessary that you have a valid proxy so it will be now generated (voms-proxy-init --voms cms)."
voms-proxy-init --voms cms

echo -e " \n Setup will be sourced...."

source setup.sh

echo -e " \n Please enter the dbs name of the dataset or parts of it."
read DBSNAME

echo -e " \n ... Checking dbs if exists... \n "

dbsql "find dataset where dataset like *$DBSNAME*"

echo -e " \n Please enter the full dbs name."
read DBSNAMEFULL

echo -e " \n ... Searching for the site name... \n "

dbsql "find site where dataset like *$DBSNAMEFULL*"

echo -e " \n Please enter the site you want to copy from. You need to copy the site name abcdef.gh in the webbrowser address: https://cmsweb.cern.ch/sitedb/json/index/SEtoCMSName?name=abcdef.gh. Then enter the T2_XY_ABCD."
read T2_XY_ABCD

echo -e " \n ... Searching for the file names... \n "

dbsql "find file where dataset like *$DBSNAMEFULL*"

echo -e " \n Please enter the filename e.g./store/data/Commissioning10/MinimumBias/RECO/May6thReReco-v1/0116/D8766FDD-3A5C-DF11-BCF1-00261894394B.root. which you want to copy. \n "
read filename

echo -e "\n This will print the complete srm-path of the desired file."

SRMPATH=`python2.6 GetSRMURLfromLFN.py --cmsname=$T2_XY_ABCD --lfn=$filename`

echo -e "Please type in a destination path e.g. /user/kuessel/CMSSW/..."
read DestinationPath

echo -e "Please type in the new filename. If it should be the same as the initial name just type a '.' ."
read destinationfile

echo -e "\n \n  Now the file will be copied."

srmcp -2 $SRMPATH file:///$DestinationPath/$destinationfile

echo -e " \n \n \t ************* THE END ****************"

