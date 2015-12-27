#!/usr/bin/env python 
#-*-coding:utf8-*-
import sys
reload(sys);sys.setdefaultencoding('utf8')
import os
import yaml
import logging
import logging.config

cur_dir = os.path.dirname(os.path.abspath(__file__))
configure = yaml.load(open(os.path.join(cur_dir,'logger.yaml')))  # <'dict'>


def initlog(logger_name=__name__,logfile='/tmp/tornado.log'):
    logger =  logging.getLogger(logger_name)
    fileHandler = logging.handlers.RotatingFileHandler(logfile, maxBytes = 1024*1024*1024, backupCount = 5)
    streamHandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)
    return logger

try:
    logging.config.dictConfig(configure)
    logging = logging.getLogger(__name__)
except Exception,e:
    print str(e)
    logging = initlog()
finally:
    logging.debug(u'----系统启动中...设置编码环境:%s----',sys.getdefaultencoding().upper())    #exc_info=True

if __name__ == '__main__':
    logging.debug(__name__)

