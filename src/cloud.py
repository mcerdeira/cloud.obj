# -*- coding: utf-8 -*-

__author__ = "mRt (martincerdeira@gmail.com)"
__version__ = "0.01"
__date__ = "$Date: 4/2/2012$"
__license__ = "GPL v3"

import urllib
import urllib2
import pickle
from urlparse import urlparse

class Obj:
    def __init__(self, url):
        self.url = url
        self.lib = urlparse(url).path.replace("/", "")
        self._getlib()

    def _getlib(self):
        response = urllib2.urlopen(self.url).read()
        if response:
            raise ImportError, response

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __getattr__(self, attr):
        if True:
            tmpurl = self.url+"/"+attr
            response = urllib2.urlopen(tmpurl).read()
            f = pickle.loads(response)     
            return f
        else:
            raise AttributeError
