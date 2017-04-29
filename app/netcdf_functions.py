#!/usr/bin/env python

import netCDF4 as nc
import numpy as np

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
        salt = salt[1:-1]
        for j in range(len(salt)):
            salt[j] = salt[j][1:-1]
        #salts[i] = salt
        
        #flatten
        #salt = sum(salt,[])

        salts[i] = salt

    
    #close the dataset
    ds.close()
    
    
    
    if ( len(salts) == 0 ): return None
    elif ( len(salts) == 1): return salts[start]
    else: return salts
    
#flatten a 2 dimensional numpy array
def flatten( numpy ):
    return numpy.reshape( -1 )

def getMin( target ):
    return min( val for val in target)

def getMax( target ):
    return max( val for val in target)

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

#given two arrays of values representing x and y values for a graph,
#determine the ratio of the x axis to the y axis
def getRatio( xvals, yvals ):
    xlength = float(getMax(xvals)) - getMin(xvals)
    ylength = float(getMax(yvals)) - getMin(yvals)
    return float(xlength) / float(ylength)

def trimPerimeter(arr):
    out = arr[0:-1]
    for i in range(len(out) ):
        out[i] = out[i][0:-1]
        
    #for pair in zip(arr, arr[1:]):
        
        
    return out

def removeNones(l):
    """remove all the none values from a 1d array"""
    return [x for x in l if x is not None]

#open a .nc file and collect data
#Return the specified number of layers
def getAxisData(fileName):
    """Returns a dict with keys 'lon', 'lat' and 'ratio'
    which correspond to an array of longitudes, array of lats, and the axis aspect ratio"""
    try:
        ds = nc.Dataset( fileName )
    except:
        return None
    
    axisData = {}
    
    lonp = ds.variables['lon_psi'][:]
    latp = ds.variables['lat_psi'][:]

    count = 0
    
    def prepareAxis(axis):
        
        axis = axis.tolist()
        axis = sum(axis,[])
        axis = gleanUniqueValues(axis)
        return axis
        
    lonp = prepareAxis(lonp)
    latp = prepareAxis(latp)

        
    axisData['lon'] = lonp
    axisData['lat'] = latp
    
    #include the ratio of lon to lat
    axisData['ratio'] = getRatio( lonp, latp )

    return axisData