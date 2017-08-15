# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 23:09:46 2017

@author: 凯风
"""

from wx_robot.handler import myselfHandler,neuralHandler,predPm25Handler,pulicHandler,redEnvelopesHandler,xiaoDouHandler 
from wx_robot.robot import wxRobot
import os

if __name__ == '__main__':
    
    # 获取当前路径
    MAINDIR = os.getcwd()
    
    # 创建处理器的实例
    predPm25 = predPm25Handler.Register()
    neural = neuralHandler.Register(MAINDIR)
    public = pulicHandler.Register()
    myself = myselfHandler.Register()
    xiaoDou = xiaoDouHandler.Register()
    redEnvelopes = redEnvelopesHandler.Register()
    
    # 创建机器人的实例
    robot = wxRobot(maindir = MAINDIR)

    # 注册处理器
    robot.registerHandler(predPm25, predPm25.type)
    robot.registerHandler(neural, neural.type)
    robot.registerHandler(public, public.type)
    robot.registerHandler(myself, myself.type)
    robot.registerHandler(redEnvelopes, redEnvelopes.type)
    robot.registerHandler(xiaoDou, xiaoDou.type)
    
    robot.run()
