# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 23:21:13 2017

@author: 凯风
"""

import psutil
import tushare as ts
import pandas as pd
import gc

class Register(object):
    """system monitor handler
    """
    def __init__(self,maindir):
        self.DEFAULT_MSG = u'指令暂未支持'
        self.type = 'text'
        self.maindir = maindir + '/wx_robot'
        self.sendPic = False
        
    def match(self, msg):
        if msg.text.startswith('@kaifeng '):
            return True
        else:
            return False

    def handle(self, msg):
        if any(p in msg.text for p in ['cpu', 'c', 'm', 'mem']):
            return self.sendPic ,self.cpu_mem()
        elif any(p in msg.text for p in ['update',u'更新']):
            return self.sendPic, self.updateStockList()
        elif any(p in msg.text for p in ['recovery',u'回收']):
            return self.sendPic, self.recoveryMemory()
        else:
            return self.sendPic ,self.DEFAULT_MSG 

    def cpu_mem(self):
        """return cpu memory usage
        """
        line = ''
        percs = psutil.cpu_percent(interval=0, percpu=True)
        for cpu_num, perc in enumerate(percs):
            line += 'CPU%-2s %5s%%\n' % (cpu_num, perc)
        mem = psutil.virtual_memory()
        line += 'Mem    %5s%% %6s / %s\n' % (
            mem.percent,
            str(int(mem.used / 1024 / 1024)) + 'M',
            str(int(mem.total / 1024 / 1024)) + 'M')
        return line
    
    def updateStockList(self):
        data = ts.get_stock_basics().index.to_series()
        data.to_csv(self.maindir + '/handler/predictStock/stockCodeList.csv', index=False)
        return 'success~'

    def recoveryMemory(self):
        gc.collect()
        return 'success~'