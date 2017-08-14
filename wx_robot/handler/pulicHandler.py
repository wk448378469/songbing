# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 23:21:02 2017

@author: 凯风
"""

class Register(object):

    def __init__(self):
        self.type = 'text'
        self.HELP_MSG = u'''\
                    欢迎使用开发机器人
                    发送图片：转化为艺术风格
                    发送定位：预测PM2.5
                    发送代码：获取源代码
                    发送说明：获取说明推送
                    '''
    
    def match(self, msg):
        if msg.text in [u'帮助', u'代码', u'说明']:
            return True
        return False

    def handle(self, msg):
        if msg.text == u'帮助':
            return self.HELP_MSG
        if msg.text == u'代码':
            return 'https://github.com/wk448378469/songbing'
        if msg.text == u'说明':
            return 'https://mp.weixin.qq.com/s?__biz=MzA3NjQzODkxNQ==&mid=202277885&idx=1&sn=8223df8808c842e959f38263c3aaf480&mpshare=1&scene=1&srcid=0813cyvJpBv3jrhz3zK0rAyj#rd'

