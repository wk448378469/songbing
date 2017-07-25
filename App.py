# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 15:00:20 2017

@author: 凯风
"""

import os
import web
from neuralstyle import myeval
import randomModel

class App:
    def __init__(self):
        self.render = web.template.render('templates', base='base')
    
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return self.render.uploadpic()
    
    def POST(self):
        x = web.input(myfile={})   
        filedir = '/userpic' 
        if 'myfile' in x: 
            filepath=x.myfile.filename.replace('\\','/') 
            filename=filepath.split('/')[-1]
            fout = open(filedir +'/'+ filename,'w') 
            fout.write(x.myfile.file.read()) 
            fout.close()
        
        modelFile = '/models/' + randomModel.randomModel()
        imageFile = filedir + '/' + filename

        myeval.neualstyle(modelFile,imageFile)
        returnPicPath = '/neuralstyle/neuralpic/' + filename
        return self.render.neulpic(returnPicPath)