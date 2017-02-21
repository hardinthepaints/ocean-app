#!/usr/bin/env python

'''
Views are handlers that respond to request from clients. In Flask,
handlers are written as python functions
'''

from app import app

#The following urls will map to this view
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

