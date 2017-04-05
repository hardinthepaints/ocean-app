#!/usr/bin/env python

"""Functions to handle user auth."""

from flask import jsonify
import warnings


# disable autodoc internal Warning
# https://github.com/acoomans/flask-autodoc/issues/27
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter('ignore', ExtDeprecationWarning)

from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password( username ):
    """Check if the given username and password are correct."""
    if username == 'xman':
        return "el33tnoob"
    return None

@auth.error_handler
def unauthorized():
    """Inform user they are not authorized using json. Use 403 instead of 401 to circumvent browser password popup"""
    return jsonify({'error':'Unauthorized access. You must provide a correct username and password.'}), 403
