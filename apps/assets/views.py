#!/usr/bin/env python
#-*-coding:utf8-*-

import os
import tornado
from control.BaseHandler import BaseHandler
from control.unblock import unblock
import bson
import json
from .model import *
from .opslog import ops_log
from .auth import authenticated

top_tags = ['asset_id','sn','asset_type','state','dev_info','idc_info','hard_info','system_info','use_info']
dev_tags = ['brand','model','unit','price','buy_time','expired_time',]
idc_tags = ['idc','cabinet_pos','tray_pos','jifang_uname','jifang_phone']
hard_tags = ['cpu_model','cpu_num','cpu_core','mem_num','mem_total','mem_desc','disk_num','disk_total','disk_desc','ssd_total','raid_model','raid_cache','raid_num','raid_desc','net_num','net_speed','net_desc','mount','mount_rom','power']

class Assets(BaseHandler):
    def get(self):
        self.render2('/assets/index.html')    

    def post(self):
        queryfrom = self.get_body_arguments('queryfrom',[])
        item = self.get_body_argument('item','')
        data = self.get_body_argument('data','')
        self.render2('/assets/error.html',err_msg =item)

class Server(BaseHandler):
    collect = 'server'

    @unblock
    @ops_log
    @authenticated
    def get(self): #查询资源
        self.id = self.get_query_argument('id','')
        self._ = self.get_query_argument('_','')
        if self._ == 'delete':
            self.deletedata = getOne(self.collect,{'_id':bson.ObjectId(self.id)})
            delete(self.collect,{'_id':bson.ObjectId(self.id)})
            self.redirect('/assets/server')
        elif self._  and id:
            self.res = getOne(self.collect,{'_id':bson.ObjectId(self.id)})
            if self.res:
                self.render2('/assets/server/%s.html'%self._,res = self.res)
            else:
                self.render2('/assets/error.html',err_msg = '资产查询失败')
        else:
            self.res = getAll(self.collect)
            self.render2('/assets/server/total.html',res=list(self.res))
        if not self._finished:self.finish()


    @unblock
    @ops_log
    @authenticated
    def post(self): #新建资源
        self.id = self.get_query_argument('id','')
        self._ = self.get_query_argument('_','')
        self.old = getOne(self.collect,{'_id':bson.ObjectId(self.id)})
        self.data = self.recv()
        if self._ == 'new':
            self.id = insert(self.collect,self.data)
            self.redirect('/assets/server?_=%s&id=%s'%('baseinfo',str(self.id)))
        elif self._ and self.id:
            try:
                update(self.collect,{'_id':bson.ObjectId(self.id)},{'$set':self.data})
            except Exception,e:
                self.render2('/assets/error.html',err_msg =str(e))
            else:
                self.redirect('/assets/server?_=%s&id=%s'%(self._,self.id))
        else:
            self.render2('/assets/error.html',err_msg = '资产查询失败')
        if not self._finished:self.finish()
    
    def recv(self):
        _type=self.get_argument('_type','')
        if _type == 'baseinfo':
            return self.baseinfo()
        elif _type == 'useinfo':
            return self.useinfo()
        elif _type == 'devinfo':
            return self.devinfo()
        elif _type == 'idcinfo':
            return self.idcinfo()
        elif _type == 'hardinfo':
            return self.hardinfo()
        elif _type == 'systeminfo':
            return self.systeminfo()
        elif _type == 'otherinfo':
            return self.otherinfo()
        elif _type == 'new':
            return self.new()
        else:
            return {}
    
    def baseinfo(self):
        return {
            'asset_id':self.get_body_argument('asset_id',''),
            'host_id':self.get_body_argument('host_id',''),
            'sn':self.get_body_argument('sn',''),
            'asset_type':self.get_body_argument('asset_type',''),
            'state':self.get_body_argument('state',''),
        }
    
    def useinfo(self):
        return {
            'use_info.owner':self.get_body_argument('owner',''),
            'use_info.users':self.get_body_argument('users','').encode('utf8').replace(',',';').split(';'),
            'use_info.use':self.get_body_argument('use',''),
            'use_info.stime':self.get_body_argument('stime',''),
            'use_info.etime':self.get_body_argument('etime',''),
        }

    def devinfo(self):
        return {
            'dev_info.brand':self.get_body_argument('brand',''),
            'dev_info.model':self.get_body_argument('model',''),
            'dev_info.unit':self.get_body_argument('unit',''),
            'dev_info.price':self.get_body_argument('price',''),
            'dev_info.buy_time':self.get_body_argument('buy_time',''),
            'dev_info.expired_time':self.get_body_argument('expired_time',''),
        }


    def idcinfo(self):
        return {
            'idc_info.idc':self.get_body_argument('idc',''),
            'idc_info.cabinet_pos':self.get_body_argument('cabinet_pos',''),
            'idc_info.tray_pos':self.get_body_argument('tray_pos',''),
            'idc_info.jifang_uname':self.get_body_argument('jifang_uname',''),
            'idc_info.jifang_phone':self.get_body_argument('jifang_phone',''),
        }
    
    def hardinfo(self):
        pass

    def systeminfo(self):
        dict = {
            'system_info.type':self.get_body_argument('type',''),
            'system_info.version':self.get_body_argument('version',''),
            'system_info.root_user':self.get_body_argument('root_user',''),
            'system_info.root_passwd':self.get_body_argument('root_passwd',''),
            'system_info.remote_ip':self.get_body_argument('remote_ip',''),
            'system_info.remote_user':self.get_body_argument('remote_user',''),
            'system_info.remote_passwd':self.get_body_argument('remote_passwd',''),
        }
        dict.update(self.ipinfo())
        return dict
        
    def ipinfo(self):
        ip = map(lambda x:[x],self.get_body_arguments('eth',''))
        bond = self.get_body_arguments('bond','')
        return {
            'system_info.IP_desc.ip':str(ip),
            'system_info.IP_desc.bond':str(bond).replace(';',',')
        }



 
    def otherinfo(self):
        return {
            'others':self.get_body_argument('others',''),
        }

    def new(self):
        dict = self.baseinfo()
        dict['others'] = ''
        for i in ['use_info','dev_info','idc_info','hard_info','system_info']:
            dict[i]={}
        dict['system_info']['IP_desc']={'ip':'[[],[],[],[],[],[],[],[]]','bond':'[]'}
        return dict






