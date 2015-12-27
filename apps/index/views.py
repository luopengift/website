#!/usr/bin/env python
#-*-coding:utf8-*-
from control.BaseHandler import BaseHandler
from control.unblock import unblock
import time

import tornado
from tornado.concurrent import run_on_executor
#python 3+ with the futures itself,however you should install it while using python2+
from concurrent.futures import ThreadPoolExecutor



class MainHandler(BaseHandler):
    @unblock
    def get(self):
        self.render2('mainpage.html')
        if not self._finished:
            self.finish()


    @unblock
    def post(self):
        try:
            print self.request.body
            result=self.request.body
            self.write(result)
        except Exception as e:
            logging.exception('Exception')
             
        finally:
            self.finish()


class MainHandlerNew(BaseHandler):
    executor = ThreadPoolExecutor(2)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        #调用下层API
        string = self.api_1().result()
        self.write(string)
        self.finish()

    @run_on_executor
    def api_1(self):
        #time.sleep(1)
        return "Hello Word"



