# A simple, example

import cloud

o = cloud.Obj("http://localhost:5555/sys") # Now o is the module sys, from remote

print "The path is ", o.path