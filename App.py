# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 23:09:46 2017

@author: 凯风
"""

from wx_robot import handler
from wx_robot.robot import wxRobot

if __name__ == '__main__':
    
    predPm25 = handler.predPm25Handler.Register()
    neural = handler.neuralHandler.Register()
    public = handler.pulicHandler.Register()
    myself = handler.myselfHandler.Register()
    xiaoDou = handler.xiaoDouHandler.Register()
    redEnvelopes = handler.redEnvelopesHandler.Register()
    
    robot = wxRobot()
    robot.registerHandler(predPm25, predPm25.type)
    robot.registerHandler(neural, neural.type)
    robot.registerHandler(public, public.type)
    robot.registerHandler(myself, myself.type)
    robot.registerHandler(redEnvelopes, redEnvelopes.type)
    robot.registerHandler(xiaoDou, xiaoDou.type)

    robot.run()