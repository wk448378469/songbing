#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 16:57:48 2017

@author: kaifeng
"""

import random
import os

def randomModel():
    modelList = os.listdir('models')
    return random.choice(modelList)