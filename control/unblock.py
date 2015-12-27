#!/usr/bin/env python
#-*-coding:utf8-*-
__author__=u'罗鹏'
import tornado,functools
#python 3+ with the futures itself,however you should install it while using python2+
from concurrent.futures import ThreadPoolExecutor




def unblock(func,replace_callback=True):
    @tornado.web.asynchronous
    @functools.wraps(func)
    def _wrapper(self,*args,**kwargs):
        def callback(future): return future.result()
        try:
            f = lambda future: tornado.ioloop.IOLoop.current().add_callback_from_signal(functools.partial(callback,future))
            future = ThreadPoolExecutor(max_workers=4).submit(functools.partial(func, self, *args, **kwargs))
            future.add_done_callback(f)
            return future.result()
        except Exception,e:
            print e
    return _wrapper



def unblock1(func,replace_callback=True):
    @tornado.web.asynchronous
    @functools.wraps(func)
    def _wrapper(*args,**kwargs):
        def callback(future): return future.result()
        f = lambda future: tornado.ioloop.IOLoop.current().add_callback(functools.partial(callback,future))
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.submit(functools.partial(func, *args, **kwargs)).add_done_callback(f)
    return _wrapper

def unblock2(func,replace_callback=True):
    @tornado.web.asynchronous
    @functools.wraps(func)
    def _wrapper(self,*args,**kwargs):
    #    def callback(future): return future.result()
        future = ThreadPoolExecutor(max_workers=4).submit(functools.partial(func, self, *args, **kwargs))
        tornado.ioloop.IOLoop.current().add_future(future ,lambda future: callback(future.result))
    return _wrapper



























