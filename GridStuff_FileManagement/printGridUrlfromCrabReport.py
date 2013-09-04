#!/usr/bin/env python
import getopt,sys,re,argparse
from xml.dom.minidom import *
# usage for file in $(ls crab_0_121012_230338/res/crab_fjr_*.xml); do ../FileManagment/trunk/printGridUrlfromCrabReport.py --xmlFile $file --useAnalysisFile | grep srm; done >& Ntuple_files.txt
def myGetSubNodeByName(node,name):
 if not node:
   return None
 if not hasattr(node,'childNodes'):
   return None
 for i,tmp_node in enumerate(node.childNodes):
  if tmp_node.nodeName == name:
   return tmp_node
 return None
parser = argparse.ArgumentParser()
parser.add_argument('--useAnalysisFile',action='store_true',default=False,help=' if Analysis File should be used')
parser.add_argument('--usePoolOutputFile',action='store_true',default=False,help=' if Poolouputmodule File should be used')
parser.add_argument('--xmlFiles',nargs='+',default=[],help=' list of input xmlFiles')
parser.add_argument('--debug',action='store_true',default=False,help=' debug on off')
parser.add_argument('--ignoreFailedJobs',action='store_true',default=False,help=' ignore jobs wichi are failed, output is less than number of jobs')
args=parser.parse_args()
if args.xmlFiles == [] or (args.useAnalysisFile and args.usePoolOutputFile) or (not args.usePoolOutputFile and not args.useAnalysisFile):
   parser.print_help()
   print "--useAnalysisFile OR --usePoolOutputFile"
   sys.exit(1)

for xmlFile in args.xmlFiles:
  dom = parse(xmlFile)
  fwkRep = dom.childNodes[0]
  # ExitCode
  exitCode = myGetSubNodeByName(fwkRep,"ExitCode")
  fwkExitCode =  myGetSubNodeByName(fwkRep,"FrameworkError")
  fwkExitCode = fwkExitCode.getAttribute("ExitStatus")
  if str(fwkExitCode) != "0":
    if not args.ignoreFailedJobs:
      sys.exit("not all finished/done "+xmlFile+" "+str(fwkExitCode))
    if args.debug:
      print "Error ",fwkExitCode
      print xmlFile
    continue
  if args.debug:
    print "ExitCode ",exitCode.getAttribute("Value")
  # output files
  if args.usePoolOutputFile:
   poolOutputFile = myGetSubNodeByName(fwkRep,"File")
   poolOutputFileGridUrl = myGetSubNodeByName(poolOutputFile,"SurlForGrid")
   if poolOutputFileGridUrl:
     mystring=str(poolOutputFileGridUrl.firstChild.nodeValue).strip()
     if mystring:
       print mystring
     else:
       print "error ",xmlFile
   else:
     print "error ",xmlFile
  if args.useAnalysisFile:
   analysisFile = myGetSubNodeByName(fwkRep,"AnalysisFile")
   analysisFileGridUrl = myGetSubNodeByName(analysisFile,"SurlForGrid")
   if analysisFileGridUrl:
     fileLoc = analysisFileGridUrl.getAttribute("Value") 
     test= re.sub('srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2\?SFN=','dcap://grid-dcap.physik.rwth-aachen.de',fileLoc) #dcap:\/\/grid-dcap\.physik\.rwth-aachen\.de',fileLoc)
     if test:
       print  test
     else:
       print "error ",xmlFile
   else:
    print "error ",xmlFile
