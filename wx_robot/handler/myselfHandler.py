# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 23:21:13 2017

@author: 凯风
"""
import psutil

class Register(object):
    """system monitor handler
    """
    def __init__(self):
        self.DEFAULT_MSG = u'指令暂未支持'
        self.type = 'text'
        
    def match(self, msg):
        if msg.text.startswith('/m') and msg['FromUserName']=='xxxx':
            return True
        return False

    def handle(self, msg):
        if any(p in msg.text for p in ['cpu', 'c', 'm', 'mem']):
            return self.cpu_mem()
        return self.DEFAULT_MSG

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