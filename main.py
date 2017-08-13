# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 10:04:04 2017

@author: 凯风
"""

import itchat
from itchat.content import *
import randomModel
from neuralstyle import myeval
import os

MAINDIR = os.getcwd()
HELP_MSG = u'''\
欢迎使用开发机器人
发送图片：转化为艺术风格
发送定位：预测PM2.5
发送代码：获取源代码
发送说明：获取说明推送
'''

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    print(msg['Text'])
    itchat.add_friend(**msg['Text'])
    itchat.send_msg(HELP_MSG, msg['RecommendInfo']['UserName'])

@itchat.msg_register(TEXT, isGroupChat=False)
def text_reply(msg):
    if u'帮助' in msg['Text']:
        itchat.send(HELP_MSG, msg['FromUserName'])
    if u'代码' in msg['Text']:
        itchat.send('https://github.com/wk448378469/songbing', msg['FromUserName'])
    if u'说明' in msg['Text']:
        itchat.send('https://mp.weixin.qq.com/s?__biz=MzA3NjQzODkxNQ==&mid=202277885&idx=1&sn=8223df8808c842e959f38263c3aaf480&mpshare=1&scene=1&srcid=0813cyvJpBv3jrhz3zK0rAyj#rd', msg['FromUserName'])

@itchat.msg_register(MAP,isGroupChat=False)
def map_reply(msg):
    print(msg['Content'])
    print(msg['Text'])
    itchat.send('%s: %s,%s' % (msg['Type'], msg['Text'], msg['Content']), msg['FromUserName'])
    # msg.user.send(u'PM2.5预测功能暂未完成')

@itchat.msg_register(PICTURE,isGroupChat=False)
def download_pic(msg):
    msg.user.send(u'(。・`ω´・)转换中，耐心些哦')
    picpath = MAINDIR + '/userpic/' + msg['FileName']
    msg['Text'](picpath)
    modelFile = MAINDIR + '/models/' + randomModel.randomModel()
    try:
        myeval.neualstyle(modelFile, picpath)
        returnPicPath = MAINDIR + '/neuralstyle/neuralpic/' + msg['FileName']
        itchat.send('@img@%s' % returnPicPath , msg['FromUserName'])
    except:
        itchat.send(u'(*´Д｀*) ，图片转换失败，请重试', msg['FromUserName'])

if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2)
    itchat.run()
