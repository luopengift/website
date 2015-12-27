#!/usr/bin/env python 
#-*-coding:utf8-*-

from pymongo import MongoClient
from conf.setting import setting

mongocur = MongoClient(setting['mongoIP'],setting['mongoPort'])
db=setting['mongoDB']
def insert(collect=None,data=None):
    return mongocur[db][collect].insert(data)

def update(collect=None,items=None,data=None):
    return mongocur[db][collect].update(items,data)

def getOne(collect=None,items=None,keys=None):   #查询一个，返回list
    ret = mongocur[db][collect].find_one(items,keys)
    return ret if ret else {}

def getAll(collect=None,items=None,*args,**kwargs):   #返回对象
    return mongocur[db][collect].find(items)

def delete(collect=None,items=None,*args,**kwargs):
    return mongocur[db][collect].remove(items)




















