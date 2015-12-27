#!/usr/bin/env python
#-*-coding:utf8-*-

import requests
from token import Token


class Menu(Token):
    '''
    自定义菜单能够帮助公众号丰富界面，让用户更好更快地理解公众号的功能。
    '''
    def create(self):
        '''
        创建菜单
        '''
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={ACCESS_TOKEN}'  
        body = '''
            {
     "button":[
     {  
          "type":"click",
          "name":"今日歌曲",
          "key":"V1001_TODAY_MUSIC"
      },
      {
           "name":"菜单",
           "sub_button":[
           {    
               "type":"view",
               "name":"搜索",
               "url":"http://www.soso.com/"
            },
            {
               "type":"view",
               "name":"视频",
               "url":"http://v.qq.com/"
            },
            {
               "type":"click",
               "name":"赞一下我们",
               "key":"V1001_GOOD"
            }]
       }]
    }



        '''
        resopnse = requests.post(url.format(ACCESS_TOKEN=self.access_token),data=body,verify=False)
        return resopnse.json()

    def get(self):
        '''
        使用接口创建自定义菜单后，开发者还可使用接口查询自定义菜单的结构。
        另外请注意，在设置了个性化菜单后，使用本自定义菜单查询接口可以获取默认菜单和全部个性化菜单信息。
        '''
        url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token={ACCESS_TOKEN}'
        response = requests.get(url.format(ACCESS_TOKEN=self.access_token),verify=False)
        return response.json()


    def delete(self):
        '''
        使用接口创建自定义菜单后，开发者还可使用接口删除当前使用的自定义菜单。
        另请注意，在个性化菜单时，调用此接口会删除默认菜单及全部个性化菜单。
        '''
        url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={ACCESS_TOKEN}'
        response = requests.get(url.format(ACCESS_TOKEN=self.access_token),verify=False)
        return response.json()



if __name__ == '__main__':
    menu=Menu()
    print menu.get()




