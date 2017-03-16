#!/usr/bin/env python

import netCDF4 as nc
from app import app
from flask import send_from_directory, Response, request
import os
import json
from time import sleep
from math import sqrt

#cross origin resource sharing library
from flask_cors import CORS, cross_origin


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

@cross_origin()
@app.route('/json')
def jsonData():
       
    #the frame after the last frame in the range returned (will NOT return this one)
    end = int( request.args.get('end', 1) )
    
    #the first frame in the range to return
    start = int(request.args.get('start', 0) )
    
    #whether or not this is the first call to the server
    first = bool(request.args.get('first', False) )

    output = getData( end=end, start=start, first=first )
    
    #the jsonp callback 
    callback = request.args.get('callback')
       
    return Response(  json.dumps(output), mimetype='application/json')

@cross_origin
@app.route('/frames')
def frames():
    frame = int( request.args.get('frame', 0) )
    first = False
    if (frame == 0 ): first = True
    
    output = getData(end = frame+1, start = frame, first=first)
    return Response(  json.dumps(output), mimetype='application/json')



#serve data in jsonp with provided callback
@app.route('/jsonp')
def jsonp():
       
    #the frame after the last frame in the range returned (will NOT return this one)
    end = int( request.args.get('end', 1) )
    
    #the first frame in the range to return
    start = int(request.args.get('start', 0) )
    
    #whether or not this is the first call to the server
    first = bool(request.args.get('first', False) )

    output = getData( end=end, start=start, first=first )
    
    #the jsonp callback 
    callback = request.args.get('callback')
       
    return Response( callback + "(" + json.dumps(output) + ")", mimetype='application/json')

@app.route('/stream_sqrt')
def stream():
    def generate():
        for i in range(500):
            yield '{}\n'.format( sqrt(i) )
            sleep(.05)

    return app.response_class(generate(), mimetype='text/plain')

#serve test files
@app.route('/tests/<path:path>')
def send_test(path):
    directory = 'tests/'
    return send_from_directory( directory, path)

@app.route('/app/static/<path:path>')
def send_static(path):
    directory = 'app/static/'
    return send_from_directory( directory, path)

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
#determine the ratio of the x axis to the y axis
def getRatio( xvals, yvals ):
    xlength = getMax(xvals) - getMin(xvals)
    ylength = getMax(yvals) - getMin(yvals)
    return float(xlength) / float(ylength)  

#open a .nc file and collect data
#Return the specified number of layers
def getData( end, start, first ):
    ds = nc.Dataset( dataFN )
    
    output = {}

    #ensure the layers correspond to correct indexes
    end = min( end, len( ds.variables['salt'][0]) )
    end = max( end, 1 )
     
    #salts = [None] * end
    salts = {}
    for i in range( start, end ):
        salt = ds.variables['salt'][0, i, :, :].squeeze()
        salt = salt.tolist()
        salts[i] = salt
        
    
    salt = ds.variables['salt'][0, 0, :, :].squeeze()
    
    #if the first call by the client
    if ( first ):
        #longitude - east and west
        lonp = ds.variables['lon_psi'][:]
        lonp = flatten( lonp )
        output[ 'x' ] = gleanUniqueValues( lonp.tolist() )

        #latitude - north or south
        latp = ds.variables['lat_psi'][:]
        latp = flatten(latp)
        output[ 'y' ] = gleanUniqueValues( latp.tolist() )
        
        #include the ratio of lon to lat
        output['ratio'] = getRatio( lonp, latp )
        
        #include the number of frames available
        output['frameCount'] = len( ds.variables['salt'][0, :, :, :].squeeze() )


    
    output['frames'] = salts
    

    
    return output


    




    
    

