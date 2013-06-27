#!/usr/bin/env python
import sys,re,subprocess,os
addExampleFile = True
print "called with ",sys.argv
file = open(sys.argv[1])
fileRe = re.match('(.*)(\.[^\.]*)',sys.argv[1])
outputFile = open(fileRe.group(1)+"_numEvents"+fileRe.group(2),'w')
lines = [ l.strip('\n') for l in file.readlines()] #[:2]
for line in lines:
  if not line.startswith('#'):
    dbsCommand='"find dataset , sum(block.numevents) where dataset = '+line+'"'
    print dbsCommand
    output = subprocess.Popen(["dbsql "+dbsCommand+" | grep AODSIM"],shell=True,stdout=subprocess.PIPE,env=os.environ).communicate()[0].strip('\n')
  else:
    output = line
  if addExampleFile:
    dbsCommand='"find file , file.numevents where dataset = '+line+'"'
    output.strip('\n') 
    output += "  "+subprocess.Popen(["dbsql "+dbsCommand+" | grep root | awk 'NR==1'"],shell=True,stdout=subprocess.PIPE,env=os.environ).communicate()[0].strip('\n')
  outputFile.write(output+'\n')
outputFile.close()
