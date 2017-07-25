# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 10:04:04 2017

@author: 凯风
"""

import os
import web

from App import App

urls = (
    '/','App',               # test 返回艺术风格图片
)

render = web.template.render('templates', base='base')

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()