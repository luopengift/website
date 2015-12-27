#!/usr/bin/env python 
#-*-coding:utf8-*-

from tornado.web import HTTPError
from models import mongodb

   
'''
权限说明【查看r，修改w，无权限o】
权限分配:   |基本信息   |使用信息   |设备信息   |IDC信息    |硬件信息   |系统信息   |root/远控信息
受限用户:   |o          |o          |o          |o          |o          |o          |o
业务用户：  |r          |rw         |r          |r          |r          |o          |o
ops用户：   |r          |r          |r          |r          |r          |r          |r
idc用户:    |r          |r          |r          |rw         |r          |rw         |rw
资产管理:   |rw         |r          |rw         |r          |rw         |r          |r


'''
def access(func):
    def _wrapper(self, *args, **kwargs):
        admin =  getOne('accounts',{"role":"admin","user":curr_user})
        if self.current_user:
            ret = func(self, *args, **kwargs)
            if admin:
                return ret
            else:
                raise HTTPError(403)
        else:
            raise HTTPError(403)
    return _wrapper








