#!/usr/bin/env python
# -*- coding: utf8 -*-
#from torndb import Connection
import requests
import ssl
import urllib,urllib2
import os,sys
import yaml
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

cur_dir = os.path.dirname(os.path.abspath(__file__))


class KSSO_API():
    def __init__(self,forward_url=None,ksso_url='https://ksso.kisops.com/'):
        self.ksso_url = ksso_url
        self.forward_url = forward_url
        self.context = ssl._create_unverified_context()

    @property
    def login_url(self):
        return '{ksso_url}login?forward={forward_url}'.format(ksso_url = self.ksso_url,forward_url = self.forward_url)

    @property
    def logout_url(self):
        ret = "%slogout?forward=%s" % (self.ksso_url,self.forward_url)
        return ret
    
    def k2sso_login(self,ticket):
        headers = {'referer': self.forward_url}
        res = requests.get("%sverify?t=%s" % (self.ksso_url,ticket),headers=headers,verify=False)
        res = res.text
        return res

    def ksso_login(self,ticket):
        request = urllib2.Request("%sverify?t=%s" % (self.ksso_url,ticket))
        request.add_header("referer",self.forward_url)
        response = urllib2.urlopen(request,context=ssl._create_unverified_context())
        return response.read()



if __name__ =='__main__':
    pass
