# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 23:21:02 2017

@author: 凯风
"""


class Register(object):
    """public message handler
    """
    def __init__(self):
        self.type = 'text'
        self.sendPic = False
        self.HELP_MSG = u'''发送图片：预测年龄，表情信息，并将其与转换艺术风格

发送文本“@代码”：获取该机器人完整代码

发送文本“@预测600000”：预测股票代码600000下一个交易日的开盘价

发送文本“@说明”：获取该机器人涉及的机器学习及深度学习的说明

发送文本：机器人会和你聊天哦'''
    
    def match(self, msg):
        if msg.text == u'@帮助' or msg.text == u'@代码':
            return True
        else:
            return False

    def handle(self, msg):
        if msg.text == u'@帮助':
            return self.sendPic, self.HELP_MSG
        elif msg.text == u'@代码':
            return self.sendPic, 'https://github.com/wk448378469/songbing'
        else:
            return self.sendPic, 'wrong message'