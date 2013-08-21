#!/usr/bin/env python
import getopt,sys
from xml.dom.minidom import *

def myGetSubNodeByName(node,name):
 for tmp_node in node.childNodes:
  if tmp_node.nodeName == name:
   return tmp_node

opts, args = getopt.getopt(sys.argv[1:], '',['xmlFile='])
xmlFile=None
for opt,arg in opts:
 #print opt , " :   " , arg
 if opt in  ("--xmlFile"):
  xmlFile=arg

dom = parse(xmlFile)

fwkRep = dom.childNodes[0]
analysisFile = myGetSubNodeByName(fwkRep,"AnalysisFile")
analysisFileGridUrl = myGetSubNodeByName(analysisFile,"SurlForGrid")
print analysisFileGridUrl.getAttribute("Value")
