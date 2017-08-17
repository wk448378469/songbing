# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:54:19 2017

@author: 凯风
"""

import tushare as ts
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from datetime import datetime,timedelta
from sklearn.pipeline import make_pipeline


class LessDataError(LookupError):
    pass


class mySVR(object):

    def __init__(self,userInput):
        self.code = userInput
        self.loadDataSuccess = True
        self.returnMessage = None
        
        try:
            self.X_train, self.X_test, self.y_train, self.y_test, self.X_pred = self.loadData()
            self.returnMessage = u'正在获取数据并继续机器学习，请耐心等待...'
        except LessDataError as L:
            self.loadDataSuccess = False
            self.returnMessage =  u'这只股票貌似刚上市，数据不足无法预测'
        finally:
            self.loadDataSuccess = False
            self.returnMessage = u'读取数据错误，请稍后重试'
                
        
    def loadData(self):
        # 准备数据
        endTime = datetime.now()
        startTime = endTime - timedelta(days=200)
        endTime = endTime.strftime('%Y-%m-%d')
        startTime = startTime.strftime('%Y-%m-%d')
        
        # 读取基础数据
        stockData = ts.get_hist_data(self.code, start=startTime, end=endTime)
        
        # 判断基础数据是否足够，否则向上抛出一个异常
        if stockData.shape[0] <= 30:
            raise LessDataError()
        
        y = stockData['open']
        X = stockData.drop(['open'],axis=1,inplace=True)
        

        return None
        
    def trainAndPredict(self):
        # 创建模型下
        svrLinear = SVR(kernel= 'linear', C= 1e3)
        svrPoly = SVR(kernel= 'poly', C= 1e3, degree= 2)
        svrRbf = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1)
        
        # 训练模型
        svrLinear.fit(self.X_train, self.y_train)
        svrPoly.fit(self.X_train, self.y_train)
        svrRbf.fit(self.X_train, self.y_train)
        
        # 预测数据
        svrLinear.predict(self.X_pred)
    
    
        