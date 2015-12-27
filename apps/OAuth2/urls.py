#!/usr/bin/env python
#-*-coding:utf8-*-
import views

urlpath = [
    (r"(?:/api)?/oauth2/user", views.User),
]
