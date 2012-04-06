# -*- coding: utf-8 -*-

__author__ = "mRt (martincerdeira@gmail.com)"
__version__ = "0.01"
__date__ = "$Date: 4/2/2012$"
__license__ = "GPL v3"

import sys, os, pickle
from bottle import run, route, error, request, response, get, post, request, debug, static_file, url

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
    return static_file('index.html', root = './static/')

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

def start_server(srvport):
    debug(True)
    print '======================================================='
    print 'Cloud.Obj Server Launched on http://localhost:' + srvport
    print '======================================================='
    run(host='localhost', port=srvport)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Must specify port!")
    else:
        start_server(sys.argv[1])