#!/usr/bin/env python
import sys,os
sys.path.append(os.getenv('CMSSW_BASE')+'/GridTools')
import DASclient.python.das_client as das_client
import urllib2,json
import PhEDExDatasvcInfo.PhEDExDatasvcInfo as PhEDExDatasvcInfo
########
optmgr  = das_client.DASOptionParser()
opts, _ = optmgr.get_opt()
host    = opts.host
debug   = opts.verbose
query   = opts.query
idx     = opts.idx
limit   = opts.limit
thr     = opts.threshold
ckey    = opts.ckey
cert    = opts.cert
das_h   = opts.das_headers
base    = opts.base
#############
import sys,re,subprocess,os
phedex = PhEDExDatasvcInfo.PhEDExDatasvcInfo()
targetAc='srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/fhohle//OfficialSamples'
targetDESY='srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/fhohle/OfficialSamples'
def main():
  nodetarget=targetAc
  print "called with ",sys.argv
  file = open(sys.argv[1])
  lines = [ l.strip('\n') for l in file.readlines()]
  myFileDicts=[]
  for line in lines:
    if not line.startswith('#'):
      filename = line.split()[2]
      datasetname = line.split()[0]
      if debug:
        print filename," ",datasetname
      foldername = re.sub('\/','__',datasetname.lstrip('\/'))
      filenameNew = re.match('.*\/([^\/]*\.root)',filename).group(1)
      targetFileName = nodetarget+"/"+foldername+"/"+filenameNew
      myFileDicts.append({"origin":filename,"target":targetFileName})
  copyStep = gridCopyFiles(myFileDicts,debug)
  copyStep.copy()
  copyStep.end()
###################
def copyLcg(origin,target,srmTimeout=30,debug=False):
  lcgCpCommand = "lcg-cp -v --srm-timeout "+str(srmTimeout)+" "+origin+" "+target
  if debug:
    print lcgCpCommand
  output = subprocess.Popen([lcgCpCommand],shell=True,stdout=subprocess.PIPE,env=os.environ)
  output.wait()
  return output.returncode
def srmls(target):
  dirname=os.path.dirname(target)
  print "listing ",dirname
  output = subprocess.Popen(['srmls '+dirname],shell=True,stdout=subprocess.PIPE,env=os.environ)
  output.wait()
  return output.communicate()[0]
class gridCopyFiles(object):
  def __init__(self,fileDicts,debug=False):
    self.fileDicts=fileDicts
    self.debug=debug
  def copy(self):
    self.failed = []
    totalFiles=len(self.fileDicts)
    for i,fdict in enumerate(self.fileDicts):
      print i,"/",totalFiles,
      origin = fdict["origin"]
      target = fdict["target"]
      if self.debug:
        print "origin ",origin," target ",target
      jsondict = das_client.get_data(host, "site file = "+origin, idx, limit, debug, thr, ckey, cert)
      nodes = [ str(ele.get('site')[0].get('name')) for ele in jsondict.get('data')]
      errorcode = "not done"
      for node in nodes:
        if self.debug:
          print "trying to download from ",node
          print origin
        srmPath = phedex.GetPFNFromLFN(node=node,lfn=origin)
        if self.debug:
          print srmPath
        errorcode = copyLcg(srmPath,target,debug=self.debug)
        print "ERRORCODE ",errorcode
        if errorcode == 0:
          break
        else: 
          self.failed.append(origin+" "+target)
          print "WARNING FAILED errorcode ",errorcode," ",origin
  def checking(self):
      totalFiles=len(self.fileDicts)
      for i,fdict in enumerate(self.fileDicts):
        print i,"/",totalFiles
        if not fdict.has_key("folder"):
          print "need folder for checking"
        folderName=fdict["folder"]
        lsOutput=srmls(fdict["target"])
        print "srmls output: ",lsOutput
        srmlsRe=re.match('.*?\n*\ *[0-9]*\ +'+'.*\/pnfs\/.*(\/store\/.*'+folderName+'\/*([^\/]*\.root\ *\n*.*))',lsOutput)
        if srmlsRe:
          print "found ",srmlsRe.group(2)
          print srmlsRe.group(1)
        else: 
          print "not found ",fdict["target"], fdict["d"] if fdict.has_key("d") else ""
  def end(self):
    for fail in self.failed:
      print "failed ",fail

if __name__ == "__main__":
  main()
