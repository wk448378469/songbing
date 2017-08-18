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
from sklearn.preprocessing import Imputer
import gc
from sklearn.metrics import mean_squared_error


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
        
        self.drawParameters = {}
        
        self.degree = 3
        self.gamma = 'auto'
        self.coef = 0.0
        self.tol = 0.001
        self.C = 1.0
        self.epsilon = 0.1
        
    def loadData(self):
        # 准备数据
        endTime = datetime.now()
        NexttradeDay = endTime + timedelta(days=1)
        NextTwotradeDay = endTime + timedelta(days=2)
        startTime = endTime - timedelta(days=300)
        
        endTime = endTime.strftime('%Y-%m-%d')
        startTime = startTime.strftime('%Y-%m-%d')
        NexttradeDay = NexttradeDay.strftime('%Y-%m-%d')
        NextTwotradeDay = NextTwotradeDay.strftime('%Y-%m-%d')
        
        # 读取基础数据
        stockData = ts.get_hist_data(self.code, start=startTime, end=endTime)
        
        # 判断基础数据是否足够，否则向上抛出一个异常
        if stockData.shape[0] <= 30:
            raise LessDataError()
        
        # 目标变量
        y = stockData['open']
        y = y[:-2]
        
        # 需要预测的数据
        X_pred = stockData[:2]
        
        # 特征数据
        stockData = stockData[2:]
        
        # 把数据缓存了以便之后画图使用
        self.drawParameters['Xaxis'] = stockData.index.values.tolist()
        self.drawParameters['Xaxis'].insert(0,NexttradeDay)
        self.drawParameters['Xaxis'].insert(0,NextTwotradeDay)
        self.drawParameters['Yaxis'] = y.values.tolist()
        
        # 分割数据集
        X_train, X_test, y_train, y_test = train_test_split(stockData,y,test_size=0.2)
        del stockData,y;gc.collect()

        # 处理数据
        featureEngineer = make_pipeline(Imputer(missing_values='NaN', strategy='mean'),StandardScaler())
        X_train = featureEngineer.fit_transform(X_train)
        X_test = featureEngineer.transform(X_test)
        X_pred = featureEngineer.transform(X_pred)
        y_test = np.log(y_test).values
        y_train = np.log(y_train).values
        
        return X_train,X_test,y_train,y_test,X_pred
        
    def trainAndPredict(self):
        
        # 创建模型下
        svrLinear = SVR(kernel= 'linear', C= self.C)
        svrPoly = SVR(kernel= 'poly', C= self.C, degree= self.degree)
        svrRbf = SVR(kernel= 'rbf', C= self.C, gamma= self.gamma)
        
        # 训练模型
        svrLinear.fit(self.X_train, self.y_train)
        svrPoly.fit(self.X_train, self.y_train)
        svrRbf.fit(self.X_train, self.y_train)
        
        # 训练集和测试集预测
        linearTrain = svrLinear.predict(self.X_train)
        polyTrain = svrPoly.predict(self.X_train)
        rbfTrain = svrRbf.predict(self.X_train)        
        linearTest = svrLinear.predict(self.X_test)
        polyTest = svrPoly.predict(self.X_test)
        rbfTest = svrRbf.predict(self.X_test)        
        
        # 训练集结果
        trainLinearMSE = mean_squared_error(np.exp(self.y_train), np.exp(linearTrain))
        trainPolyMSE = mean_squared_error(np.exp(self.y_train), np.exp(polyTrain))
        trainRbfMSE = mean_squared_error(np.exp(self.y_train), np.exp(rbfTrain))
        self.drawParameters['trainLinearMSE'] = trainLinearMSE
        self.drawParameters['trainPolyMSE'] = trainPolyMSE
        self.drawParameters['trainRbfMSE'] = trainRbfMSE
        
        # 测试集结果
        testLinearMSE = mean_squared_error(np.exp(self.y_test), np.exp(linearTest))
        testPolyMSE = mean_squared_error(np.exp(self.y_test), np.exp(polyTest))
        testRbfMSE = mean_squared_error(np.exp(self.y_test), np.exp(rbfTest))
        self.drawParameters['testLinearMSE'] = testLinearMSE
        self.drawParameters['testPolyMSE'] = testPolyMSE
        self.drawParameters['testRbfMSE'] = testRbfMSE
        
        # 预测数据
        linearResult = np.exp(svrLinear.predict(self.X_pred))
        polyResult = np.exp(svrPoly.predict(self.X_pred))
        rbfResult = np.exp(svrRbf.predict(self.X_pred))
        finalresult = (linearResult + polyResult + rbfResult) / 3
        self.drawParameters['linearResult'] = linearResult
        self.drawParameters['polyResult'] = polyResult
        self.drawParameters['rbfResult'] = rbfResult        
        self.drawParameters['finalresult'] = finalresult
                           
    def drawing(self):
        pass
