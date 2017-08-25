# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:45:29 2017

@author: 凯风
"""

from predictStock import test
import pandas as pd
import gc
import re

class parametersError(LookupError):
    pass


class Register(object):
    """predict stock prices handler
    """
    def __init__(self, maindir):
        self.type = 'text'
        self.stockCode = None
        self.maindir = maindir + '/wx_robot/handler/predictStock'
        self.codeList = self.loadCodeList()
        self.sendPic = True
        self.DEFAULT_MSG = u'股票代码不存在，请重试'
    
    
    def loadCodeList(self):
        return pd.read_csv(self.maindir+'/stockCodeList.csv', header=None, dtype='str')[0].values
    
    def match(self, msg):
        if msg.text.startswith(u'@预测'):
            return True
        else:
            return False

    def handle(self, msg):
        self.stockCode = msg.text[3:9]
        if self.checkStockCode():
            try:
                parameters = self.parseParameters(msg)
            except parametersError:
                return not self.sendPic, self.DEFAULT_MSG
            
            userModel = test.mySVR(self.stockCode , parameters , self.maindir)
            
            if userModel.loadDataSuccess:
                picUrl = userModel.trainAndPredict()
                msg.user.send(userModel.returnMessage)
                return self.sendPic , picUrl
            else:
                message = userModel.returnMessage
                del userModel;gc.collect()
                return not self.sendPic, message
        else:
            return not self.sendPic, self.DEFAULT_MSG
            
    def checkStockCode(self):
        if self.stockCode in self.codeList:
            return True
        else:
            return False
        
    def parseParameters(self, msg):
        parameters = {}
        parameters['degree'] = 3 # 多项式核的参数，在其他核时无效
        parameters['coef'] = 0.0
        parameters['tol'] = 0.001 # 容错率精度
        parameters['C'] = 1.0 # 惩罚项系数
        parameters['epsilon'] = 0.1
        msg = msg.text.split(' ')[1:]
        if len(msg) == 0 :
            return parameters
        
        else:
            for parameter in msg:
                if 'degree' in parameter:
                    try:
                        num = re.findall('[0-9,.]', parameter)
                        strNum = ''
                        for i in num:
                            strNum = strNum + i
                        parameters['degree'] = int(strNum)
                    except:
                        self.DEFAULT_MSG = u'degree is bad numbers'
                        raise parametersError()
                    
                elif 'coef' in parameter:
                    try:
                        num = re.findall('[0-9,.]', parameter)
                        strNum = ''
                        for i in num:
                            strNum = strNum + i
                        parameters['coef'] = float(strNum)
                    except:
                        self.DEFAULT_MSG = u'coef is bad numbers'
                        raise parametersError()
                        
                elif 'tol' in parameter:
                    try:
                        num = re.findall('[0-9,.]', parameter)
                        strNum = ''
                        for i in num:
                            strNum = strNum + i
                        parameters['tol'] = float(strNum)
                    except:
                        self.DEFAULT_MSG = u'tol is bad numbers'
                        raise parametersError()
                    
                elif 'C' in parameter:
                    try:
                        num = re.findall('[0-9,.]', parameter)
                        strNum = ''
                        for i in num:
                            strNum = strNum + i
                        parameters['C'] = float(strNum)
                    except:
                        self.DEFAULT_MSG = u'C is bad numbers'
                        raise parametersError()
                    
                elif 'epsilon' in parameter:
                    try:
                        num = re.findall('[0-9,.]', parameter)
                        strNum = ''
                        for i in num:
                            strNum = strNum + i
                        parameters['epsilon'] = float(strNum)
                    except:
                        self.DEFAULT_MSG = u'epsilon is bad numbers'
                        raise parametersError()
                
        return parameters
                
                
                
                
                
                
                
                
                
                
                