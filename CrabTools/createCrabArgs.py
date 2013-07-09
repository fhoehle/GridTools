import sys,os,commands,StringIO
def MakeString(maxEvents,inputFile,jobId):
 return '  <Job MaxEvents="'+str(maxEvents)+'"  InputFiles="'+inputFile+'"  SkipEvents="0"    FirstLumi="'+str(jobId)+'" JobID="'+str(jobId)+'" >\n  </Job>\n'
argsCrab='<arguments>\n'
jobIdx=1
dcachepath='/pnfs/physik.rwth-aachen.de/cms'
dcachefolder='/store/user/htholen/raw_lhef_20130708/'
dcacheprefix='srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN='
filetype='lhef$'
filename='ttA-8895037'
dcacheContent=commands.getoutput('srmls '+dcacheprefix+dcachepath+dcachefolder+' | grep '+filetype+' | awk \'{print $2}\' | sed \'s/^.*\\('+filename+'.*[0-9][0-9]*.'+filetype+'\\)$/\\1/\'')
#print 'srmls ',dcacheprefix+dcachepath+dcachefolder
dcacheList=StringIO.StringIO(dcacheContent)
print "len ",len(dcacheContent.split())
for file in dcacheContent.split():
 if filename in file:
  argsCrab+=MakeString("-1",dcachefolder+file,jobIdx)
  jobIdx+=1
 print file
argsCrab+='</arguments>'
print "create XML"
print "created ",jobIdx-1,"  jobs"
#rint folderContent
outfile=open("arguments.xml","w")
outfile.write(argsCrab)
outfile.close()
