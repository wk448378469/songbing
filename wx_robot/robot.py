# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 23:21:50 2017

@author: 凯风
"""

from itchat.core import Core
from itchat.content import *
import platform
import os

class wxRobot(object):
    '''weixin robot class

    参数说明:
    -----------
        
        hot_reload(bool):退出程序后暂存登陆状态，默认为True

        defaultMsg(str):用户发送不支持的图片时返回的文本信息

        MAINDIR(str):程序主目录

        handlers(dict):处理器的字典，默认为空，registerHandler可添加，仅支持text、map、picture、note四类默认

    方法说明:
    -----------

        judgmentSystem:判断主机系统

        registerHandler:注册添加处理器

        dispathc:调度函数，机器人接受信息后，判断使用什么已注册的处理器

        run:启动机器人

    '''
    def __init__(self, maindir, hot_reload = False , defaultMsg = u'暂未支持的图片格式'):
        self.hot_reload = hot_reload
        self.wx = Core()
        self.handlers = {'text':[], 'picture':[], 'note':[]}
        self.enableCmdQR = self.judgmentSystem()
        self.default_msg = defaultMsg
        self.MAINDIR = maindir + '/wx_robot'
    
    def judgmentSystem(self):
        imformation = platform.platform()
        if 'Windows' in imformation:
            return True
        else:
            return 2
    
    def registerHandler(self, handler, htype):
        if htype in self.handlers:
            self.handlers[htype].append(handler)
        else:
            self.handlers[htype] = []
            self.handlers[htype].append(handler)
    
    def dispatch(self):
        @self.wx.msg_register(TEXT)
        def _dispatchText(msg):
            for h in self.handlers['text']:
                if h.match(msg):
                    sendPic, returnData = h.handle(msg)
                    if sendPic:
                        self.wx.send('@img@%s' % returnData , msg['FromUserName'])
                    else:
                        self.wx.send(returnData, msg['FromUserName'])
                    del h
                    break

        @self.wx.msg_register(PICTURE)
        def _dispatchPic(msg):
            picpath = self.MAINDIR + '/userpic/' + msg['FileName']
            msg['Text'](picpath)
            if os.path.getsize(picpath)/1024 >= 200:
                self.wx.send(u'图片太大啦，请不要点击微信中的发送原图~'，msg['FromUserName'] )
            else:
                for h in self.handlers['picture']:
                    if h.match(msg):
                        sendPic,returnData = h.handle(msg,picpath)
                        if sendPic:
                            self.wx.send('@img@%s' % returnData , msg['FromUserName'])
                        else:
                            self.wx.send(returnData, msg['FromUserName'])
                    else:
                        self.wx.send(self.default_msg, msg['FromUserName'])
                    del h

        @self.wx.msg_register(NOTE)
        def _dispathNote(msg):
            for h in self.handlers['note']:
                if h.match(msg):
                    sendPic,returnData = h.handle(msg)
                    if sendPic:
                        self.wx.send('@img@%s' % returnData, msg['FromUserName'])
                    else:
                        self.wx.send(returnData, msg['FromUserName'])
                    del h

        @self.wx.msg_register(FRIENDS)
        def add_friend(msg):
            self.wx.add_friend(**msg['Text'])
            self.wx.send_msg(u'很高兴遇见你', msg['RecommendInfo']['UserName'])

    def run(self):
        self.dispatch()
        self.wx.auto_login(hotReload=self.hot_reload, enableCmdQR=self.enableCmdQR)
        self.wx.run()
