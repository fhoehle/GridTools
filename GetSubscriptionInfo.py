from PhEDExDatasvcInfo.PhEDExDatasvcInfo import PhEDExDatasvcInfo

import csv,getopt,sys

def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size

usage = 'python GetSubscriptionInfo.py --dataset=/TTbar/* (--output=output.csv)'

try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "dataset=","output="])
except getopt.GetoptError, err:
    print str(err) 
    print usage
    sys.exit(-1)

dataset = None
output=None

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print usage
        sys.exit(-1)
    elif opt in ("--dataset=="):
        dataset = arg.strip()
    elif opt in ("--output=="):
        output = arg.strip()
    else:
        assert False, "unhandled option"

if dataset==None:
    print usage
    sys.exit(-1)

phedex = PhEDExDatasvcInfo()
datasets = phedex.GetSubscriptionInfo(dataset)

csvfile=None

if output!=None:
    csvfile = csv.writer(open(output,"wb"))
    csvfile.writerow(["Dataset","Size","Node","Group"])

for dataset in datasets:
    for subscription in dataset["subscription"]:
        print dataset['name'],convert_bytes(dataset['bytes']),subscription["node"],subscription["group"]
        if csvfile!=None:
            csvfile.writerow([dataset['name'],convert_bytes(dataset['bytes']),subscription["node"],subscription["group"]])
        
        
