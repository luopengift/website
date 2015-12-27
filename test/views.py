#!/usr/bin/env python
#-*-coding:utf8-*-
from control.BaseHandler import BaseHandler
from control.unblock import unblock
import time,datetime
from pymongo import MongoClient
conn = MongoClient('10.33.20.49',27017)
class Test1(BaseHandler):
    @unblock
    def get(self):
        print conn.test.test.insert({'time':datetime.datetime.now()})
        time.sleep(120)
        self.write('This is a test1.')
        self.finish()
class Test2(BaseHandler):
    @unblock
    def get(self):
        self.write('This is a test2.')
        self.finish()
