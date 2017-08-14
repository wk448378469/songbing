# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 23:21:50 2017

@author: 凯风
"""

from itchat.core import Core
from itchat.content import *
import platform

class wxRobot(object):
    def __init__(self, hot_reload = False , defaultMsg = u'暂未支持'):
        self.hot_reload = hot_reload
        self.wx = Core()
        self.handlers = {'text':[], 'map':[], 'picture':[], 'note':[]}
        self.enableCmdQR = self.judgmentSystem()
        self.default_msg = defaultMsg
    
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
        @self.wx.msg_register([TEXT], isGroupChat=False)
        def _dispatchText(msg):
            for h in self.handlers['text']:
                if h.match(msg):
                    self.wx.send(h.handle(msg), toUserName=msg['FromUserName'])

        @self.wx.msg_register([MAP], isGroupChat=False)
        def _dispatchMap(msg):
            for h in self.handlers['map']:
                if h.match(msg):
                    self.wx.send('@img@%s' % h.handle(msg) , msg['FromUserName'])

        @self.wx.msg_register([PICTURE], isGroupChat=False)
        def _dispatchPic(msg):
            for h in self.handlers['picture']:
                if h.match(msg):
                    self.wx.send(h.handle(msg), toUserName=msg['FromUserName'])
        
        @self.wx.msg_register([NOTE], isGroupChat=False)
        def _dispathNote(msg):
            for h in self.handlers['Note']:
                if h.match(msg):
                    self.wx.send(h.handle(msg), toUserName=msg['FromUserName'])
                    # 这个地方在加一个参数，去判断性别的吧~

        @self.wx.msg_register(FRIENDS)
        def add_friend(msg):
            self.wx.add_friend(**msg['Text'])
            self.wx.send_msg(u'很高兴遇到你', msg['RecommendInfo']['UserName'])

    def run(self):
        self.dispatch()
        self.wx.auto_login(hotReload=self.hot_reload, enableCmdQR=self.enableCmdQR)
        self.wx.run()