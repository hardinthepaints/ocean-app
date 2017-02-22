#!/usr/bin/env python

import netCDF4 as nc
from app import app
from flask import send_from_directory
import os
from flask import Response
import json


'''
Views are handlers that respond to request from clients. In Flask,
handlers are written as python functions
'''



dataFN = 'app/static/ocean_his_0002.nc'

#Open a .nc dataset and serve the data
@app.route('/')
@app.route('/index')
def index():
    ds = nc.Dataset( dataFN )
    salt = ds.variables['salt'][0, 0, :, :].squeeze()
    lonp = ds.variables['lon_psi'][:]
    latp = ds.variables['lat_psi'][:]
    
    output = {}
    output['salt'] = numpyToArray(salt)
    output['lonp'] = numpyToArray(lonp)
    output['latp'] = numpyToArray(latp)
    
    return Response(json.dumps(output), mimetype='application/json')

#convert a 2 dimensional numpy array to a python array
#empties are converted to null
def numpyToArray( numpy ):
    rows = len( numpy[0] )
    columns =  len( numpy )
    numpy = numpy.reshape(columns, rows)
    
    return numpy.tolist()




    
    

