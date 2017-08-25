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

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from datetime import datetime,timedelta
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Imputer
from sklearn.metrics import mean_squared_error


class LessDataError(LookupError):
    pass


class mySVR(object):

    def __init__(self, stockCode, parameters, maindir):
        self.code = stockCode
        self.loadDataSuccess = True
        self.returnMessage = None
        self.drawParameters = {}
        self.maindir = maindir + '/predictResult/'
        try:
            self.X_train, self.X_test, self.y_train, self.y_test, self.X_pred = self.loadData()
            if self.drawParameters['predictDays'] == 1:
                self.returnMessage = u'无法获取今日的收盘数据，正预测下一个交易日的开盘价，请耐心等待...'
            else:
                self.returnMessage = u'正在预测下两个交易日的开盘价，请耐心等待...'
        except LessDataError:
            self.loadDataSuccess = False
            self.returnMessage =  u'这只股票貌似刚上市或未上市，数据不足无法预测'
        
        self.degree = parameters['degree']
        self.coef = parameters['coef']
        self.tol = parameters['tol']
        self.C = parameters['C']
        self.epsilon = parameters['epsilon']
        
    def loadData(self):
        # 准备数据
        currentTime = datetime.now()
        self.picname = self.code + '-' + currentTime.strftime('%Y-%m-%d-%H-%M-%S') + '.png'
        startTime = currentTime - timedelta(days=300)        
        endTime = currentTime.strftime('%Y-%m-%d')
        startTime = startTime.strftime('%Y-%m-%d')
        
        # 读取基础数据
        stockData = ts.get_hist_data(self.code, start=startTime, end=endTime)
        
        # 判断基础数据是否足够，否则向上抛出一个异常
        if stockData is None:
            raise LessDataError()
        
        if stockData.shape[0] <= 30:
            raise LessDataError()
        
        
        # 怎么解释这里呢...
        if currentTime.weekday() <= 4:
            self.drawParameters['predictDays'] = 1 if endTime != str(stockData.index[0]) else 2
        else:
            self.drawParameters['predictDays'] = 2
        
        # 计算下一个（两个）交易日的日期
        self.calcDate()
        
        # 目标变量
        y = stockData['open']
        y = y[:-self.drawParameters['predictDays']]
        
        # 需要预测的数据
        X_pred = stockData[:self.drawParameters['predictDays']]
        
        # 特征数据
        stockData = stockData[self.drawParameters['predictDays']:]
        
        # 把数据缓存了以便之后画图使用
        self.drawParameters['Xaxis'] = stockData.index.values.astype(str).tolist()
        self.drawParameters['Xaxis'].reverse()
        self.drawParameters['Yaxis'] = y.values.tolist()
        self.drawParameters['Yaxis'].reverse()
        
        # 分割数据集
        X_train, X_test, y_train, y_test = train_test_split(stockData,y,test_size=0.2)

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
        svrLinear = SVR(kernel= 'linear', C= self.C , epsilon = self.epsilon, tol=self.tol)
        svrPoly = SVR(kernel= 'poly', C= self.C, degree= self.degree, epsilon = self.epsilon, coef0=self.coef, tol=self.tol)
        svrRbf = SVR(kernel= 'rbf', C= self.C ,epsilon = self.epsilon, tol=self.tol)
        
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
        
        return self.drawing()
                           
    def drawing(self):
        plt.style.use('fivethirtyeight')
        fig = plt.figure(figsize=(12,6.5), dpi=100)
        fig.suptitle('stock:%s opening price predict ' % self.code, fontsize=20)
        ax1 = plt.subplot(211)
        line = ax1.plot_date(self.drawParameters['Xaxis'],self.drawParameters['Yaxis'],linestyle="-",marker="None", linewidth=1.2)
        for i in range(self.drawParameters['predictDays']):
            plot = ax1.scatter([self.drawParameters['newDates'][i]],[self.drawParameters['finalresult'][i]],color='red')
        ax1.legend((line,plot),('','next predict'))
        
        ax2 = plt.subplot(212)
        ax2.set_axis_off()
        col_labels = ['linear','ploy','rbf']
        col_colors = [(0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0)]
        row_labels = ['trainMAE','testMAE','nextDayOpenPricePredict']
        row_colors = [(0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0)]
        table_vals = [[self.drawParameters['trainLinearMSE'],self.drawParameters['trainPolyMSE'],self.drawParameters['trainRbfMSE']],
                      [self.drawParameters['testLinearMSE'],self.drawParameters['testPolyMSE'],self.drawParameters['testRbfMSE']],
                      [self.drawParameters['linearResult'][0],self.drawParameters['polyResult'][0],self.drawParameters['polyResult'][0]]]
        cell_colors = [[(0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0)],
                        [(0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0)],
                        [(0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0)]]
        if self.drawParameters['predictDays'] == 2:
            row_labels.append('nextTwoDayOpenPricePredict')
            row_colors.append((0, 0, 0, 0))
            cell_colors.append([(0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0)])
            table_vals.append([self.drawParameters['linearResult'][1],self.drawParameters['polyResult'][1],self.drawParameters['polyResult'][1]])
        
        ax2.table(cellText=table_vals, cellColours=cell_colors ,colWidths=[0.14]*10, rowColours=row_colors,
                  rowLabels=row_labels, colLabels=col_labels, colColours=col_colors , loc='center')        
        ax2.text(0.1,0.2,'The opening price is forecast at %.2f on the next trading day'%self.drawParameters['finalresult'][0],fontsize=15)
        if self.drawParameters['predictDays'] == 2:
            ax2.text(0.08,0.1,' The opening price forecast for the next two trading days is %.2f '%self.drawParameters['finalresult'][1],fontsize=15)
        ax2.text(0.2,-0.05,'finalresult = (linearResult + polyResult + rbfResult) / 3',fontsize=10 ,color='red')
        
        returnUrl = self.maindir + self.picname
        
        plt.savefig(returnUrl)
        
        return returnUrl
        
        
    def calcDate(self):
        weekDay = datetime.now().weekday()
        self.drawParameters['newDates'] = np.zeros((self.drawParameters['predictDays'],),dtype='S10')
        if weekDay <= 2:
            for i in range(self.drawParameters['predictDays']):
                self.drawParameters['newDates'][i] =  (datetime.now() + timedelta(days=i+1)).strftime('%Y-%m-%d')
        elif weekDay == 3 and self.drawParameters['predictDays'] == 1:
            self.drawParameters['newDates'][0] = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        elif weekDay == 3 and self.drawParameters['predictDays'] == 2:
            self.drawParameters['newDates'][0] = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            self.drawParameters['newDates'][1] = (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d')
        elif weekDay == 4 and self.drawParameters['predictDays'] == 1:
            self.drawParameters['newDates'][0] = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        elif weekDay == 4 and self.drawParameters['predictDays'] == 2:
            self.drawParameters['newDates'][0] = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
            self.drawParameters['newDates'][1] = (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d')
        elif weekDay == 5:
            for i in range(self.drawParameters['predictDays']):
                self.drawParameters['newDates'][i] = (datetime.now() + timedelta(days=i+2)).strftime('%Y-%m-%d')
        elif weekDay == 6:
            for i in range(self.drawParameters['predictDays']):
                self.drawParameters['newDates'][i] = (datetime.now() + timedelta(days=i+1)).strftime('%Y-%m-%d')