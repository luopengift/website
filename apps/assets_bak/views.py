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

class Server(BaseHandler):
    #@unblock
    def get(self):
        self.render2('/assets/assets.html')
        #self.finish()






class Users(BaseHandler):
    def get(self):
        pass




