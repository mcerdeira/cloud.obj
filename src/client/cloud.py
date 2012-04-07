# -*- coding: utf-8 -*-

__author__ = 'mRt (martincerdeira@gmail.com)'
__version__ = '0.01'
__date__ = '$Date: 4/2/2012$'
__license__ = 'GPL v3'

import urllib
import urllib2
import pickle
from urlparse import urlparse

class Obj:
    def __init__(self, url):
        self.url = url
        self.lib = urlparse(url).path.replace('/', '')
        self.lib__str__ = ''
        self._getlib()

    def _getlib(self):
        response = urllib2.urlopen(self.url).read()
        if response:
            raise ImportError, response
        else:
            self.lib__str__ = pickle.loads(urllib2.urlopen(self.url+'/__str__').read())

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        return self.lib__str__

    def __getattr__(self, attr):
        if attr:
            tmpurl = self.url+"/"+attr
            response = urllib2.urlopen(tmpurl).read()
            f = pickle.loads(response)
            return f
        else:
            raise AttributeError
