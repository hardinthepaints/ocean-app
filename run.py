#!/usr/bin/env python

import sys

from app import app

basePath = "app/static/webapp/plotly/{}"

extra_files = [basePath.format("plotly_test.html"), basePath.format("myajax.js"), basePath.format("myheatmap.js") ]

#run in debug mode if in args
if ( "-d" in sys.argv ):
    app.run( debug=True, extra_files=[] )
else:
    app.run( debug=False )




