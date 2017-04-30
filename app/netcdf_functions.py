#!/usr/bin/env python

import netCDF4 as nc
import numpy as np

def getDataByHour(date, hour):
    """Get the top layer of salinity data for the given date and hour"""
    fileName = "app/ncFiles/{}/ocean_his_{}.nc".format( date, hour )
    return getData(1, 0, fileName)

def getData(end, start, fileName):
    """Get the given range of layers of salinity from the given .nc file. If the range only includes one layer, return None"""
    ds = nc.Dataset( fileName )
    
    output = {}
    
    #throw an exception if end and start are not right
    #its ok to throw exceptions here because the server will not access this code at runtime
    if not end > start: raise ValueError("parameter 'end' must be greater than start.")
        
    for variable in ["salt", "temp"]:
         
        data = {}
    
        for i in range( start, end ):
            layer = ds.variables[variable][0, i, :, :].squeeze()
            layer = layer.tolist()
            
            layer = trimPerimeter(layer)
            #layer = layer[1:-1]
            #for j in range(len(layer)):
            #    layer[j] = layer[j][1:-1]
    
            data[i] = layer
            
        if ( len(data) == 0 ):
            pass
        elif ( len(data) == 1):
            output[variable]=data[start]
        else:
            output[variable]=data
        
    ds.close()
    
    return output
    
    

    
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
    """remove a 'border' of data from a 2d array"""
    out = arr[1:-1]
    for i in range(len(out) ):
        out[i] = out[i][1:-1]
                
        
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