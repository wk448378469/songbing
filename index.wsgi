# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 10:04:04 2017

@author: 凯风
"""

import sae
import os
import web
import model
from sae.ext.storage import monkey
from sae.storage import Bucket

urls = (
    '/','Index',
    '/del/(\d+)','Delete',
    '/upload','Upload'                  # test 图片上传
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root,base='base')

class Index:
    form = web.form.Form(web.form.Textbox('title',web.form.notnull,description='I need to:'),
                         web.form.Button('Add todo'))
    def GET(self):
        todos = model.get_todos()
        form = self.form()
        return render.index(todos,form)
    
    def POST(self):
        form = self.form()
        if not form.validates():
            todos = model.get_todos()
            return render.index(todos,form)
        model.new_todo(form.d.title)
        raise web.seeother('/')


class Delete:
    def POST(self,id):
        id = int(id)
        model.del_todo(id)
        raise web.seeother('/')

class Upload:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render.uploadpic()
    
    def POST(self):
        monkey.patch_all()
        x = web.input(myfile={})   
        filedir = '/s/userpic' 
        if 'myfile' in x: 
            filepath=x.myfile.filename.replace('\\','/') 
            filename=filepath.split('/')[-1]
            fout = open(filedir +'/'+ filename,'w') 
            fout.write(x.myfile.file.read()) 
            fout.close()
        
        returnPic = '11.jpg'
        bucket = Bucket('neuralpic')
        returnPicPath = bucket.generate_url(returnPic)
        return render.neulpic(returnPicPath)
        
        
        
        raise web.seeother('/upload')

app = web.application(urls,globals()).wsgifunc()
application = sae.create_wsgi_app(app)