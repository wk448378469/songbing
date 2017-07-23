#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 10:47:45 2017

@author: kaifeng
"""

from __future__ import print_function
import tensorflow as tf
from sae.ext.storage import monkey

import preprocessing_factory
import reader
import model

def neualstyle(model_file,image_file):
    
    # sae的storage可以以文件路径的形式访问 
    monkey.patch_all()
    # 初始化参数
    loss_model = 'vgg_16'
    height = 0
    width = 0
    
    # 读取图片，并将图片转化为tensor张量
    with open(image_file,'rb') as img:
        with tf.Session().as_default() as sess:
            if image_file.lower().endswith('png'):
                # 将图片转化为张量，tensor，[height,width,channels]
                image = sess.run(tf.image.decode_png(img.read()))
            else:
                image = sess.run(tf.image.decode_jpeg(img.read()))
            height = image.shape[0]
            width = image.shape[1]
    
    with tf.Graph().as_default():
        with tf.Session().as_default() as sess:
            # 获取处理图片的方法
            image_preprocessing_fn , _ = preprocessing_factory.get_preprocessing(loss_model,is_training=False)
            # 获取预处理后的tensor
            image = reader.get_image(image_file,height,width,image_preprocessing_fn)
            # 添加一个维度，oldshape=[height,width,3] ——> newshape=[1,height,width,3]
            image = tf.expand_dims(image,0)
            
            # 获取神经网络
            generated = model.net(image,training=False)
            generated = tf.cast(generated,tf.uint8)
            
            # 去掉增加的维
            generated = tf.squeeze(generated, [0])
            
            # 保存模型的变量
            saver = tf.train.Saver(tf.global_variables(), write_version=tf.train.SaverDef.V1)
            sess.run([tf.global_variables_initializer(), tf.local_variables_initializer()])
            saver.restore(sess, model_file)
            
            # 保存图片
            generated_name = image_file.split('/')[-1]
            generated_file = '/s/neuralpic/' + generated_name
            with open(generated_file,'wb') as img:
                img.write(sess.run(tf.image.encode_jpeg(generated)))