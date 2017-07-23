# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 10:04:04 2017

@author: 凯风
"""

import sae
import os
import web

from App import App

urls = (
    '/','App',               # test 返回艺术风格图片
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root,base='base')

app = web.application(urls,globals()).wsgifunc()
application = sae.create_wsgi_app(app)