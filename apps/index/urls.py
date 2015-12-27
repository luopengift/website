#!/usr/bin/env python
#-*-coding:utf8-*-
import views

urlpath = [
    (r"(?:/api)?/", views.MainHandler),
    (r"(?:/api)?/new", views.MainHandlerNew),
]
