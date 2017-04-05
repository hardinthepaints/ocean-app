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

#Index - uncomment to make active endpoint
@app.route('/oceanapp/v1.0/app/static/<path:path>', methods=['GET'])
@auto.doc(groups=['private', 'public'])
def index(path): 
    directory = 'app/static/'
    return send_from_directory( directory, path)

#
#@app.route('/app/static/<path:path>')
#@auto.doc(groups=['public'])
#def send_static(path):
#    """Serve static files"""
#    directory = 'app/static/'
#    return send_from_directory( directory, path)

#Get data from the sql db.
@cross_origin()
@auto.doc(groups=['private', 'public'])
@app.route('/oceanapp/v1.0/jsonsql', methods=['GET'])
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
    
    return Response( outputJson, status=status,  content_type='application/json')
  
#Get data from .nc files
@cross_origin()
@auto.doc(groups=['private', 'public'])
@app.route('/oceanapp/v1.0/json/<date>', methods=['GET'])
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
            

       





    
    

