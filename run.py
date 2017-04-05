#!/usr/bin/env python

import sys

from app import app

#run in debug mode if in args
if ( "-d" in sys.argv ):
    app.run( debug=True )
else:
    app.run( debug=False )




