<h1 align="center">Ocean App<h1/>

<p align="center">
    <img src ="app/static/slider_demo2.gif?" />
</p>

## Synopsis

This is a project to create a client-side web app which displays oceanography data in time-lapse form. 

## Installation

1. Download .zip of repository
2. Install requirements: `pip install -r requirements.txt`
3. On OS X, Linux and Cygwin you mush indicate 'run.py' is an executable file: `chmod a+x run.py`
4. Execute the script to start the server. `python3 run.py`
5. To run from command line in debug mode:
    `$ export FLASK_APP=run.py`
    `$ export FLASK_DEBUG=1`
    `$ flask run`
6. In your browser, open tests/javascript/javascript_test.html

## Usage

1. Start the flask server: `./run.py` or `python3 run.py` in the root directory.
2. Open tests/javascript/javascript_test.html in a browser. Or, go to http://localhost:5000/tests/plotly/javascript_test.html
3. According to [Plotly benchmarks](https://plot.ly/benchmarks/ "this"), Chrome is the fastest browser for rendering heatmaps.

## License

MIT
