# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 15:00:20 2017

@author: 凯风
"""

import os
import web
from sae.ext.storage import monkey
from sae.storage import Bucket
from neuralstyle import myeval
import randomModel

class App:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
    
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return self.render.uploadpic()
    
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
        
        modelFile = '/s/models/' + randomModel.randomModel()
        imageFile = filedir + '/' + filename

        myeval.neualstyle(modelFile,imageFile)

        bucket = Bucket('neuralpic')
        returnPicPath = bucket.generate_url(filename)
        return self.render.neulpic(returnPicPath)