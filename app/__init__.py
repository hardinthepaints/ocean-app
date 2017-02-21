#!/usr/bin/env python

from flask import Flask

#creates the application object of class 'Flask'
app = Flask(__name__)

#imports 'views' --at end of file to avoid circular refs
from app import views


