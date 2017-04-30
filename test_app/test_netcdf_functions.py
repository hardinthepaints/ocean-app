import sys
import os
import unittest

sys.path.append('../')
from app import app, netcdf_functions



class NetcdfWrapperTestCase(unittest.TestCase):
    
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
    
    def test_getData(self):
        
        
        a = netcdf_functions.getData(39, 38, "ocean_his_0002.nc")

        
        #get a result where the end if before the start. Should return 
        b = netcdf_functions.getData(39, 38, "ocean_his_0002.nc")
        assert b != None
        
        c = netcdf_functions.getData(40, 39, "ocean_his_0002.nc")
        
        #assert that the function isnt just returning all the same values, but is returning values where appropriate
        assert c != None
        assert c != b
        assert a == b
        
        for result in [a, b, c]:
            assert 'salt' in result
            assert 'temp' in result
            salt = result['salt']
            temp = result['temp']            
            assert len(salt) == len(temp)
            assert len(salt[0]) == len(temp[0])
            
        
        
    
if __name__ == '__main__':
    unittest.main()
   
