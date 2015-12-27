#!/usr/bin/env python
#-*-coding:utf8-*-
from control.BaseHandler import BaseHandler
from control.unblock import unblock
import time,datetime
from libs.ksso import KSSO_API

ksso = KSSO_API('http://10.33.20.49/login')

class Login(BaseHandler):
    @unblock
    def get(self):
        if self.current_user:
             self.redirect('/assets')
        else:
            t=self.get_argument('t','')
            if t:
                username = ksso.ksso_login(t)
                if username:
                    self.set_secure_cookie("username", username)#,expires_days=0)
                    self.redirect('/assets')
                else:
                    self.render2('assets/error.html', err_msg='Ksso Retrun False')
            else:
                self.redirect(ksso.login_url) 
        if not self._finished:self.finish()


    def post(self):
        username = self.get_body_argument('username','')
        password = self.get_body_argument('password','')
        self.render2('assets/error.html',err_msg='登录失败,请重试！')

class Logout(BaseHandler):
    
    def get(self):
        '''
        user login out
        '''
        self.clear_cookie("username")
        ret = ksso.logout_url()
        self.redirect(ret)
        if not self._finished:self.finish()



