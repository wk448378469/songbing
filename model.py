# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 11:13:42 2017

@author: 凯风
"""

import web
import sae.const

def Link():
    db = sae.const.MYSQL_DB
    user = sae.const.MYSQL_USER
    pw = sae.const.MYSQL_PASS
    host = sae.const.MYSQL_HOST
    port = int(sae.const.MYSQL_PORT)
    return web.database(dbn='mysql', host=host, port=port, db=db, user=user, pw=pw)

db = Link()

def get_todos():
    return db.select('todo',order='id')

def new_todo(text):
    db.insert('todo',title=text)
    
def del_todo(id):
    db.delete('todo',where='id=$id',vars=locals())