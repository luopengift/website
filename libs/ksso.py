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


class SSO_API():
    def __init__(self,forward_url=None,sso_url='https://sso.shabi.com/'):
        self.sso_url = sso_url
        self.forward_url = forward_url
        self.context = ssl._create_unverified_context()

    @property
    def login_url(self):
        return '{sso_url}login?forward={forward_url}'.format(sso_url = self.sso_url,forward_url = self.forward_url)

    @property
    def logout_url(self):
        ret = "%slogout?forward=%s" % (self.sso_url,self.forward_url)
        return ret
    
    def k2sso_login(self,ticket):
        headers = {'referer': self.forward_url}
        res = requests.get("%sverify?t=%s" % (self.sso_url,ticket),headers=headers,verify=False)
        res = res.text
        return res

    def sso_login(self,ticket):
        request = urllib2.Request("%sverify?t=%s" % (self.sso_url,ticket))
        request.add_header("referer",self.forward_url)
        response = urllib2.urlopen(request,context=ssl._create_unverified_context())
        return response.read()



if __name__ =='__main__':
    pass
