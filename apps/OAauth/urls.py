#!/usr/bin/env python
#-*-coding:utf8-*-
import views

urlpath = [
    (r"(?:/api)?/auth", views.AuthHandler),
]
