# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 23:20:51 2017

@author: 凯风
"""
from itchat.content import PICTURE
from neuralstyle.randomModel import randomModel
from neuralstyle.myeval import neualstyle
from faceDetection.faceDetection import detection

class Register(object):
    """picture handler
    """
    def __init__(self,maindir):
        self.type = 'picture'
        self.maindir = maindir + '/wx_robot/handler/neuralstyle'
        self.sendPic = True
        
    def match(self, msg):
        if msg.FileName.split('.')[-1] in ['png','jpg','jpeg']:
            return True
        else:
            return False

    def handle(self, msg, picpath):
        """return image processing results
        """
        # 人脸识别
        detectionResuilt = detection(picpath)
        msg.user.send(detectionResuilt)
        
        # 艺术风格图片转换
        modelFile = self.maindir + '/models/' + randomModel()
        print(modelFile)
        try:
            print(picpath)
            neualstyle(modelFile, picpath)
            returnPicPath = self.maindir + '/neuralpic/' + msg['FileName']
            return self.sendPic , returnPicPath
        except:
            return not self.sendPic,  u'(*´Д｀*) ，图片转换失败，请重试'
