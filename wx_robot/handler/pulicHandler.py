# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 23:21:02 2017

@author: 凯风
"""

help_msg = u'''发送图片：将其转化为艺术风格
发送定位：预测PM2.5(未完成)
发送代码：获取该机器人源代码
发送说明：获取机器人使用说明(未完成)'''

class Register(object):
    """public message handler
    """
    def __init__(self):
        self.type = 'text'
        self.HELP_MSG = help_msg
    
    def match(self, msg):
        if msg.text == u'帮助' or msg.text == u'代码' or msg.text == u'说明':
            return True
        else:
            return False

    def handle(self, msg):
        if msg.text == u'帮助':
            return self.HELP_MSG
        if msg.text == u'代码':
            return 'https://github.com/wk448378469/songbing'
        if msg.text == u'说明':
            return 'https://mp.weixin.qq.com/s?__biz=MzA3NjQzODkxNQ==&mid=202277885&idx=1&sn=8223df8808c842e959f38263c3aaf480&mpshare=1&scene=1&srcid=0813cyvJpBv3jrhz3zK0rAyj#rd'

