<h1 align="center">Ocean App Server (under development)<h1/>


<p align="center">
    <img src ="app/static/command_line_demo.gif?" />
</p>

<p align="center">
    <img src ="app/static/slider_demo2.gif?" />
</p>

## Synopsis

A Flask RESTful API to expose oceanography data format.

## Installation

1. Download .zip of repository
2. Install requirements: `pip install -r requirements.txt`
3. On OS X, Linux and Cygwin you mush indicate 'run.py' is an executable file: `chmod a+x run.py`
4. Download the .nc files (could take a couple hours) and populate database with `python3 setup_data.py`
    Note: The downloader can be stopped early with `ctr-c` and will resume automatically on next run.

## Usage

1. Start the flask server: `python3 run.py` in the root directory. `python3 run.py -d` to run in debug mode.
2. To run from command line in debug mode:

    `$ export FLASK_APP=run.py`  
    `$ export FLASK_DEBUG=1`  
    `$ flask run`  
3. Open [app/static/Webapp/plotly/plotly_test.html](app/static/Webapp/plotly/plotly_test.html) in a browser. Or, go to [http://localhost:5000/app/static/webapp/plotly/plotly_test.html](http://localhost:5000/app/static/webapp/plotly/plotly_test.html )
4. According to [Plotly benchmarks](https://plot.ly/benchmarks/ "this"), Chrome is the fastest browser for rendering heatmaps.


## Task List
- [x] Create RESTful API reference
- [x] Unit Tests
- [x] Fix tests/python_test.py
- [ ] Add streaming capability
- [ ] Send time-based range of frames
- [x] Require username + password
- [x] Compression with gzip
- [x] Compression by altering json float precision
- [x] SQLite database
 
## License

MIT
