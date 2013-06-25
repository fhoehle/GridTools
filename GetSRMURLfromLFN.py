#!/usr/bin/env python

from PhEDExDatasvcInfo.PhEDExDatasvcInfo import PhEDExDatasvcInfo

import getopt,sys

usage = "python GetSRMURLfromLFN.py --cmsname=T2_XY_ABCDE --lfn=/store/user/AliBaba/..."

try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "cmsname=","lfn="])
except getopt.GetoptError, err:
    print str(err) 
    print usage
    sys.exit(-1)

cmsname = None
lfn=None

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print usage
        sys.exit(-1)
    elif opt in ("--cmsname=="):
        cmsname = arg.strip()
    elif opt in ("--lfn=="):
        lfn = arg.strip()
    else:
        assert False, "unhandled option"

if cmsname==None or lfn==None:
    print usage
    sys.exit(-1)

phedex = PhEDExDatasvcInfo()
    
print phedex.GetPFNFromLFN(node=cmsname,lfn=lfn)




