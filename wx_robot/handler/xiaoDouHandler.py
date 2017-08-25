# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 23:21:25 2017

@author: 凯风
"""

import requests

class Register(object):
    """ xiaodou robot handler
    Referer: http://xiao.douqq.com/
    """

    def __init__(self):
        self.key = 'SUtPNW5GTk89bUtCYlp3V1pkPW9tZklNdVJJQUFBPT0'
        self.type = 'text'
        self.sendPic = False
        self.DEFAULT_MSG = u'Σ( ° △ °|||)︴, 聊天机器人挂机了...'
        
    def match(self, msg):
        return True

    def handle(self, msg):
        url = 'http://api.douqq.com'
        params = {'key': self.key, 'msg': msg.text}
        print(msg.text)
        try:
            resp = requests.get(url, params=params)
            print (resp.text)
            return self.sendPic, resp.text
        except requests.exceptions.RequestException:
            return self.sendPic, self.DEFAULT_MSG