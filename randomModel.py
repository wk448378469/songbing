#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 16:57:48 2017

@author: kaifeng
"""

import random
from sae.storage import Bucket,Connection


def randomModel():
    c=Connection()
    bucket=c.get_bucket('models')
    
    allcontent = [i for i in bucket.list()]
    modelList = []
    for i in range(len(allcontent)):
        modelList.append(allcontent[i]['name'].encode('utf-8'))
    
    return random.choice(modelList)