#!/usr/bin/env python
#-*-coding:utf8-*-

import os
import tornado
from control.BaseHandler import BaseHandler
from control.unblock import unblock
import bson
import json
import time
import requests
from .model import *
from .opslog import ops_log
from libs.api.weixin.messages import SendMsg



def api_music(keyword):
    
    url = 'http://s.music.163.com/search/get/'
    params = {'src':'lofter','type':1,'filterDj':True,'s':keyword,'limit':10,'offset':0}
    response = requests.get(url,params=params).json()
    if response['code'] == 200:
        return response['result']['songs'][0]
    return False


def xml2dict(xml_string):
    try: 
        import xml.etree.cElementTree as ET 
    except ImportError: 
        import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(xml_string)
    except Exception, e: 
        print str(e)
    else:
        return {child.tag:child.text for child in root.iter()}


class WeiXin(BaseHandler):
    def get(self):
        print self.request.arguments
        signature = self.get_query_argument('signature','')
        echostr = self.get_query_argument('echostr','')
        '''
        import hashlib
        str_list = [self.token, timestamp, nonce]
        str_list.sotr()
        combind_str = ''.join(str_list)
        encrypt_str = hashlib.sha1(combind_str).hexdigest()
        if encrypt_str == signature:
            return True
        return False
        '''

        self.write(echostr)

    @unblock
    def post(self):
        body = self.request.body
        recv = xml2dict(body)
        print recv 
        #send = SendMsg().text(recv.get('FromUserName'),recv.get('ToUserName'),int(time.time()),u'你好')
        msgType = recv.get('MsgType','') 
        if msgType == 'event':
            if recv.get('Event') in ['subscribe','unsubscribe']:
                send = SendMsg().text(recv.get('FromUserName'),recv.get('ToUserName'),int(time.time()),u'你好')
        elif msgType == 'text' :
            res_music = api_music(recv.get('Content',''))
            send = SendMsg().music(
                recv.get('FromUserName'),
                recv.get('ToUserName'),
                int(time.time()),
                recv.get('Content'),
                res_music['album']['name'],
                res_music['audio'],
                res_music['audio']
            )
        else:
            send=''
            
        self.write(send)
        self.finish()







