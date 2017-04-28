#!/usr/bin/env python
import os
import sys
from flask import Flask, g

#allow cross origin requests
from flask_cors import CORS, cross_origin


def getParentDirectory():
    """Get the parent directory of this file. This makes it so the app will work, (and the db will be found)
    no matter the current working directory."""
    path = os.path.dirname(os.path.realpath(__file__))
    path = '/'.join( path.split('/')[:-1] )
    return path

#creates the application object of class 'Flask'
#according to documentation it is necesary to define the root path
app = Flask(__name__, root_path = getParentDirectory() )


#activate cross origin requests
cors = CORS( app )

#imports 'views' --at end of file to avoid circular refs
from app import views


