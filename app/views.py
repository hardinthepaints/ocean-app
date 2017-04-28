#!/usr/bin/env python

from flask import send_from_directory, Response, request, jsonify, url_for, abort

#import modules
from app import app, db_functions, auth_functions, compress_functions, netcdf_functions
gzipped = compress_functions.gzipped
zipp = compress_functions.zipp
auth = auth_functions.auth
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
@app.route('/oceanapp/v1.0/jsonsql', methods=['GET'])
@auto.doc(groups=['private', 'public'])
@cross_origin(allow_headers="*", expose_headers="Content-length")
@auth.login_required
def jsonsql():
    """Return json data from the sql db. Login required. If 'gzip=true' in query, then the response will be compressed."""
    status = 200
    
    start = time.time()
    #store data in a string, which is correct json format
    if (request.args.get("precomp")):
        output = getCompressedTable()
        r = Response( output, status=status,  content_type='application/json')        
        #return with the appropriate headers
        return compress_functions.addHeaders(r)
    else:
        outputJson = getTableAsJson()

        
        r = Response( outputJson, status=status,  content_type='application/json')
        
        #if the request contains 'gzip' in the query, then compress them
        if (request.args.get("gzip")):
            return zipp(r)
        return r


#Get data from .nc files
@app.route('/oceanapp/v1.0/json/<date>', methods=['GET'])
@auto.doc(groups=['private', 'public'])
@cross_origin(allow_headers="*")
def json(date):
    """Return json data based on params, queried from netCDF files. The date argument should be in yyyymmdd format. """
    date=str(date)
    status = 200
        
    args = request.args
    
    try:
        hours = args.getlist("hours")
        if (len(hours) == 0): abort(404)
    except:
        abort(404)
        
    output = { "url":url_for('json', date=date, hours=args.getlist("hours"), _external=True)}
    
    frames = {}
    def checkHour(hour):
        
        #key format yyyymmddhh
        key = date + hour.zfill(2)
        if ( hourIsReal(hour)):
            frames[ key ] = {"id":hour.zfill(4)}
        else:
            pass
            #frames[ key ] = None
    
        
    for val in hours:
        checkHour(val)    
        
    
    for key in frames.keys():
        if (frames[ key ] != None):
            identity = frames[key]['id']
            frames[ key ]['z'] = netcdf_functions.getDataByHour(date, identity) 
    
    output["hoursData"] = frames

    return jsonify( output ), status

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

#HELPER FUNCTIONS
def getInt( value ):
    """Attempt to convert to an int and if fail then return None"""
    try:
        return int(value)
    except ValueError:
        return None
    
def hourIsReal( hour ):
    """Check if the hour is a real hour in our dataset"""
    hour = getInt( hour )
    if hour == None:
        return False
    if hour not in range(2, 73):
        return False
    return True


            

       





    
    

