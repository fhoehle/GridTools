#!/usr/bin/env python

from PhEDExDatasvcInfo.PhEDExDatasvcInfo import PhEDExDatasvcInfo

import getopt,sys

usage = "python GetRequestInfo --node=T2_XY_ABCD --dataset=/PrimaryDataset/SecondaryDataset/DATATIER"

try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "node=","dataset="])
except getopt.GetoptError, err:
    print str(err) 
    print usage
    sys.exit(-1)

node=None
dataset=None

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print usage
        sys.exit(-1)
    elif opt in ("--node=="):
        node = arg.strip()
    elif opt in ("--dataset=="):
        dataset = arg.strip()
    else:
        assert False, "unhandled option"

if node==None or dataset==None:
    print usage
    sys.exit(-1)


phedex=PhEDExDatasvcInfo()

print phedex.GetRequestInfo(node=node,dataset=dataset)
