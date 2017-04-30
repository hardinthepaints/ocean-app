#!/usr/bin/env python
import time
import sys
import os
sys.path.append('../../')


"""Downloads .nc files and stores data in a sql db for this app when you have no data."""

from app import app, forcastdownloader
from app.db import db_functions
from flask import Flask, current_app

start = time.time()


#download .nc files if necessary
forcastdownloader.downloadYesterday()
downloadTime = time.time() - start
start = time.time()

#app = Flask(__name__)

with app.app_context():
    db_functions.init_db()
    db_functions.populate_db()

initdbTime = time.time() - start

print("downloadTime:{}s, initdbTime:{}s, total:{}s,".format(downloadTime, initdbTime, sum([downloadTime, initdbTime])))

