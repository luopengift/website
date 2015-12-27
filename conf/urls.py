#!/usr/bin/env python 
#-*-coding:utf8-*-

def patterns(*args):
    return reduce(lambda x,y:x+y,args,[])
