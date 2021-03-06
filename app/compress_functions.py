#!/usr/bin/env python
from flask import after_this_request, request
from io import BytesIO as IO
import gzip
import functools

"""Functions for compressing responses before they are sent off.
To use them in views.py, add the decorator @gzipped to the endpoint"""

def gzipped(f):
    """Compress the response before sending it off"""
    @functools.wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            
            return zipp(response)

        return f(*args, **kwargs)

    return view_func

def zipp(response):
    """Compress a response"""
    #accept_encoding = request.headers.get('Accept-Encoding', '')
    #if 'gzip' not in accept_encoding.lower():
        #return response

    response.direct_passthrough = False

    if (response.status_code < 200 or
        response.status_code >= 300 or
        'Content-Encoding' in response.headers):

        return response
    
    #compress the data
    response.data = compressData(response.data)
    
    #add headers
    response = addHeaders(response)
    return response

def addHeaders(response):
    """Add the headers to indicate the response is compressed"""
    #add appropriate headers
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Vary'] = 'Accept-Encoding'
    response.headers['Content-Length'] = len(response.data)
    return response

def compressData(  data ):
    
    gzip_buffer = IO()
    gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
    gzip_file.write( data )
    gzip_file.close()
    
    return gzip_buffer.getvalue()
    


