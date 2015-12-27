#!/usr/bin/env python
#-*-coding:utf8-*-
import sys
reload(sys);sys.setdefaultencoding("utf-8")
import tornado.httpserver
import tornado.ioloop
import tornado.web

from conf.setting import settings,options
from control.handlers import handlers
from libs.logger import logging

class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, handlers,**settings)

def main():#多进程模式
    tornado.options.parse_command_line()
    sockets = tornado.netutil.bind_sockets(options.port)
    tornado.process.fork_processes(0)   # forks one process per cpu
    server = tornado.httpserver.HTTPServer(Application(),xheaders=True)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()

def maintest():#单进程模式
    tornado.options.parse_command_line() #解析命令行, 有了这行，还可以看到日志...
    server = tornado.httpserver.HTTPServer(Application(),xheaders=True)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
        #main()
        maintest()









