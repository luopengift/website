#!/usr/bin/env python 
#-*-coding:utf8-*-
#监控宝API,用于token获取,用户管理,组管理
__author__ = 'luopeng1'
__time__ = '20151126'

import sys
import json
import time
import requests
import hashlib   

def MD5(string):
    m2 = hashlib.md5()   
    m2.update(string)   
    return m2.hexdigest()

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class JKB_API(object):
    
    url = 'https://api.jiankongbao.com/v2'
    username = 'luopeng1@cmcm.com'
    password = 'luopeng1123456'
    client_id = '113720'
    client_secret = 'abb16cd6a6f4615c942f2ac870bb271da086f1ac'

    access_token = ''
    refresh_token = ''
    expires_in = 0

    def __init__(self):
        self.token()
 
    def __get_token(self):
        data = {
            'grant_type':'password',
            'username':self.username,
            'password':MD5(self.password),
            'client_id':self.client_id,
            'client_secret':self.client_secret,
        }
        response = requests.post(self.url+'/oauth/token.json',data=data)
        res = json.loads(response.text)
        self.access_token = res.get('access_token','')
        self.refresh_token = res.get('refresh_token','')
        self.expires_in = int(time.time()) + res.get('expires_in','')
        return self.access_token


    def __get_refresh_token(self):
        data = {
            'grant_type':'refresh_token',
            'client_id':self.client_id,
            'client_secret':self.client_secret,
            'refresh_token':self.refresh_token,
        }
        response = requests.post(self.url+'/oauth/token.json',data=data)
        print response.text
        return json.loads(response.text)

    def token(self):
        if int(time.time()) < self.expires_in:
            return self.access_token
        else:
            return self.__get_token()

    def get_user(self,user_id=None):
        if user_id:
            uri = '/user/info/{user_id}.json'.format(user_id = user_id)
        else:
            uri = '/user/info.json'
    
        params = {'access_token':self.token()}
        response = requests.get(self.url+uri,params=params)
        return json.loads(response.text)

    def get_all_users(self):
        params = {'access_token':self.token()}
        response = requests.get(self.url+'/user/lists.json',params=params)
        return json.loads(response.text)
    
    #TODOS:还没有测试通过#
    def create_user(self,data):
        params = {'access_token':self.token()}
        response = requests.get(self.url+'/user/create.json',params=params,data=json.dumps(data))
        return json.loads(response.text)

    def modify_user(self,user_id,data=None):
        params = {'access_token':self.token()}
        data = '''----WebKitFormBoundary96q7eecsvNHmY9t8
Content-Disposition: form-data; name="data"

{"user_qq":200005678}
----WebKitFormBoundary96q7eecsvNHmY9t8'''
        data = {"user_qq":200005678}
        print data
        
        headers = {
            'content-type':'multipart/form-data'
        } 



        response = requests.post(self.url+'/user/modify/%s.json?access_token=%s'%(user_id,self.token()),data=data,headers = headers)
        print response.url
        return response.text

    def stop_user(self,user_id):
        params = {'access_token':self.token()}
        response = requests.put(self.url+'/user/stop/%s'%user_id,params=params)
        print response.url
        return json.loads(response.text)

    def start_user(self,user_id):
        params = {'access_token':self.token()}
        response = requests.put(self.url+'/user/start/%s'%user_id,params=params)
        return json.loads(response.text)

    def get_group(self):
        params = {'access_token':self.token()}
        response = requests.get(self.url+'/user/organization.json',params=params)
        return json.loads(response.text)

api = JKB_API()

if __name__ == '__main__':
    chenjiliang = '328786'
    luopeng = '328780'
    for i in api.get_all_users():
        if i.get('user_email',)=='chenjiliang@cmcm.com':
            print i
    
    print api.get_group()