class Switch(BaseHandler):
    collect = 'switch'

    @unblock
    @authenticated
    def get(self): #查询资源
        self.id = self.get_query_argument('id','')
        self._ = self.get_query_argument('_','')
        if self._ == 'delete':
            self.deletedata = getOne(self.collect,{'_id':bson.ObjectId(self.id)})
            delete(self.collect,{'_id':bson.ObjectId(self.id)})
            self.redirect('/assets/switch')
        if self._ and self.id:
            self.res = getOne(self.collect,{'_id':bson.ObjectId(self.id)})
            if self.res:
                self.render2('/assets/switch/%s.html'%self._,res =self.res)
            else:
                self.render2('/assets/error.html',err_msg = '资产查询失败')
        else:
            self.res = getAll(self.collect)
            self.render2('/assets/switch/total.html',res=list(self.res))
        if not self._finished: self.finish()



    @ops_log 
    @authenticated
    def post(self):
        self.id = self.get_query_argument('id','')
        self._ = self.get_query_argument('_','')
        self.old = getOne(self.collect,{'_id':bson.ObjectId(self.id)})
        self.data = self.recv()
        if self._=='new':
            self.id = insert(self.collect,self.data)
            self.redirect('/assets/switch?_=%s&id=%s'%('baseinfo',str(self.id)))
        elif self._ and id:
            try:
                update(self.collect,{'_id':bson.ObjectId(self.id)},{'$set':self.data})
            except Exception,e:
                self.render2('/assets/error.html',err_msg =str(e))
            else:
                self.redirect('/assets/switch?_=%s&id=%s'%(self._,self.id))
        else:
            self.render2('/assets/error.html',err_msg = '资产查询失败')
        if not self._finished:self.finish()


    def recv(self):
        _type=self.get_argument('_type','')
        if _type == 'baseinfo':
            return self.baseinfo()
        elif _type == 'useinfo':
            return self.useinfo()
        elif _type == 'devinfo':
            return self.devinfo()
        elif _type == 'idcinfo':
            return self.idcinfo()
        elif _type == 'hardinfo':
            return self.hardinfo()
        elif _type == 'systeminfo':
            return self.systeminfo()
        elif _type == 'otherinfo':
            return self.otherinfo()
        elif _type == 'new':
            return self.new() 
        else:
            return {}


    def baseinfo(self):
        return {
            'asset_id':self.get_body_argument('asset_id',''),
            'sn':self.get_body_argument('sn',''),
            'asset_type':self.get_body_argument('asset_type',''),
            'state':self.get_body_argument('state',''),
            'monitor':self.get_body_argument('monitor',''),
        }

    def useinfo(self):
        return {
            'use_info.department':self.get_body_argument('department',''),
            'use_info.owner':self.get_body_argument('owner',''),
            'use_info.users':self.get_body_argument('users','').encode('utf8').replace(',',';').split(';'),
            'use_info.use':self.get_body_argument('use',''),
            'use_info.project_name':self.get_body_argument('project_name',''),
            'use_info.project_desc':self.get_body_argument('project_desc',''),
            'use_info.stime':self.get_body_argument('stime',''),
            'use_info.etime':self.get_body_argument('etime',''),
        }


    def devinfo(self):
        return {
            'dev_info.brand':self.get_body_argument('brand',''),
            'dev_info.model':self.get_body_argument('model',''),
            'dev_info.price':self.get_body_argument('price',''),
            'dev_info.buy_time':self.get_body_argument('buy_time',''),
            'dev_info.expired_time':self.get_body_argument('expired_time',''),
            'dev_info.contract':self.get_body_argument('contract',''),
        }


    def idcinfo(self):
        return {
            'idc_info.country':self.get_body_argument('country',''),
            'idc_info.city':self.get_body_argument('city',''),
            'idc_info.ascription':self.get_body_argument('ascription',''),
            'idc_info.idc':self.get_body_argument('idc',''),
            'idc_info.cabinet_pos':self.get_body_argument('cabinet_pos',''),
            'idc_info.tray_pos':self.get_body_argument('tray_pos',''),
            'idc_info.jifang_uname':self.get_body_argument('jifang_uname',''),
            'idc_info.jifang_phone':self.get_body_argument('jifang_phone',''),
        }


    def systeminfo(self):
        return {
            'system_info.type':self.get_body_argument('type',''),
            'system_info.version':self.get_body_argument('version',''),
            'system_info.environment':self.get_body_argument('environment',''),
            'system_info.remote_ip':self.get_body_argument('remote_ip',''),
            'system_info.remote_port':self.get_body_argument('remote_port',''),
        }


    def otherinfo(self):
        return {
            'others':self.get_body_argument('others',''),
        }


    def new(self):
        dict = self.baseinfo()
        dict['others'] = ''
        for i in ['use_info','dev_info','idc_info','hard_info','system_info']:
            dict[i]={}
        return dict



