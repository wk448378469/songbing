# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:45:29 2017

@author: 凯风
"""

from predictStock import test
import pandas as pd

class Register(object):
    """predict stock prices handler
    """
    def __init__(self):
        self.type = 'text'
        self.stockCode = None
        self.DEFAULT_MSG = u'股票代码不存在请重试'
        
    def match(self, msg):
        if msg.text.startswith(u'预测') and len(msg.text[2:]) == 6:
            return True
        else:
            return False

    def handle(self, msg):
        if self.checkStockCode(msg.text):
            self.stockCode = msg[2:]
            userModel = test.mySVR(self.stockCode)
            
            userModel.trainAndPredict()
        else:
            return self.DEFAULT_MSG
            
    def checkStockCode(self, msg):
        code = msg[2:]
        codelist = pd.read_csv('D:/mygit/songbing/wx_robot/handler/predictStock/stockCodeList.csv',header=None,dtype='str')
        
        if code in codelist.values:
            return True
        else:
            return False