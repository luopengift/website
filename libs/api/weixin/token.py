#!/usr/bin/env python
#-*-coding:utf8-*-
import requests
import json
import time
'''
URL(服务器地址) http://www.luopeng.space/
Token(令牌) 1234567890
EncodingAESKey(消息加解密密钥) RPac5l5uIR3cVNV8QYli54TEdz62t3PdMGoH89aQNMk
消息加解密方式 兼容模式

开发者ID
AppID(应用ID)wxd07b4fd2abe53cde
AppSecret(应用密钥)4d7aa6b04c59e67d98a9440c4c5bdd38


'''

class ErrorMsg(Exception):
    ''' exception for error code returned by api
    '''
    def __init__(self, errmsg):
        self.errmsg = errmsg

    def __str__(self):
        return str(self.errmsg)


class Token():
    '''
    access_token是公众号的全局唯一票据，公众号调用各接口时都需使用access_token。
    开发者需要进行妥善保存。access_token的存储至少要保留512个字符空间。
    access_token的有效期目前为2个小时，需定时刷新，重复获取将导致上次获取的access_token失效。
    '''

    AppID = 'wxc79ea9dbccb1b47f'#'wxd07b4fd2abe53cde'
    AppSecret = '7cbf783061856324b1a9d3d8d2ecd29d'#'4d7aa6b04c59e67d98a9440c4c5bdd38'
    access_token = ''
    expires_in = 0

    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Token, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance  

    def __init__(self):
        self.getToken()

    def accessToken(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
        response = requests.get(url.format(APPID=self.AppID,APPSECRET=self.AppSecret),verify=False).json()
        if response.has_key('access_token'):
            self.access_token = response.get('access_token','')
            self.expires_in = response.get('expires_in','')+int(time.time())
            return self.access_token
        else:
            raise ErrorMsg(response)
        return self.access_token
    
    def getToken(self):
        if self.expires_in == 0 or self.expires_in < int(time.time()):
            return self.accessToken()
        return self.access_token

class CallbackIP(Token):
    '''
    如果公众号基于安全等考虑，需要获知微信服务器的IP地址列表，
    以便进行相关限制，可以通过该接口获得微信服务器IP地址列表。
    ''' 
    def getCallbackIp(self):
        url = 'https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token={ACCESS_TOKEN}'
        response = requests.get(url.format(ACCESS_TOKEN=self.access_token),verify=False).text
        return json.loads(response).get('ip_list',[])
        



if __name__ == '__main__':
    token=Token()
    print token.getToken()
