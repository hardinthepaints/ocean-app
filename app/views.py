#!/usr/bin/env python

from flask import send_from_directory, Response, request, jsonify, url_for, abort

#import modules
from app import app, compress_functions
from app.db import db_functions
gzipped = compress_functions.gzipped
zipp = compress_functions.zipp
getTableAsJson = db_functions.getTableAsJson
getCompressedTable = db_functions.getCompressedTable

import os
import json as JSON
import warnings
from time import sleep
from math import sqrt
import time

#cross origin resource sharing library
from flask_cors import CORS, cross_origin

# disable autodoc internal Warning
# https://github.com/acoomans/flask-autodoc/issues/27
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter('ignore', ExtDeprecationWarning)

#setup auto doc decorator
from flask.ext.autodoc import Autodoc
auto = Autodoc(app)

app.config['dataFN'] = 'app/static/ocean_his_0002.nc'

#Index - uncomment to make active endpoint
@app.route('/oceanapp/v1.0/app/static/<path:path>', methods=['GET'])
@auto.doc(groups=['private', 'public'])
def index(path): 
    directory = 'app/static/'
    return add_header( send_from_directory( directory, path) )

#Get data from the sql db.
@app.route('/oceanapp/v1.0/json', methods=['GET'])
@auto.doc(groups=['private', 'public'])
@cross_origin(allow_headers="*", expose_headers="Content-length")
def json():
    """Return json data from the sql db. Login required. If 'gzip=true' in query, then the response will be compressed."""
    status = 200
    
    start = time.time()
    
    #store data in a string, which is correct json format
    output = getCompressedTable()
    r = Response( output, status=status,  content_type='application/json')        
    #return with the appropriate headers
    return compress_functions.addHeaders(r)


def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
    
#Error Handling    
@app.errorhandler(404)
def not_found(error):
    """Make the 404 response json instead of the default html"""
    return jsonify(error=str(error)), 404

#Documentation endpoints
@app.route('/oceanapp/v1.0/doc/')
@app.route('/oceanapp/v1.0/doc/public', methods=['GET'])
@auto.doc(groups=['public'])
def public_doc():
    """Documentation for this api."""
    return auto.html(groups=['public'], title='Ocean App Web Service Public Documentation')

@app.route('/oceanapp/v1.0/doc/private', methods=['GET'])
@auto.doc(groups=['private'])
def private_doc():
    """Display documentation for how to use this api and private functions"""
    return auto.html(groups=['private'], title='Ocean App Web Service Private Documentation')



            

       





    
    

