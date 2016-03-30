#!/usr/bin/env python 
#-*-coding:utf8-*-
import sys
reload(sys);sys.setdefaultencoding('utf8')
import urllib,urllib2,ssl,json,time
from logger import logging

def httpResponse(url, method='POST',data=None,headers=None):
    response = None
    if headers == None:
        headers = {
            "Origin": "https://www.baidu.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) " +\
                "AppleWebKit/537.36 (KHTML, like Gecko) " +\
                "Chrome/34.0.1847.116 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.baidu.com/login?forward=http://localhost",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            "Cookie": "sessionid=ubwzabfvvyy0ft4y4nk5qlduv7nswrim",
        }
    try:
        request = urllib2.Request(url, data, headers=headers, origin_req_host=None, unverifiable=False)
        #request = urllib2.Request(url, data, origin_req_host=None, unverifiable=False)
        request.get_method = lambda:method
        try:
            response = urllib2.urlopen(request)                   #python <= 2.6
        except AttributeError, e:
            logging.debug(u'URLopen AttributeError: {msg}'.format(msg = e))
            response = urllib2.urlopen(request,  context=ssl._create_unverified_context()) #python 2.7
    except urllib2.HTTPError, e:
        logging.error(u'HTTP 服务器({url})无法完成请求.错误码:{code}'.format(url = url, code = e.code),exc_info=True)
    except urllib2.URLError, e:
        logging.error(u'HTTP 无法连接服务器({url}).原因:{reason}'.format(url = url, reason = e.reason),exc_info=True)
    except Exception, e:
        logging.error(u'HTTP 服务器({url})其他未知错误{error}'.format(url = url, error = e),exc_info=True)
    else:
        code = response.code
        result = response.read()
        #print 'url',response.geturl() #url
        #print 'info',response.info()  #头信息？
        logging.debug(u'HTTP 服务器({url})响应:{result}'.format(url = url, result = 'True'),exc_info=True)
        return code, result
    finally:
        if response:
            response.close()
        else:
            return False, 'error'


def multiHttpResponse(url, method='POST',data=None,count=5,sleep=5):
    '''
    HTTP GET/POST 数据,失败重试(默认重试5次,每次延时5秒)
    '''
    num=0
    while count:
        num+=1
        logging.info(u'{method}第{num}次数据.'.format(method=method,num=num))
        code ,result = httpResponse(url, method,data)
        if code == 200 or result != 'error':
            return code, result
        else:
            time.sleep(sleep)
            count-=1
    logging.error(u'尝试{num}次,仍然失败退出.'.format(num=num))
    return False, 'error'


if __name__ == '__main__':
    #data=urllib.urlencode({'username':'luopeng1','password':'b0!Xb-x)'})
    #httpResponse('https://ksso.kisops.com/login?forward=http://10.33.20.49:8000/login',data)
    #data = json.dumps({'_id':'55fa98c88a825641b202722e','title':'test','blog':u'你好','time':123456567,'author':'luopeng1'})
    #print httpResponse('http://10.33.20.49:8001')
    #url = 'http://myview.chinanetcenter.com/api/bandwidth-channel.action?u=db_kingsoft&p=myviewAPI_Kingsoft&startdate=2015-11-09&enddate=2015-11-09&channel=news.pop.www.duba.net&isExactMatch=true&region=cn;fg&isp=cn;other&resultType=2&format=json'
    #print httpResponse(url,'GET')
    httpurl = 'http://10.33.20.155/openapi'
    soapurl = 'http://10.33.20.155/r/s?service=CheetahApi&wsdl=true'
    data = {"sid":"1d107230-e9e2-449e-9046-4df431ae2c70","systemAlias":"测试服务器","systemDomain":"www.baidu.com"}
    headers = {'accessKey':'test','secret':'test'}
    res = httpResponse(httpurl,'POST',headers=headers,data = urllib.urlencode(data))
    print res[1]





















