#!/usr/bin/env python
#-*-coding:utf8-*-

import time
import functools


def executeTime(func):
    '''
    装饰器,测试函数执行时间
    '''
    @functools.wraps(func)
    def _warp(*args,**kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print func.__name__,'执行时间:',end-start
        return res
    return _warp

