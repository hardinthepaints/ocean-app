import os, sys
import gzip
import time
import json
import unittest


"""Test suite to test the endpoints in app/views.py"""

#allow to import packages in parent directory
sys.path.append('../')

from app import app, db_functions


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
            assert len(entries) == 2, "Unexpected number of entries"
            
    def test_get_all_entries(self):
        with app.app_context():
            
            entries = db_functions.get_all_entries()
            
            assert len(entries[b"framesCompressed"]) < len(entries[b"frames"])
            
            
    
if __name__ == '__main__':
    unittest.main()
   
