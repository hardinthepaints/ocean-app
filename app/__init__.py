#!/usr/bin/env python
import os

from flask import Flask
from flask_cors import CORS, cross_origin


#creates the application object of class 'Flask'
#according to documentation it is necesary to define the root path
app = Flask(__name__, root_path = os.getcwd() )
cors = CORS( app )

#imports 'views' --at end of file to avoid circular refs
from app import views


