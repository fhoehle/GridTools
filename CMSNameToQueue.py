#!/usr/bin/env python

from SiteDB.SiteDB import SiteDBJSON
import ldap as ldap

import getopt,sys

def main():

    usage = "python CMSNameToQueue.py --cmsname=T2_XY_ABCDE"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "cmsname="])
    except getopt.GetoptError, err:
        print str(err) 
        print usage
        sys.exit(-1)

    cmsname = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print usage
            sys.exit(-1)
        elif opt in ("--cmsname=="):
            cmsname = arg.strip()
        else:
            assert False, "unhandled option"

    if cmsname==None:
        print usage
        sys.exit(-1)

    siteDBAPI = SiteDBJSON()

    try:
        response = siteDBAPI.getJSON("CMSNametoCE", name=cmsname)
    except:
        raise

    for entry,ce in response.items():
        try:
            filter = "(&(objectclass=gluece)(GlueCEInfoHostName="+(ce['name'])+")(GlueCEAccessControlBaseRule=VO:cms))"
            ldapCon = ldap.initialize("ldap://lcg-bdii.cern.ch:2170/")
            results = ldapCon.search_s("Mds-Vo-name=local,o=grid",2,filter,["GlueCEUniqueID"])
            print results[0][1]['GlueCEUniqueID'][0]
        except:
            raise 

if __name__ == '__main__':
    main()
