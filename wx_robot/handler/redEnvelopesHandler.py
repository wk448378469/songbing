# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 01:33:32 2017

@author: 凯风
"""


class Register(object):

    def __init__(self):
        self.type = 'note'
        self.HELP_MSG = '~'
    
    def match(self, msg):
        if msg.text == u'收到红包，请在手机上查看':
            return True
        return False

    def handle(self, msg):
        return 'thanks'
