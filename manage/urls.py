#!/usr/bin/env python
#-*-coding:utf8-*-
#import kssoAuth
import views
urlpath = [
    #(r"/login", kssoAuth.Login),
    (r"/auth/login", views.Login),
    (r"/auth/logout", views.Logout),
]
