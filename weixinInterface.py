#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 16:57:48 2017

@author: kaifeng
"""


import hashlib
import web
import time
import os
from lxml import etree
import faceDetection
import urllib2
import randomModel
import test

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token = "songbingdiguo"
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update,list)
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = web.data()
        xml = etree.fromstring(str_xml)
        msgType = xml.find('MsgType').text
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        if msgType == 'image':
            #picurl = xml.find('PicUrl').text
            #filecontent = urllib2.urlopen(picurl)
            #detectionResuilt = faceDetection.detection(filecontent.read())
            
            # make neural pic
            #neuralPicPath = neuralPic(picurl)
            #accessToken = basic.Basic().get_access_token()
            #userMedia = media.Media()
            #mediaId = userMedia.upload(accessToken,neuralPicPath,'image')
            #return self.render.reply_image(fromUser,toUser,int(time.time()),mediaId)
            # return self.render.reply_text(fromUser,toUser,int(time.time()),'Sorry , I have a error , please try again later...')
            mediaId = test.test()
            if 'access_token' not in mediaId:
                return self.render.text(fromUser,toUser,int(time.time()),mediaId)
            return self.render.reply_image(fromUser,toUser,int(time.time()),mediaId)
            # return self.render.reply_text(fromUser,toUser,int(time.time()),detectionResuilt)
        else:
            content = xml.find('Content').text
            return self.render.reply_text(fromUser,toUser,int(time.time()),content)
