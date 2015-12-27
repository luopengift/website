#!/usr/bin/env python
#-*-coding:utf8-*-
from conf.urls import patterns
import test.urls
import manage.urls
import apps.index.urls
import apps.weixin.urls


handlers = patterns(
    test.urls.urlpath,              #测试
    manage.urls.urlpath,              #系统管理相关
    apps.index.urls.urlpath,        #主页测试
    apps.weixin.urls.urlpath,


)



