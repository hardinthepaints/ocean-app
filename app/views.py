#!/usr/bin/env python

import netCDF4 as nc
from app import app
from flask import send_from_directory
from flask import Response
from flask import request
import os
import json


'''
Views are handlers that respond to request from clients. Each methode with an '@' statement is a view.
'''

dataFN = 'app/static/ocean_his_0002.nc'

#serve the data in json
@app.route('/')
@app.route('/index')
def index():
    
    output = getData()
       
    return Response(json.dumps(output), mimetype='application/json')

#serve data in jsonp with provided callback
@app.route('/jsonp')
def jsonp():
       
    output = getData()
    
    callback = request.args.get('callback')
       
    return Response( callback + "(" + json.dumps(output) + ")", mimetype='application/json')
    

#convert a 2 dimensional numpy array to a python array
#empties are converted to null
def numpyToArray( numpy ):
    rows = len( numpy[0] )
    columns =  len( numpy )
    numpy = numpy.reshape( columns, rows )
    
    return numpy.tolist()

#open a .nc file and collect data
def getData():
    ds = nc.Dataset( dataFN )
    
    
    salts = []
    for i in range( len( ds.variables['salt'][0])):
        salt = ds.variables['salt'][0, i, :, :].squeeze()
        salt = numpyToArray(salt)
        salts.append(salt)
    
    salt = ds.variables['salt'][0, 0, :, :].squeeze()
    lonp = ds.variables['lon_psi'][:]
    latp = ds.variables['lat_psi'][:]
    
    output = {}
    output['salts'] = salts
    output['salt'] = numpyToArray(salt)
    output['lonp'] = numpyToArray(lonp)
    output['latp'] = numpyToArray(latp)
    
    return output
    




    
    

