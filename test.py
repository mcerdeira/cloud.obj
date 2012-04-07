# A simple, example

from src.client import cloud

#url = "http://cloudobj.appspot.com/"
url = "http://localhost:8080/"

lib = "sys"

o = cloud.Obj(url + lib) # Now o is the module sys, from remote

print "The object is", o

print "The path is ", o.path