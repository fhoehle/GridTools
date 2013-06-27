#!/usr/bin/env python
import GridTools.DASclient.das_client as das_client
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
print "called with ",sys.argv
file = open(sys.argv[1])
lines = [ l.strip('\n') for l in file.readlines()]
phedex = PhEDExDatasvcInfo.PhEDExDatasvcInfo()
srmTimeout = 30
targetAc='srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/fhohle//OfficialSamples'
maxNum = len(lines)
failed = []
for i,line in enumerate(lines):
  #output = ''
  print i,"/",maxNum," ",line
  if not line.startswith('#'):
    filename = line.split()[2]
    datasetname = line.split()[0]
    print filename,"  ",datasetname
    #print filename
    jsondict = das_client.get_data(host, "site file = "+filename, idx, limit, debug, thr, ckey, cert)
    nodes = [ str(ele.get('site')[0].get('name')) for ele in jsondict.get('data')]
    errorcode = "not done"
    for node in nodes:
      print "trying to download from ",node
      print filename
      srmPath = phedex.GetPFNFromLFN(node=node,lfn=filename)
      foldername = re.sub('\/','__',datasetname.lstrip('\/'))
      filenameNew =  re.match('.*\/([^\/]*\.root)',filename).group(1)
      print srmPath
      lcgCpCommand = "lcg-cp -v --srm-timeout "+str(srmTimeout)+" "+srmPath+" "+targetAc+"/"+foldername+"/"+filenameNew
      print lcgCpCommand
      output = subprocess.Popen([lcgCpCommand],shell=True,stdout=subprocess.PIPE,env=os.environ)
      output.wait()
      errorcode = output.returncode
      if errorcode == 0:
        break
    if errorcode != 0:
      failed.append(line)
      print "WARNING FAILED errorcode ",errorcode," ",filename
for fail in failed:
  print "failed ",fail
