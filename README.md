<h1 align="center">Ocean App (under development)<h1/>

<p align="center">
    <img src ="app/static/slider_demo2.gif?" />
</p>

## Synopsis

This is a project to create a client-side web app which displays oceanography data in time-lapse form. 

## Installation

1. Download .zip of repository
2. Install requirements: `pip install -r requirements.txt`
3. On OS X, Linux and Cygwin you mush indicate 'run.py' is an executable file: `chmod a+x run.py`
4. Download the .nc files (could take a couple hours): `cd app` `python3 forcastdownloader`

## Usage

1. Start the flask server: `python3 run.py` in the root directory. `python3 run.py -d` to run in debug mode.
2. To run from command line in debug mode:

    `$ export FLASK_APP=run.py`  
    `$ export FLASK_DEBUG=1`  
    `$ flask run`  
3. Open app/static/webapp/plotly/plotly_test.html in a browser. Or, go to [http://localhost:5000/app/static/webapp/plotly/plotly_test.html]("http://localhost:5000/app/static/webapp/plotly/plotly_test.html")
4. According to [Plotly benchmarks](https://plot.ly/benchmarks/ "this"), Chrome is the fastest browser for rendering heatmaps.

## License

MIT
