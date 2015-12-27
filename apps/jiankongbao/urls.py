#!/usr/bin/env python
#-*-coding:utf8-*-
import views

urlpath = [
    (r"(?:/api)?/jiankongbao/resource/(.*)", views.Resource),
    (r"(?:/api)?/jiankongbao/user/(.*)", views.User),
    (r"(?:/api)?/jiankongbao/send", views.Send),
]
