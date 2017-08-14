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

    DEFAULT_MSG = u'Σ( ° △ °|||)︴, 聊天机器人挂机了...'

    def __init__(self):
        self.key = 'SUtPNW5GTk89bUtCYlp3V1pkPW9tZklNdVJJQUFBPT0'
        self.type = 'text'
        
    def match(self, msg):
        return True

    def handle(self, msg):
        url = 'http://api.douqq.com'
        params = {'key': self.key, 'msg': msg.text}
        try:
            resp = requests.get(url, params=params)
        except requests.exceptions.RequestException:
            return self.DEFAULT_MSG
        return resp.text