#!/usr/bin/env python
import sys,re,argparse,os
import xml.dom.minidom as minidom
# usage for file in $(ls crab_0_121012_230338/res/crab_fjr_*.xml); do ../FileManagment/trunk/printGridUrlfromCrabReport.py --xmlFile $file --useAnalysisFile | grep srm; done >& Ntuple_files.txt
sys.path.append(os.getenv('CMSSW_BASE')+os.path.sep+'MyCMSSWAnalysisTools')
from CrabTools import myGetSubNodeByName
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--useAnalysisFile',action='store_true',default=False,help=' if Analysis File should be used')
  parser.add_argument('--usePoolOutputFile',action='store_true',default=False,help=' if Poolouputmodule File should be used')
  parser.add_argument('--xmlFiles',nargs='+',default=[],help=' list of input xmlFiles')
  parser.add_argument('--debug',action='store_true',default=False,help=' debug on off')
  parser.add_argument('--printDcapPath',action='store_true',default=False,help=' return dcapPath defualt is srm')
  parser.add_argument('--ignoreFailedJobs',action='store_true',default=False,help=' ignore jobs wichi are failed, output is less than number of jobs')
  args=parser.parse_args()
  if args.xmlFiles == [] or (args.useAnalysisFile and args.usePoolOutputFile) or (not args.usePoolOutputFile and not args.useAnalysisFile):
     parser.print_help()
     print "--useAnalysisFile OR --usePoolOutputFile"
     sys.exit(1)
  print "\n".join(getFileNames(args.useAnalysisFile,args.usePoolOutputFile,args.ignoreFailedJobs,args.xmlFiles,args.debug,args.printDcapPath).values())
def getFileNames(useAnalysisFile,usePoolOutputFile,ignoreFailedJobs,xmlFiles,debug,printDcapPath):  
  fileNames={}
  import re
  for xmlFile in xmlFiles:
    dom = minidom.parse(xmlFile)
    jobNum = re.match('.*/crab_fjr_([0-9]+)\.xml',xmlFile).group(1) 
    fwkRep = myGetSubNodeByName(dom,"FrameworkJobReport")#dom.childNodes[0]
    if fwkRep.getAttribute("Status") != "Success" :
      if not ignoreFailedJobs:
        sys.exit("jobReport said not successful "+fwkRep.getAttribute("Status")+" "+xmlFile)
      if debug:
        print "jobFailed"
       
    # ExitCode
    exitCode = myGetSubNodeByName(fwkRep,"ExitCode")
    fwkExitCode =  myGetSubNodeByName(fwkRep,"FrameworkError")
    fwkExitCode = fwkExitCode.getAttribute("ExitStatus")
    if str(fwkExitCode) != "0":
      if not ignoreFailedJobs:
        sys.exit("not all finished/done "+xmlFile+" "+str(fwkExitCode))
      if debug:
        print "Error ",fwkExitCode
        print xmlFile
      continue
    if debug:
      print "ExitCode ",exitCode.getAttribute("Value")
    # output files
    if usePoolOutputFile:
     poolOutputFile = myGetSubNodeByName(fwkRep,"File")
     poolOutputFileGridUrl = myGetSubNodeByName(poolOutputFile,"SurlForGrid")
     if poolOutputFileGridUrl:
       poolOutputLoc = str(poolOutputFileGridUrl.firstChild.nodeValue).strip()
       if printDcapPath:
         poolOutputLoc = re.sub('srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2\?SFN=','dcap://grid-dcap.physik.rwth-aachen.de',fileLoc)
       if poolOutputLoc:
         fileNames[jobNum] = poolOutputLoc
       else:
         print "error ",xmlFile
     else:
       print "error ",xmlFile
    if useAnalysisFile:
     analysisFile = myGetSubNodeByName(fwkRep,"AnalysisFile")
     analysisFileGridUrl = myGetSubNodeByName(analysisFile,"SurlForGrid")
     if analysisFileGridUrl:
       fileLoc = analysisFileGridUrl.getAttribute("Value") 
       if printDcapPath:
         fileLoc = re.sub('srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2\?SFN=','dcap://grid-dcap.physik.rwth-aachen.de',fileLoc) #dcap:\/\/grid-dcap\.physik\.rwth-aachen\.de',fileLoc)
       if fileLoc:
         fileNames[jobNum]=fileLoc
       else:
         print "error ",xmlFile
     else:
      print "error ",xmlFile
    sys.stdout.flush()
  return fileNames
###############
if __name__ == "__main__":
  main()
