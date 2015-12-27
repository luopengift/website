#!/usr/bin/env python
#-*-coding:utf8-*-
import os
import yaml
import base64
import uuid
import tornado
from tornado.options import options

cur_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(cur_dir)
setting = yaml.load(open(os.path.join(cur_dir,'config.yaml')))

tornado.options.define('debug', default=setting['DebugModel'], help='enable debug mode')
tornado.options.define('port', default=setting['HttpServerPort'], help='run on the given port', type=int)


settings = dict(
    template_path = os.path.join(base_dir,'templates/').replace('\\','/'),
    static_path = os.path.join(base_dir,'static/'),
    cookie_secret = 'zkJhueaSQteGnmlA1+FHpEPnfnojJ09KjTQ60qcE7Pc=',
    #cookie_secret = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
    login_url = '/login',
    debug = options.debug,
    compiled_template_cache=False,#模板不会被缓存
)



