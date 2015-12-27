#!/usr/bin/env python
#-*-coding:utf8-*-
from .token import Token

class RecvMsg():
    

    def text(self):
        pass





class SendMsg():


    def text(self,toUser,fromUser,CreateTime,Content):
        msg = '''<xml>
            <ToUserName><![CDATA[{toUser}]]></ToUserName>
            <FromUserName><![CDATA[{fromUser}]]></FromUserName>
            <CreateTime>{CreateTime}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{Content}]]></Content>
            </xml>'''.format(
                toUser=toUser,
                fromUser=fromUser,
                CreateTime=CreateTime,
                Content=Content
            )
        return msg


    def music(self,toUser,fromUser,CreateTime,TITLE,DESCRIPTION,MUSIC_Url,HQ_MUSIC_Url):
        msg = '''
            <xml>
                <ToUserName><![CDATA[{toUser}]]></ToUserName>
                <FromUserName><![CDATA[{fromUser}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[music]]></MsgType>
                <Music>
                    <Title><![CDATA[{TITLE}]]></Title>
                    <Description><![CDATA[{DESCRIPTION}]]></Description>
                    <MusicUrl><![CDATA[{MUSIC_Url}]]></MusicUrl>
                    <HQMusicUrl><![CDATA[{HQ_MUSIC_Url}]]></HQMusicUrl>
                </Music>
            </xml>'''.format(
                toUser=toUser,
                fromUser=fromUser,
                CreateTime=CreateTime,
                TITLE=TITLE,
                DESCRIPTION=DESCRIPTION,
                MUSIC_Url=MUSIC_Url,
                HQ_MUSIC_Url=HQ_MUSIC_Url,
            )
        return msg



class AutoReply(Token):
    def getAutoReply(self):
        '''
        获取公众号当前使用的自动回复规则，包括关注后自动回复、消息自动回复（60分钟内触发一次）、关键词自动回复。
        '''
        url = 'https://api.weixin.qq.com/cgi-bin/get_current_autoreply_info?access_token={ACCESS_TOKEN}'
        response = requests.get(url.format(ACCESS_TOKEN=self.access_token),verify=False)
        return response.json()





