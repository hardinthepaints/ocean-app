#!/usr/bin/env python

import netCDF4 as nc
from flask import send_from_directory, Response, request, jsonify, url_for, abort

#import modules
from app import app, db_functions, auth_functions

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

from app import compress_functions
gzipped = compress_functions.gzipped

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

#Index - uncomment to make active endpoint
@app.route('/oceanapp/v1.0/app/static/<path:path>', methods=['GET'])
@auto.doc(groups=['private', 'public'])
def index(path): 
    directory = 'app/static/'
    return add_header( send_from_directory( directory, path) )

#Get data from the sql db.
@auto.doc(groups=['private', 'public'])
@app.route('/oceanapp/v1.0/jsonsql', methods=['GET'])
@gzipped
@cross_origin(allow_headers="*", expose_headers="Content-length")
@auth_functions.auth.login_required
def jsonsql():
    """Return json data from the sql db. Login required."""
    status = 200
    output = {}

    db = db_functions.get_db()
    
    #limit the number of rows to return
    limit = 75
    
    result = db.execute("select * from entries limit ?", [limit])
    queryResult = result.fetchall()
    
    #store data in a string, which is correct json format
    outputJson = "["
        
    for row in queryResult:
        outputJson += '{{ "z":{}, "yyyymmddhh":{} }},'.format( row[1], row[0] )
    outputJson = outputJson[0:-1] + "]"
    
    r = Response( outputJson, status=status,  content_type='application/json')
    return r

@app.route('/oceanapp/v1.0/stream_sqrt')
@auto.doc(groups=['public'])
def stream():
    def generate():
        for i in range(500):
            yield '{}\n'.format( sqrt(i) )
            #sleep(.05)

    return app.response_class(generate(), mimetype='text/plain')


#Get data from .nc files
@auto.doc(groups=['private', 'public'])
@app.route('/oceanapp/v1.0/json/<date>', methods=['GET'])
@cross_origin(allow_headers="*")
def json(date):
    """Return json data based on params, queried from netCDF files. The date arguement should be in yyyymmdd format."""
    date=str(date)
    status = 200
    
    #if the date is not on the system return not found
    if not os.path.exists("app/ncFiles/{}".format(date)):
        abort(404)
        
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
            frames[ key ]['z'] = getDataByHour(date, identity) 
    
    output["hoursData"] = frames

        
    return jsonify( output ), status

def getDataByHour(date, hour):
    """Get the top layer of salinity data for the given date and hour"""
    fileName = "app/ncFiles/{}/ocean_his_{}.nc".format( date, hour )
    return getData(1, 0, fileName)


#open a .nc file and collect data
#Return the specified number of layers
def getData( end, start, fileName ):
    """Get the given range of layers of salinity from the given .nc file. If the range only includes one layer, return None"""
    
    try:
        ds = nc.Dataset( fileName )
    except:
        return None
    
    #ensure the layers correspond to correct indexes
    end = min( end, len( ds.variables['salt'][0]) )
    end = max( end, 1 )
     
    salts = {}
    for i in range( start, end ):
        salt = ds.variables['salt'][0, i, :, :].squeeze()
        salt = salt.tolist()
        salts[i] = salt
    
    #close the dataset
    ds.close()
    
    if ( len(salts) == 0 ): return None
    elif ( len(salts) == 1): return salts[0]
    else: return salts
    
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


            

       





    
    

