<h1 align="center">Ocean App Server (under development)<h1/>

## Synopsis

A RESTful Flask API which uses redis to expose oceanography data with a visualizer. The visualizer was build using create-react-app and the react-three-renderer.

## Installation

1. Install repository and submodule: `git clone --recursive https://github.com/hardinthepaints/ocean-app-server`
2. Install requirements: `pip install -r requirements.txt`
3. Install redis: `brew install redis`
4. In app/db, run `redis-server redisdb.conf` to start the redis server.
5. To run the flask development server: `python3 run.py`

## Usage

0. If the redis server is not running, in app/db, run `redis-server redisdb.conf` to start the redis server.
1. Start the flask server: `python3 run.py` in the root directory. `python3 run.py -d` to run in debug mode.
2. To run from command line in debug mode:
    `$ export FLASK_APP=run.py`  
    `$ export FLASK_DEBUG=1`  
    `$ flask run`  
3. Go to [http://localhost:5000/oceanapp/v1.0/app/static/react-ocean-app/build/index.html](http://localhost:5000/oceanapp/v1.0/app/static/react-ocean-app/build/index.html) to view the visualizer.
4. For documentation of API endpoints, go to [http://localhost:5000/oceanapp/v1.0/doc/](http://localhost:5000/oceanapp/v1.0/doc/).

## Tests

1. Make sure the redis db is running.
2. in /test_app, run `python3 -m unittest discover` to run all the tests.

## Development notes

The scripts `app/db/setup_data.py`, `app/db/db_functions` and `app/forcastdownloader.py` are for downloading the data in netCDF4 format and culling out relevant data to be compressed and stored in the database. As it is now, the redis db contains 72 hours' worth of temp and salinity data. To download the data, run `python3 setup_data.py`.

## Task List
- [x] Create RESTful API reference
- [x] Unit Tests
- [x] Fix tests/python_test.py
- [ ] Add streaming capability
- [x] Send time-based range of frames
- [x] Require username + password
- [x] Compression with gzip
- [x] Compression by altering json float precision
- [x] Database



## License

MIT
