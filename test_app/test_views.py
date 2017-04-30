import os, sys
import gzip
import time
import json
import test_db_functions

"""Test suite to test the endpoints in app/views.py"""

#allow to import packages in parent directory
sys.path.append('../')

from app import app, views

import unittest
import tempfile
import json
import flask
from base64 import b64encode

#static helper functions 
def loadJSON( data ):
    """Load bytes of data into an object if it is json"""
    string = decodeUTF8( data )
    if ( string != None ):
        return json.loads( string )
    else:
        return None
    
    
def decodeUTF8( string ):
    """Decode bytes of data if it is 'utf-8'"""
    try:
        decoded = string.decode('utf-8')
        return decoded
    except UnicodeError:
        return None

def errorsStringsEqual(a,b):
    a = int(a[0:3])
    b = int(b[0:3])
    return a == b

def getAuthHeaders():
    #encode the username and password
    usrpass = b64encode(("{0}:{1}".format("xman", "el33tnoob")).encode('utf-8')).decode('ascii')

    headers = {
        'Authorization': 'Basic ' + usrpass
    }
    return headers
    
    
ERROR_KEY = "error"
NOT_FOUND = "404 NOT FOUND"
OK = "200 OK"
ENTRY_POINT = "/oceanapp/v1.0"

class FlaskrTestCase(unittest.TestCase):
    
    def setUp(self):
        """setup client testing"""
        self.app = app.test_client()
        app.config["DEBUG"] = True
        #self.context = flask.Flask(__name__)        

    def tearDown(self):
        """End client testing"""
        #os.close(self.db_fd)
        #os.unlink(app.config['DATABASE'])
        pass
    
    #REAL ENDPOINTS
    def test_index(self):
        """test the index endpoint"""
        for endpoint in ['/index/']:
            rv = self.makeGet(endpoint)
            jsonObj = loadJSON( rv.data )
            assert jsonObj != None
            
    def test_public_doc(self):
        rv = self.makeGet("/doc/public")
        self.assertOK( rv )
        
    def test_private_doc(self):
        rv = self.makeGet("/doc/private")
        self.assertOK( rv )
        
    
    def test_json(self):
        endpoint = ENTRY_POINT + '/json'
        
        headers = getAuthHeaders()
          
        rv = self.app.get( endpoint, headers=headers)
        
        #decompress the data
        assert "gzip" == rv.headers['Content-Encoding']
        
        start = time.time()
        rv.data = gzip.decompress( rv.data )
        #print("unzip time: {}".format( time.time()-start ))

        #check authorized
        self.assertOK(rv)
        
        #parse json  
        result = loadJSON( rv.data )

        
        assert len(result)%72 == 0, "Expected length to be a multiple of 72 but got {}".format(str(len(result)))
        
        test_db_functions.assertFields(result)
        

    #NONEXISTENT ENDPOINTS
    def test_notfound(self):
        self.assertNotFound("/nonendpoint")
        
    
    def test_json_notfound(self):
        self.assertNotFound('/json/20170aa')
        
    #HELPERS 
    def makeGet(self, endpoint):
        """make a get request and ensure the return type is correct"""
        """We always want GET requests to return json from this server, even on 404s except for the doc"""
        
        endpoint = ENTRY_POINT + endpoint
        rv = self.app.get(  endpoint)
        
        contentType = rv.headers['Content-Type']
        assertionError = "wrong content type: '{}', endpoint: '{}'"
        
        #if not documentation, should be in json format
        if ("/oceanapp/v1.0/doc" in endpoint):
            assert 'text/html' in contentType, assertionError.format(contentType, endpoint)
        else:
            assert contentType == 'application/json', assertionError.format(contentType, endpoint)
  
        return rv
    
    def assertOK(self, rv):
        assert rv.status == OK, "Expected {} but got {}".format( OK, rv.status )
    
    def assertNotFound(self, endpoint):
        """Test that an enpoint which does not exist returns a 404 and in json"""
        rv = self.makeGet(endpoint)
        
        #check status
        assert( rv.status == NOT_FOUND )
        
        #check json
        jsonObj = loadJSON( rv.data )
        assert jsonObj != None
        assert ERROR_KEY in jsonObj
        assert "404" in jsonObj[ERROR_KEY]

class ViewsTest(unittest.TestCase):
    """test the functions in views.py which do not require a context"""
    
    def setUp(self):
        """setup client testing"""
        self.app = app
        #app.config["DEBUG"] = True
        #self.context = flask.Flask(__name__)        

    def tearDown(self):
        """End client testing"""
        #os.close(self.db_fd)
        #os.unlink(app.config['DATABASE'])
        pass
    
    
if __name__ == '__main__':
    unittest.main()
   