class Storage(BaseHandler):
    collect = 'storage'

    @unblock
    @authenticated
    def get(self): #查询资源
        self.id = self.get_query_argument('id','')
        self._ = self.get_query_argument('_','')
        if self._ == 'delete':
            self.deletedata = getOne(self.collect,{'_id':bson.ObjectId(self.id)})
            delete(self.collect,{'_id':bson.ObjectId(self.id)})
            self.redirect('/assets/storage')
        if self._ and self.id:
            self.res = getOne(self.collect,{'_id':bson.ObjectId(self.id)})
            if self.res:
                self.render2('/assets/storage/%s.html'%self._,res = self.res)
            else:
                self.render2('/assets/error.html',err_msg = '资产查询失败')
        else:
            self.res = getAll(self.collect)
            self.render2('/assets/storage/total.html',res=list(self.res))
        if not self._finished: self.finish()


    @ops_log
    @authenticated
    def post(self):
        self.id = self.get_query_argument('id','')
        self._ = self.get_query_argument('_','')
        self.old = getOne(self.collect,{'_id':bson.ObjectId(self.id)})
        self.data = self.recv()
        if self._=='new':
            self.id = insert(self.collect,self.data)
            self.redirect('/assets/storage?_=%s&id=%s'%('baseinfo',str(self.id)))
        elif self._ and id:
            try:
                update(self.collect,{'_id':bson.ObjectId(self.id)},{'$set':self.data})
            except Exception,e:
                self.render2('/assets/error.html',err_msg =str(e))
            else:
                self.redirect('/assets/storage?_=%s&id=%s'%(self._,self.id))
        else:
            self.render2('/assets/error.html',err_msg = '资产查询失败')
        if not self._finished:self.finish()



    def recv(self):
        _type=self.get_argument('_type','')
        if _type == 'baseinfo':
            return self.baseinfo()
        elif _type == 'useinfo':
            return self.useinfo()
        elif _type == 'devinfo':
            return self.devinfo()
        elif _type == 'idcinfo':
            return self.idcinfo()
        elif _type == 'hardinfo':
            return self.hardinfo()
        elif _type == 'systeminfo':
            return self.systeminfo()
        elif _type == 'otherinfo':
            return self.otherinfo()
        elif _type == 'new':
            return self.new()
        else:
            return {}


    def baseinfo(self):
        return {
            'asset_id':self.get_body_argument('asset_id',''),
            'sn':self.get_body_argument('sn',''),
            'asset_type':self.get_body_argument('asset_type',''),
            'state':self.get_body_argument('state',''),
            'monitor':self.get_body_argument('monitor',''),
        }

    def useinfo(self):
        return {
            'use_info.department':self.get_body_argument('department',''),
            'use_info.owner':self.get_body_argument('owner',''),
            'use_info.users':self.get_body_argument('users','').encode('utf8').replace(',',';').split(';'),
            'use_info.use':self.get_body_argument('use',''),
            'use_info.project_name':self.get_body_argument('project_name',''),
            'use_info.project_desc':self.get_body_argument('project_desc',''),
            'use_info.stime':self.get_body_argument('stime',''),
            'use_info.etime':self.get_body_argument('etime',''),
        }



    def devinfo(self):
        return {
            'dev_info.brand':self.get_body_argument('brand',''),
            'dev_info.model':self.get_body_argument('model',''),
            'dev_info.price':self.get_body_argument('price',''),
            'dev_info.buy_time':self.get_body_argument('buy_time',''),
            'dev_info.expired_time':self.get_body_argument('expired_time',''),
            'dev_info.contract':self.get_body_argument('contract',''),
        }


    def idcinfo(self):
        return {
            'idc_info.country':self.get_body_argument('country',''),
            'idc_info.city':self.get_body_argument('city',''),
            'idc_info.ascription':self.get_body_argument('ascription',''),
            'idc_info.idc':self.get_body_argument('idc',''),
            'idc_info.cabinet_pos':self.get_body_argument('cabinet_pos',''),
            'idc_info.tray_pos':self.get_body_argument('tray_pos',''),
            'idc_info.jifang_uname':self.get_body_argument('jifang_uname',''),
            'idc_info.jifang_phone':self.get_body_argument('jifang_phone',''),
        }



    def systeminfo(self):
        return {
            'system_info.type':self.get_body_argument('type',''),
            'system_info.version':self.get_body_argument('version',''),
            'system_info.environment':self.get_body_argument('environment',''),
            'system_info.remote_ip':self.get_body_argument('remote_ip',''),
            'system_info.remote_port':self.get_body_argument('remote_port',''),
        }


    def otherinfo(self):
        return {
            'others':self.get_body_argument('others',''),
        }



    def new(self):
        dict = self.baseinfo()
        dict['others']=''
        for i in ['use_info','dev_info','idc_info','hard_info','system_info']:
            dict[i]={}
        
        return dict


class Ec2(BaseHandler):
    collect = 'ec2'
    
    @unblock
    @authenticated
    def get(self):
        id = self.get_query_argument('id','')
        if id:
            res = getOne(self.collect,{'_id':bson.ObjectId(id)})
            print 'res',res
            if res:
                self.render2('/assets/ec2/ec2.html',res = res)
            else:
                self.render2('/assets/error.html',err_msg = '资产查询失败')
        else:
            res = getAll(self.collect)
            self.render2('/assets/ec2/total.html',res=list(res))
        self.finish()



    @authenticated
    def post(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        print cur_dir
        with open('/tmp/test.txt','r') as r:
            cur = r.read()

        aa = eval(cur)
        print insert('server',aa)
        self.write(cur)

class Opslog(BaseHandler):
    collect = 'opslog'
    def get(self):
        res = getAll(self.collect).sort('time',-1)
        self.render2('/assets/opslog/total.html',res=list(res))

    def post(self):
        pass



