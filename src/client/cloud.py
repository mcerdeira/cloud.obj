# -*- coding: utf-8 -*-

#===============================================================================
# DOC
#===============================================================================

"""Client for:

    =================================
    CLOUD.OBJ
         One object to rule them all
    =================================

"""

#===============================================================================
# META
#===============================================================================

__author__ = 'mRt (martincerdeira@gmail.com)'
__version__ = '0.01'
__date__ = '$Date: 4/2/2012$'
__license__ = 'GPL v3'


#===============================================================================
# IMPORTS
#===============================================================================

import collections
import abc
import urllib
import urllib2
import pickle
import hashlib
import time
from urlparse import urlparse

try:
    import memcache
except ImportError:
    memcache = None


#===============================================================================
# ABSTRACT CACHE
#===============================================================================

class AbstractCache(object):
    """Base classes for create caches in infopython"""
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, ttl=60):
        """Creates a new instance
        
        params
            ``ttl``
                Time to live of the data.
        """
        self._ttl = ttl
    
    def __getitem__(self, k):
        return self.retrieve_data(k)
        
    def __setitem__(self, k, v):
        self.store_data(k, self.ttl, v)
    
    def get(self, k, d=None):
        """C.get(k[,d]) -> C.pull(k) if k in C and can be retrieved, else d.  
        d defaults to None.

        """
        try:
            return self[k]
        except Exception:
            return d

    @property
    def ttl(self):
        return self._ttl

    @ttl.setter
    def ttl(self, ttl):
        self._ttl = ttl
    
    #===========================================================================
    # ABSTRACTS METHODS
    #===========================================================================
       
    @abc.abstractmethod
    def store_data(self, k, ttl, v):
        """Set the data and the ttl in to cache.

        """
        raise NotImplementedError()
            
    @abc.abstractmethod
    def retrieve_data(self, k):
        """Retrieve a data from a cache.
        
        """
        raise NotImplementedError()
        
    @abc.abstractmethod
    def clear_expired(self):
        """Deletes all expired data from the cache
        
        """
        raise NotImplementedError()
        
    @abc.abstractmethod
    def clear(self):
        """Removes all data from cache
        
        """
        raise NotImplementedError()


#===============================================================================
# DICT CACHE
#===============================================================================

class DictCache(AbstractCache):
    """Implementation of a cache in a memory dictionary

    """
    def __init__(self, ttl=60):
        """Creates a new instance

        params:

            ``ttl``
                Time to live of the data.

        """
        super(DictCache, self).__init__(ttl=ttl)
        try:
            self._ich = collections.OrderedDict()
            self._ttds = collections.OrderedDict()
        except AttributeError:
            #This version of python does not support OrderedDict
            from ordereddict import OrderedDict
            self._ich = OrderedDict()
            self._ttds = OrderedDict()

    def store_data(self, k, ttl, v):
        self._ich[k] = v
        self._ttds[k] = (
            time.time() + ttl if ttl != None else None
        )

    def retrieve_data(self, k):
        ttd = self._ttds.get(k, 0)
        if ttd == None or time.time() < ttd:
            return self._ich[k]
        elif ttd:
            self._ttds.pop(k)
            self._ich.pop(k)

    def clear_expired(self):
        for k, ttd in self._ttds.items():
            if ttd != None and ttd < time.time():
                self._ttds.pop(k)
                self._ich.pop(k)
            else:
                break

    def clear(self):
        self._ich.clear()
        self._ttds.clear()


#===============================================================================
# MEMCACHED CACHE
#===============================================================================

if memcache:

    class MemcachedCache(AbstractCache):
        """Implementation of a memcache for infopython

        """
        def __init__(self, hosts, debug=0, ttl=60):
            """Creates a new instance

            params:

                ``hosts``
                    A list of *hosts:port* of memcache daemons.

                ``debug``
                    Debug levels of memcache.

                ``ttl``
                    Time to live of the data.

            """
            super(MemcachedCache, self).__init__(ttl=ttl)
            self._mc = memcache.Client(hosts, debug=debug)
            self._prefix = hashlib.sha1(
                str(time.time()) + str(id(self))
            ).hexdigest() + "_"

        def ping(self):
            """Return *True* if any server is response

            """
            try:
                return bool(self._mc.get_stats())
            except:
                return False

        def store_data(self, k, ttl, v):
            if self.ping():
                key = self._prefix + k
                value = pickle.dumps(v)
                ttl = ttl if ttl != None else 0
                self._mc.set(key, value, time=ttl)

        def retrieve_data(self, k):
            if self.ping():
                key = self._prefix + k
                value = self._mc.get(key)
                if value:
                    return pickle.loads(value)
            return None

        def clear_expired(self):
            pass

        def clear(self):
            if self.ping():
                self._mc.flush_all()


#===============================================================================
# OBJ
#===============================================================================

class Obj(object):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        global _cache
        key = kwargs.get("url") or (args[0] if args else None)
        instance = _cache[key]
        if not instance:
            instance = super(Obj, cls).__new__(cls) # , *args, **kwargs) This throws a deprecation warning
            _cache[key] = instance
        return instance

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
            global _cache
            tmpurl = self.url + "/" + attr
            f = _cache[tmpurl]
            if not f:
                response = urllib2.urlopen(tmpurl).read()
                f = pickle.loads(response)
                _cache[tmpurl] = f
            return f
        else:
            raise AttributeError

#===============================================================================
# CACHE CONF
#===============================================================================

_cache = DictCache(60) 


def get_cache():
    return _cache

    
def set_cache(engine):
    if not isinstance(engine, AbstractCache):
        msg = "'engine' must be an instance of a subclass of AbstractCache"
        raise TypeError(msg)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
