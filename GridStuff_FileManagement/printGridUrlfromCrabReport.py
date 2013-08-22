#!/usr/bin/env python
import getopt,sys,re
from xml.dom.minidom import *
# usage for file in $(ls crab_0_121012_230338/res/crab_fjr_*.xml); do ../FileManagment/trunk/printGridUrlfromCrabReport.py --xmlFile $file --useAnalysisFile | grep srm; done >& Ntuple_files.txt
def myGetSubNodeByName(node,name):
 for i,tmp_node in enumerate(node.childNodes):
  if tmp_node.nodeName == name:
   return tmp_node
useAnalysisFile=False
usePoolOutputFile=False
opts, args = getopt.getopt(sys.argv[1:], 'h',['xmlFile=','usePoolOutputFile','useAnalysisFile'])
xmlFile=None
useAnalysisFile = False
for opt,arg in opts:
 #print opt , " :   " , arg
 if opt in  ("--xmlFile"):
  xmlFile=arg
 if opt in ("--useAnalysisFile"):
  useAnalysisFile = True
 if opt in ("--usePoolOutputFile"):
  usePoolOutputFile=True
 if opt in ("-h"):
  print "for file in $(ls crab_0_121012_230338/res/crab_fjr_*.xml); do ../FileManagment/trunk/printGridUrlfromCrabReport.py --xmlFile $file --useAnalysisFile | grep srm; done >& Ntuple_files.txt"
  sys.exit(0)
dom = parse(xmlFile)
if xmlFile == None or xmlFile =="" or (useAnalysisFile and usePoolOutputFile) or (not usePoolOutputFile and not useAnalysisFile):
 print "usage: $absolutePathtoXmlFile/xmlFile --useAnalysisFile OR --usePoolOutputFile"
 sys.exit(1)
fwkRep = dom.childNodes[0]
# ExitCode
exitCode = myGetSubNodeByName(fwkRep,"ExitCode")
print "ExitCode ",exitCode.getAttribute("Value")
# output files
if usePoolOutputFile:
 poolOutputFile = myGetSubNodeByName(fwkRep,"File")
 poolOutputFileGridUrl = myGetSubNodeByName(poolOutputFile,"SurlForGrid")
 mystring=str(poolOutputFileGridUrl.firstChild.nodeValue).strip()
 print mystring
if useAnalysisFile:
 analysisFile = myGetSubNodeByName(fwkRep,"AnalysisFile")
 analysisFileGridUrl = myGetSubNodeByName(analysisFile,"SurlForGrid")
 fileLoc = analysisFileGridUrl.getAttribute("Value") 
 test= re.sub('srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2\?SFN=','dcap://grid-dcap.physik.rwth-aachen.de',fileLoc) #dcap:\/\/grid-dcap\.physik\.rwth-aachen\.de',fileLoc)
 print  test
 
