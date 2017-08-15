#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 16:57:48 2017

@author: kaifeng
"""

import random

def randomModel():
    modelList = ['cubist.ckpt-done','denoised_starry.ckpt-done','feathers.ckpt-done','mosaic.ckpt-done','scream.ckpt-done','udnie.ckpt-done','wave.ckpt-done']
    return random.choice(modelList)
