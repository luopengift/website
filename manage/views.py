#!/usr/bin/env python
#-*-coding:utf8-*-
from control.BaseHandler import BaseHandler
from control.unblock import unblock



user={
    'luopeng':'995596',



}
    

def auth(username):
    return '0000'



class Login(BaseHandler):
    def get(self):
        pass

    def post(self):
        username = self.get_body_argument('username',False)
        password = self.get_body_argument('password',False)
        secret = self.get_body_argument('secret',False)
        if username and password and secret:
            if password == user.get(username,''):
                if secret == auth(username):
                    self.set_secure_cookie('username',username)#,expires_days=0)
                    self.redirect('/')
                else:
                    self.write('动态验证失败')
            else:
                self.write('密码错误')    
        else:
            self.write('不能为空')
        pass

class Logout(BaseHandler):
    def get(self):
        self.clear_cookie('username')
        self.redirect('/')
        #if not self._finished:self.finish()





