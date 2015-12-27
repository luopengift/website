#!/usr/bin/env python
#-*-coding:utf8-*-
import views

urlpath = [
    (r"(?:/api)?/assets", views.Assets),
    (r"(?:/api)?/assets/search", views.Assets),
    (r"(?:/api)?/assets/server", views.Server),
    (r"(?:/api)?/assets/switch", views.Switch),
    (r"(?:/api)?/assets/storage", views.Storage),
    (r"(?:/api)?/assets/ec2", views.Ec2),
    (r"(?:/api)?/assets/opslog", views.Opslog),
]
