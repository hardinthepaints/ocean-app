import os, sys
import gzip
import time
import json
import unittest
import gzip
from flask_redis import FlaskRedis
import test_views

"""Test suite to test the endpoints in app/views.py"""

#allow to import packages in parent directory
sys.path.append('../')

from app import app
from app.db import db_functions


class DatabaseTestCase(unittest.TestCase):
    
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
    
    def test_get_keys(self):
        with app.app_context():
            
            entries = db_functions.get_keys()
            for entry in entries:
                entry = entry.decode('utf-8')
                expectedEntries = ["frames", "framesCompressed"]
                assert entry in expectedEntries, "entries {} not in {}".format(entry, expectedEntries)
                
            expected = 1
            assert len(entries) == expected, "Unexpected number of entries. Expected {} but got {}".format(expected, len(entries))
            
    def test_get_all_entries(self):
        with app.app_context():
            
            
            entries = db_functions.get_all_entries()
            frames = entries[b"framesCompressed"]
            assert len(frames) > 0
            
            frames = test_views.loadJSON( gzip.decompress(frames) )
            
            assert type(frames) == type([]), "unexpected type {}".format(type(frames))
            
            assertFields(frames)
                        
    def test_db_entries(self):
        with app.app_context():
            
            keys = db_functions.get_keys()
                            
    def test_get_db(self):
        with app.app_context():
            
            db = db_functions.get_db()
            assert (db != None)
            
    def test_getNcFilesDir(self):
        parent = db_functions.getNcFilesDir()
        
        assert os.path.isdir(parent)
        

            
def assertFields(result):
             
    #assert that the result is ordered and each row has correct keys
    last = 0
    
    assert len(result) > 0, "Empty result"
    
    for row in result:
        
        for attrib in ["yyyymmddhh", 'salt', 'temp']:
            assert attrib in row, "arribute '{}' not found in row".format(attrib)
            
        
        expectedtype = type([])
        actual = type(row['salt'])
        assert actual is expectedtype, "Wrong type. expected {} but got {}.".format( expectedtype, actual )

        expectedtype = type([])
        actual = type(row['temp'])
        assert actual is expectedtype, "Wrong type. expected {} but got {}.".format( expectedtype, actual )
        
        expectedtype = type("")
        actual = type(row['yyyymmddhh'])
        assert actual is expectedtype, "Wrong type. expected {} but got {}.".format( expectedtype, actual )  

    
        curr = int(row['yyyymmddhh'] )
        assert last < curr
        last = curr
        
            
    
if __name__ == '__main__':
    unittest.main()
   
