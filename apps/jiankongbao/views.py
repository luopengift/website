#!/usr/bin/env python
#-*-coding:utf8-*-
from control.BaseHandler import BaseHandler
from control.unblock import unblock

import urllib
import time
import json
import hmac

from libs.httpclient import httpResponse
from libs.hash import HmacMD5

class Resource(BaseHandler):
    @unblock
    def get(self,method):
        if method not in ['create','update','delete','read']:
            self.write('method error!')
        else:
            self.write('method is %s'%method)
            pass
        self.finish()


    @unblock
    def post(self,method):
        if method == 'create':
            self.create()
        self.finish()

    def create(self):
        result = json.loads(self.request.body)
        result['uid'] = HmacMD5('jkbtest',str(time.time())+result.get('user','default'))
        self.write(result)

class User(BaseHandler):
    def get(self):
        self.write('User get')

    def post(self):
        pass


'''
{'channel':xxx,'remote':'xxx','recv':'xxxx','time':‘xxx’,'msg':'xxxx','type':'xxxx','errcode':0}

errortype=
0:success

'''
class Send(BaseHandler):
    def get(self):
        pass
    def post(self):
        headers = json.loads(self.request.headers)
        data = json.loads(self.request.body)
        
        self.write(headers)
        self.write(data)
        self.render2('base.html')

        pass

        












