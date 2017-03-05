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
       
    layers = int( request.args.get('layers', 1) )
    output = getData( layers )
    
    callback = request.args.get('callback')
       
    return Response( callback + "(" + json.dumps(output) + ")", mimetype='application/json')

#glean the unique values in order from many repeating values
def gleanUniqueValues( arr ):
    dic = {}
    out = []
    for v in arr:
        if v in dic:
            pass
        else:
            dic[v] = True
            out.append( v )
    return out

#flatten a 2 dimensional numpy array
def flatten( numpy ):
    return numpy.reshape( -1 )

def getMin( target ):
    return min( val for val in target)

def getMax( target ):
    return max( val for val in target)

#given two arrays of values representing x and y values for a graph,
#determine the ration of the x axis to the y axis
def getRatio( xvals, yvals ):
    xlength = getMax(xvals) - getMin(xvals)
    ylength = getMax(yvals) - getMin(yvals)
    return float(xlength) / float(ylength)
 

    

#open a .nc file and collect data
#Return the specified number of layers
def getData( layers = 1 ):
    ds = nc.Dataset( dataFN )
    
    #ensure the layers correspond to correct indexes
    layers = min( layers, len( ds.variables['salt'][0]) )
    layers = max( layers, 1 )
    
    salts = []
    for i in range( layers ):
        salt = ds.variables['salt'][0, i, :, :].squeeze()
        salt = salt.tolist()
        salts.append(salt)
    
    salt = ds.variables['salt'][0, 0, :, :].squeeze()
    
    #longitude - east and west
    lonp = ds.variables['lon_psi'][:]
    lonp = flatten( lonp )
    
    #latitude - north or south
    latp = ds.variables['lat_psi'][:]
    latp = flatten(latp)
    
    output = {}
    output['salts'] = salts
    output['salt'] = salt.tolist()
    output[ 'latp' ] = gleanUniqueValues( latp.tolist() )
    output[ 'lonp' ] = gleanUniqueValues( lonp.tolist() )
    output['ratio'] = getRatio( lonp, latp )

    
    return output
    




    
    

