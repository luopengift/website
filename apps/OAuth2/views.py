#!/usr/bin/env python
#-*-coding:utf8-*-

from control.BaseHandler import BaseHandler
from control.unblock import unblock
import json
from .model import *
from .api import api


collect = 'test'
user_info = ['uname','password','role','group','mail','phone','qq']

def change(_data):
    ret = []
    for i in _data:
        data=dict()
        data['user_email'] = i.get('mail','')
        data['user_name'] = i.get('uname','')
        data['user_psw'] = i.get('password','')
        data['user_roles'] = i.get('role','')
        data['organization'] = i.get('group','')
        data['user_tel'] = i.get('phone','')
        data['user_qq'] = i.get('qq','')
        ret.append(data) 
    return ret
       

def cut_mail(mail):
    return mail.split('@')[0]

class User(BaseHandler):

    @unblock
    def get(self): #查询资源
        uname = self.get_query_arguments('uname','')
        if not uname:
            res = {'errtype':1,'info':u'错误的请求参数'}
        else:
            if uname=='all':
                res = getAll(collect,{'uname':uname})
                if not res:
                    res = {'errtype':2,'info':u'查询值不存在'}
                else:
                    pass  #去监控宝验证
        self.write(res)
        self.finish()



    @unblock
    def post(self): #新建资源
        recv=eval(self.request.body)
        t = self.check_access(recv)
        if not t[0]:
            res = t[1]
        else:
            news = map(lambda x:cut_mail(x.get('mail','')),recv)
            users = map(lambda x:cut_mail(x.get('mail','')),getAll(collect))
            exists = set(news) & set(users)
            if exists:
                res = {'status':'fail','info':u'用户%s已存在,新增失败'% ','.join(exists).strip(',')}
            else:
                all = map(lambda x:cut_mail(x.get('user_email','')),api.get_all_users())
                exists = set(news) & set(all)
                if exists:
                    res = {'status':'fail','info':u'用户%s已存在监控宝系统中'% ','.join(exists).strip(',')}
                else:
                    ret = api.create_user(change(recv))
                    res = ret
                    _id = insert(collect,recv)
                    
                    if not _id:
                        res.update({'status':'fail','info':u'用户新增失败'})
                    res.update({'status':'success','info':u'用户新增成功'})

        return self.finish(res)

    @unblock
    def put(self): #修改资源
        form_data = self.request.body
        recv = json.loads(self.get_body_argument('data',''))

        print form_data
        print type(form_data)
        print recv
        print type(recv)


        print self.request.headers

        #print change(recv)
        

        t = self.check_access([recv])
        if not t[0]:
            res = t[1]
        else:
            news = map(lambda x:cut_mail(x.get('mail','')),recv)
            users = map(lambda x:cut_mail(x.get('mail','')),getAll(collect))
            exists = set(news) - set(users)
            if exists:
                res = {'status':'fail','info':u'用户%s不存在,修改失败'% ','.join(exists).strip(',')}
            else:
                all = api.get_all_uses()
                all_users = map(lambda x:cut_mail(x.get('user_email','')),all)
                exists = set(news) - set(all_users)
                print exists
                if exists: 
                    res = {'status':'fail','info':u'用户%s不存在监控宝系统中,修改失败'%','.join(exists).strip(',')}
                else:
                    ret = []
                    for i in change(recv):
                        ret.append(api.modify_user(id,i))
                    print ret
                    for i in recv:
                        _id = update(collect,{'mail':i.get('mail','')},{'$set':i})
                    print _id
                    if not _id:
                        res = {'info':u'数据修改失败'}
                    res = {'info':u'数据修改成功'}
        self.write(res)
        self.finish()


    def delete(self): #删除资源
        uname = self.get_query_arguments('uname',[])
        if uname == []:
            res = {'info':u'用户名为空'}
        elif len(uname) != len(set(uname)):
            res = {'info':u'用户名重复'}
        else:
            users = map(lambda x:cut_mail(x.get('mail','')),getAll(collect))
            exists = set(uname) - set(users)
            if exists:
                res = {'status':'fail','info':u'用户%s不存在,删除失败'% ','.join(exists).strip(',')}
            else:
                all = api.get_all_users()
                all_users = map(lambda x:cut_mail(x.get('user_email','')),all)
                exists = set(uname) - set(all_users)
                if exists:
                    res = {'status':'fail','info':u'用户%s不存在监控宝系统中,删除失败'%','.join(exists).strip(',')}
                else:
                    ret = {}
                    for i in all:
                        if cut_mail(i.get('user_mail','')) in uname:
                            api_res = api.stop_user(i.get('user_id',''))
                    #        ret.update({str(cut_mail(i.get('user_mail','')):api_res})
                    res = {'info':ret}
                    for i in uname:
                        
                        delete(collect,{'uname':i}) 
                    res = {'info':'cunzai'}
        '''    
        if uname:
            for i in uname:
                t = self.check_user(i)
                if not t[0]:
                    res = t[1]
                    break
            else:
                r = delete(collect,{'uname':uname})
                print r
                res = {'info':u'删除用户成功.'}
        else:
            res = {'info':u'提交的用户错误!'}
        '''
        self.write(res)


    def check_exists(self,_data,keys):
        return list(set(_data) -set(keys))      #s.difference(t)
        


    def check_access(self,_data):
        if isinstance(_data,list):
            mail=[]
            for i in _data:
                res = self.check_exists(i.keys(),user_info)
                if res:
                    return (False,{'info':u'%s不合法'% ','.join(res).strip(',')})
                user_mail = i.get('mail','')
                if user_mail == '':
                    return (False,{'info':u'邮箱是必选参数'})
                else:
                    if user_mail in mail:
                        return (False,{'info':u'提交的数据中,邮箱%s重复'%user_mail})
                    else:
                        mail.append(i.get('mail',''))
            else:
                return (True,{})
        else:
            return (False,{'info':u'数据格式不合法'})

    
    def check_user(self,uname):
        users = map(lambda x:x.get('uname',''),getAll(collect))
        return self.check_exists(set(uname),set(users))


'''
url - http://10.33.20.49/oauth2/user

新建用户:
    method:POST
    数据格式:
        <单个用户>
            [{
                'uname':<require>,
                'password':<require>,
                'role':<require>,
                'group':<not require>,
                'mail':<require>,
                'phone':<require>,
                'qq':<require>
             }]
        <多个用户>
            [{<单个用户>},{<单个用户>,...]


删除用户:
    method:DELETE
    数据格式:
        <单个用户>
            ?uname=xxx
        <多个用户>
            ?uname=xxx&uname=xxx&uname=xxx.....


修改用户:
    method:PUT
    数据格式:
        (同新建用户)        

查询用户:
    method:GET
    数据格式:
        <单个用户>
            ?uname=xxx
        <多个用户>
            ?uname=xxx&uname=xxx&uname=xxx.....
        <所有用户>
            ?uname=all
        














            


'''





