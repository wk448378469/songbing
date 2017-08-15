#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 16:57:48 2017

@author: kaifeng
"""


import urllib2
import time
import json

def detection(picurl):
    """人脸识别的方法
    相关：https://www.faceplusplus.com.cn/

    Args:
      picurl:本地图片的绝对路径 

    Returns:
      识别结果
    """
    httpUrl = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    key = 'I7bWVph8XNRCT8cXMw9GL2Ob4MsJ8DqS'
    secret = '5e_fj-GYIZkDRO5nHrh8STI6ZQg66s_V'
    returnAttributes = 'gender,age,emotion'
    boundary = '----------%s' % hex(int(time.time() *1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(returnAttributes)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    with open(picurl,'rb') as f:
        data.append(str(f.read()))
    data.append('--%s--\r\n' % boundary)
    http_body = '\r\n'.join(data)

    # request
    req = urllib2.Request(httpUrl)
    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    req.add_data(http_body)
    # link
    try:
        resp = urllib2.urlopen(req,timeout=5)
        return resultAnalysis(resp.read())
    except urllib2.HTTPError as e:
        print e.read()
        return None
        
    else:
        return None

def resultAnalysis(resultStr):
    """解析人脸获取的json
    Args:
      resultStr:json 

    Returns:
      解析结果
    """
    allContent = json.loads(resultStr)
    faceNum = len(allContent[u'faces'])
    if faceNum == 0:
        return u'未发现面部, 正进行图片转换，耐心等待哦...'
    elif faceNum == 1:
        age = str(allContent[u'faces'][0][u'attributes'][u'age'][u'value'])
        emotionList = [u'anger',u'disgust',u'fear',u'happiness',u'neutral', u'sadness',u'surprise']
        maxEmotion = ''
        maxValue = 0
        for emotion in emotionList:
            emotionValue = allContent[u'faces'][0][u'attributes'][u'emotion'][emotion]
            if emotionValue >= maxValue:
                maxValue = emotionValue
                maxEmotion = emotion.encode('utf-8')
                if maxEmotion == 'anger':
                    maxEmotion = '愤怒'
                elif maxEmotion == 'disgust':
                    maxEmotion = '厌恶'
                elif maxEmotion == 'fear':
                    maxEmotion = '恐惧'
                elif maxEmotion == 'happiness':
                    maxEmotion = '高兴'
                elif maxEmotion == 'neutral':
                    maxEmotion = '平静'
                elif maxEmotion == 'sadness':
                    maxEmotion = '伤心'
                else:
                    maxEmotion = '惊讶'
        returnData = '猜测年龄：%s , 表情看上去有些%s ,正进行图片转换，耐心等待哦...' % (age,maxEmotion)
        return unicode(returnData,'utf-8')
    else:
        return u'图片中的人有点多呀，正进行图片转换，耐心等待哦...'
