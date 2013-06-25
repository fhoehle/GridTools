from xml.dom.minidom import parse

import urllib,urllib2

try:
    import json
except:
    import simplejson as json

class PhEDExDatasvcInfo:

    def __init__(self,datasvc_url="https://cmsweb.cern.ch/phedex/datasvc",format="json",instance="prod"):
        self.format=format
        self.url = datasvc_url+'/'+self.format+'/'+instance

    def __GetDomFromPhedex(self,parameters,api):  

        SupportedAPIs = ['lfn2pfn']

        if api not in SupportedAPIs:
            msg="API %s is currently not supported." % (api)
            raise PhEDExDatasvcInfo,msg
    
        parameters = urllib.urlencode(parameters)

        try:
            urlresults = urllib22.urlopen(self.url+'/'+api, parameters)
            urlresults = parse(urlresults)
        except IOError:
            msg="Unable to access PhEDEx Data Service at %s with given API %s" % (self.url,api)
            raise PhEDExDatasvcInfo,msg

        return urlresults

    def __GetJSONFromPhedex(self,parameters,api):

        SupportedAPIs = ['lfn2pfn','subscriptions','RequestList','transferrequests']

        if api not in SupportedAPIs:
            msg="API %s is currently not supported." % (api)
            raise PhEDExDatasvcInfo,msg
    
        parameters = urllib.urlencode(parameters)

        #try:
        urlresults = urllib.urlopen(self.url+'/'+api, parameters)
        urlresults = json.load(urlresults)
        #except IOError:
        #    msg="Unable to access PhEDEx Data Service at %s with given API %s" % (self.url,api)
        #    raise PhEDExDatasvcInfo,msg

        return urlresults

    def GetPFNFromLFN(self,node,lfn,protocol='srmv2'):
        parameters = {'node' : node , 'lfn': lfn , 'protocol': protocol}

        if self.format == "xml":

            domresults = self.__GetDomFromPhedex(parameters,'lfn2pfn')
            
            result = domresults.getElementsByTagName('phedex')

            if not result:
                return []

            result = result[0]
            pfn = None
            mapping = result.getElementsByTagName('mapping')

            for i in mapping:
                pfn=i.getAttribute("pfn")
                if pfn:
                    return pfn

        elif self.format == "json":
            jsondict = self.__GetJSONFromPhedex(parameters,'lfn2pfn')

            for i in jsondict['phedex']['mapping']:
                try:
                    return i['pfn']
                except:
                    pass

        else:
            return None

    def GetSubscriptionInfo(self,dataset):
        parameters = {'dataset' : dataset}

        if self.format == "json":
            jsondict = self.__GetJSONFromPhedex(parameters,'subscriptions')

            return jsondict['phedex']['dataset']

        else:
            return None

    def GetRequestInfo(self,**kargs):
       
        if self.format == "json":
            jsondict = self.__GetJSONFromPhedex(kargs,'RequestList')
            return jsondict['phedex']['request']
        else:
            return None
        
    def GetSubscriptionsInfo(self,node,group):
        parameters = {'node' : node, 'group' : group}

        if self.format == "json":
            jsondict = self.__GetJSONFromPhedex(parameters,'subscriptions')

            return jsondict['phedex']['dataset']

        else:
            return None

    def GetTransferRequestInfo(self,**kargs):

        if self.format == "json":
            jsondict = self.__GetJSONFromPhedex(kargs,'transferrequests')
            return jsondict['phedex']['request']
        else:
            return None

            
