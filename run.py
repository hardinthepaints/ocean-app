#!/usr/bin/env python

import sys
import webbrowser

from app import app

basePath = "app/static/webapp/plotly/{}"

extra_files = [basePath.format("plotly_test.html"), basePath.format("myajax.js"), basePath.format("myheatmap.js") ]

#open the main page in a web browser
if __name__ == '__main__':
    webbrowser.open("http://localhost:5000/oceanapp/v1.0/app/static/react-ocean-app/build/index.html")

#run in debug mode if in args
if ( "-d" in sys.argv ):
    app.run( debug=True, extra_files=[], threaded=True )
else:
    app.run( debug=False, threaded=True )
    





