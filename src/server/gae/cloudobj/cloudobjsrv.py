# -*- coding: utf-8 -*-

__author__ = "mRt (martincerdeira@gmail.com)"
__version__ = "0.01"
__date__ = "$Date: 4/2/2012$"
__license__ = "GPL v3"

import sys, os, pickle
import bottle
from bottle import run, route, error, request, response, get, post, request, debug, static_file
from google.appengine.ext.webapp.util import run_wsgi_app

def _import(lib, action):
    """
    Hack to return imported module
    """
    buf =  "def f():\n"
    buf += "    import " + lib + "\n"
    buf += "    return " + lib + "." + action + "\n"
    try:
        exec(buf)
        return f()
    except ImportError, e:
        return str(e)

def _tryimport(lib):
    buf = "import " + lib
    try:
        exec(buf)
        return ""
    except ImportError, e:
        return str(e)

@route('/')
def default():
    return static_file('index.html', root = '/static/')

@route('/static/<filename>')
def static(filename):
    return static_file(filename, root = '/static/')

@route('/<lib>')
def import_lib(lib):
    return _tryimport(lib)

@route('/<lib>/<action>')
def use_lib(lib, action):
    obj = _import(lib, action)
    return pickle.dumps(obj)

@error(404)
def error_hdl(error):
    return "<b>Ups, this is bad...</b>"

def main():
    debug(True)
    run_wsgi_app(bottle.default_app())

if __name__ == '__main__':
    main()