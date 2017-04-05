
"""Functions to handle creation, population, and access of sqlite database."""

from flask import g
import os
import sys
from app import app, views
from sqlite3 import dbapi2 as sqlite3
import netCDF4 as nc
import json


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'app.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_all_entries():
    db = get_db()
    cur = db.execute('select date from entries order by date desc')
    return cur.fetchall()

def populate_db():
    """Populate the db with data from the 'ncfiles' folder"""
    db = get_db()
    ncFilesDir = "./app/ncFiles/"
    for root, dirs, files in os.walk(ncFilesDir, topdown=False):
        for name in dirs:
            yearString = name
            yearPath = ncFilesDir + name
            for root, dirs, files in os.walk( yearPath ):
                for name in files:
                    
                    #print( ncFilesDir + name )

                    salt = views.getData(1, 0, yearPath + "/" + name )
                    
                    if ( salt != None ):
                        date = yearString + name [ -5:-3 ]
                        saltJSON = json.dumps(salt)
                        db.execute("insert into entries (date, z) values (?, ?)", [date, saltJSON] )
                        print(date)
    db.commit()
    count = db.execute("select count(*) from entries")
    print( "inserted {} into entries".format(count))




@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')
    populate_db()
    
@app.cli.command('printrowcount')
def printrowcount_command():
    """Print the database."""
    entries = get_all_entries()
    print( "entry count: \n" + str( len(entries)) )
    
@app.cli.command('printdb')
def printdb_command():
    """Print the database."""
    entries = get_all_entries()
    print( "entries: \n" + str( entries) )


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
