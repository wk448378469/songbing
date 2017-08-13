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
    data.append(picurl)
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
    allContent = json.loads(resultStr)
    faceNum = len(allContent[u'faces'])
    if faceNum == 0:
        return 'Not found face , picture is being artificially processed...'
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
        return 'Guess your age is %s , your expression looks like %s , picture is being artificially processed...' % (age,maxEmotion)
    else:
        return 'The number of people a little more , picture is being artificially processed...'
