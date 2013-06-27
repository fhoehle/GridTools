#!/usr/bin/env python
import GridTools.DASclient.das_client as das_client
import urllib2,json
from PhEDExDatasvcInfo.PhEDExDatasvcInfo import PhEDExDatasvcInfo

def getCMSName(firstSite):
  cert = '/home/home2/institut_3b/hoehle/.globus/usercert.pem'
  ckey    = '/home/home2/institut_3b/hoehle/.globus/userkey.pem'
  hdlr = das_client.HTTPSClientAuthHandler(ckey,cert)
  opener = urllib2.build_opener(hdlr)
  headers = {"Accept": "application/json"}
  reqSiteRes  = urllib2.Request('https://cmsweb.cern.ch/sitedb/data/prod/site-resources', headers=headers)
  fdescSiteRes = opener.open(reqSiteRes)
  data = fdescSiteRes.read()
  fdesc = opener.open(req)
  dataSiteRes = fdescSiteRes.read()
  fdescSiteRes.close()
  jsondictSiteRes = json.loads(dataSiteRes)
  siteRes = jsondictSiteRes.get('result')
  #jsondict.keys()
  #jsondict.get('desc')
  for res in siteRes:
    if firstSite in res[2] and 'SE' in res[1]:
      print(res[0])
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
lines = [ l.strip('\n') for l in file.readlines()][:2]
phedex = PhEDExDatasvcInfo()
for line in lines:
  #output = ''
  if not line.startswith('#'):
    filename = line.split()[2]
    #print filename
    jsondict = das_client.get_data(host, "site file = "+filename, idx, limit, debug, thr, ckey, cert)
    node = str(jsondict.get('data')[0].get('site')[0].get('name'))
    srmPath = phedex.GetPFNFromLFN(node=node,lfn=filename)
    print srmPath
