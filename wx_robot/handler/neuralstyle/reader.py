#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 10:48:26 2017

@author: kaifeng
"""

from os import listdir
from os.path import isfile , join
import tensorflow as tf

def get_image(path,height,width,preprocess_fn):
    # 判断图片是否以png结尾
    png = path.lower().endswith('png')
    
    # 读取输入文件的全部内容，返回tensor张量
    img_bytes = tf.read_file(path)
    
    # 将图片内容转化为tensor，但是没有run哦
    image = tf.image.decode_png(img_bytes,channels=3) if png else tf.image.decode_jpeg(img_bytes,channels=3)
    
    # 调用传入的方法，返回预处理后的图片
    return preprocess_fn(image,height,width)