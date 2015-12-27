#!/usr/bin/env python 
#-*-coding:utf8-*-
import functools
import datetime
import bson
from .model import *

opslog = 'opslog'

def ops_log(func):
    @functools.wraps(func)    
    def log(self,*args,**kwargs):
        ret = func(self,*args,**kwargs)
        if self.request.method == "POST":
            try:
                writelog(
                    self = self,
                    id = self.id,
                    collect = self.collect,
                    user = self.current_user,
                    action = self.get_query_argument('_',''),
                    new = self.data,
                )
            except Exception,e:
                print str(e)
            return ret
        elif self.request.method == "GET":
            if self._ == "delete":
                try:
                    writelog(
                        self = self,
                        id = self.id,
                        collect = self.collect,
                        user = self.current_user,
                        action = self.get_query_argument('_',''),
                        new = {},
                    )
                except Exception,e:
                    print str(e)
                return ret
    return log


def writelog(self,id,collect,user,action,new):
    print id
    print list(getAll(collect))
    old = self.old
    asset_id = old.get('asset_id','')
    if action == 'new':
        act = u'新增'
        old_data = {}
    elif action == 'delete':
        act = u'删除'
        old_data = self.deletedata
        asset_id = old_data.get('asset_id','')
    else:
        act = u'修改'
        if action == 'baseinfo':
            for info in ['use_info','dev_info','idc_info','hard_info','system_info']:
                old_data = old.pop(info)
        else:
            old_data = old.get(action.split('info')[0]+'_info',{})
    print old_data
    logdata = {
        'current_user':user,
        'type':collect,
        'act':act,
        'asset_no':id,
        'asset_id':asset_id,
        'old_data':changedata(old_data),
        'new_data':changedata(new),
        'time':datetime.datetime.now(),
    }
    insert(opslog,logdata)
    return 

def changedata(data):
    d={}
    for i in data.keys():
        d[i.split('.')[-1]] = data[i]
    return d









