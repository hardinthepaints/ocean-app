import os, sys
import gzip
import time
import json

"""Test suite to test the endpoints in app/views.py"""

#allow to import packages in parent directory
sys.path.append('../')

from app import app
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
        self.context = flask.Flask(__name__)        

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
        """Test the json enpoint by querying for existent and nonexistent frames.
        Then check result for presence of the real frames and lack of the fake ones."""
        data = {
            "hours" : [1,2,3]
        }
        date = "20170305"
        
        endpoint = ENTRY_POINT + '/json/{}'.format(date)
        rv = self.app.get(  endpoint, query_string=data)
        
        result = loadJSON( rv.data )

        
        assert '200' in rv.status, "unexpected status. expected {} but got {}".format('200', rv.status)
        
        assert 'hoursData' in result
        assert type(result) == type({}), "Unexpected json result type. Expected {} but got {}".format( type({}), type(result) )
        assert "2017030501" not in result['hoursData']
        assert "2017030502" in result['hoursData']
        assert "2017030503" in result['hoursData']
    
    def test_jsonsql(self):
        endpoint = ENTRY_POINT + '/jsonsql'
        
        headers = getAuthHeaders()
        
        sizes = {}
        results = []
        possible_params = [None, 'gzip=true', "precomp=true"]
        #test with the gzip parameter
        for query_string in possible_params:
                
            rv = self.app.get( endpoint, query_string=query_string, headers=headers)
            
            sizes[ query_string ] = int(rv.headers["Content-Length"])
            
            #decompress the data
            if query_string in possible_params[1:]:
                assert "gzip" == rv.headers['Content-Encoding']
                
                start = time.time()
                rv.data = gzip.decompress( rv.data )
                #print("unzip time: {}".format( time.time()-start ))

            #check authorized
            self.assertOK(rv)
            
            #parse json  
            result = loadJSON( rv.data )
            
            #assert that the result is ordered and each row has correct keys
            last = 0
            
            assert len(result) == 72, "Expected 72 frames but got {}".format(str(len(result)))
            for row in result:
                curr = int(row['yyyymmddhh'] )
                assert last < curr
                assert "z","yyyymmddhh" in row
                last = curr
            results.append(result)
        
        #assert the compressed endpoints have equal results and are smaller than uncompressed
        assert sizes[possible_params[0]] > sizes[possible_params[1]] == sizes[possible_params[2]]
        assert results[0] == results[1]
        assert results[1] == results[2]
        
        
    #def test_encoder(self):
    #    x = [float(1.0002442),float(7.0002442),float(4.0002442)]
    #    print(x)
    #    jsonencoder = app.json_encoder
    #    print(jsonencoder.default(jsonencoder, x))
    #    
    #    #json.dumps(x)
        
        

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
    
if __name__ == '__main__':
    unittest.main()
   
