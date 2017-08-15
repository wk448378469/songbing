# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 23:20:36 2017

@author: 凯风
"""

class Register(object):
    """map predict pm 2.5 handler
    """
    def __init__(self):
        self.type = 'map'

    def match(self, msg):
        return True

    def handle(self, msg):
        return u'预测PM2.5功能开发中，暂未完成'
