#!/usr/bin/env python
#-*-coding:utf8-*-

from tornado.httpclient import AsyncHTTPClient,HTTPRequest

from control.BaseHandler import BaseHandler
from control.unblock import unblock

#from libs.logger import logging

import urllib
import time

import hmac

#from python_hmac_auth import HmacAuth
from libs.httpclient import httpResponse

HTTPurl = 'http://10.33.20.155/openapi'


def HmacMD5(key,string):
    myhmac = hmac.new(key)
    myhmac.update(string)
    return myhmac.hexdigest().upper()



class AuthHandler(BaseHandler):
    @unblock
    def get(self):
        if True:
            sid = self.get_argument('sid','')
            data = {
                'sid':sid,
                "sig_method":"HmacMD5",
                'systemAlias':'10.33.20.49',
                'systemDomain':'yunwei.cmcm.com',
                'access_key':'test',
                #'accessKey':'test',
                #'secret':'test',
                'cmd':'cheetah.singleLogin',
                'timestamp':str(int(time.time()*1000)),
            }
            sortdata = sorted(data.iteritems(), key=lambda d:d[0])
            secretstr = 'test'+''.join(map(lambda x:''.join(x),sortdata))
            md5 =  HmacMD5('test',secretstr)
            data['sig']=md5
            url = HTTPurl+'?%s'% urllib.urlencode(data)
            resp = httpResponse(url,'GET')
            self.write(resp[1])
        self.finish()


    @unblock
    def post(self):
        try:
            print self.request.body
            result=self.request.body
            self.write(result)
        except Exception as e:
            logging.exception('Exception')
             
        finally:
            self.finish()


