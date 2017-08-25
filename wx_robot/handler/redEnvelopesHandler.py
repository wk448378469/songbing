# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 01:33:32 2017

@author: 凯风
"""


class Register(object):
    """received a red envelopes handler
    """
    def __init__(self):
        self.type = 'note'
        self.sendPic = False
    
    def match(self, msg):
        if msg.text == u'收到红包，请在手机上查看':
            return True
        return False

    def handle(self,msg):
        return self.sendPic, u'(≖ ‿ ≖)✧谢谢老板的红包'
