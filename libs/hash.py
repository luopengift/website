#!/use/bin/env python 
#-*-coding:utf8-*-

import hmac
import hashlib

def HmacMD5(key,string):
    s = hmac.new(key)
    s.update(string)
    return s.hexdigest().upper()


def MD5(string):
    s = hashlib.md5()   
    s.update(string)   
    return s.hexdigest()










