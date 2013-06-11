#To find hello_ext module we need to add workspace to PYTHON_PATH
#To find libJoshiLibrary.so we need to add it's location to LD_LIBRARY_PATH
#Both of these are done in setting up run configurations.
#See TestBoostPython config for details, just make sure to include LD_LIBRARY_PATH in Environment Variables

#Option 2 for python path - not using eclipse
import sys, os
path = "/home/phcostello/Documents/workspace/TestBoostPython/Debug/"
#sys.path.append(path)
from ctypes import CDLL
CDLL('libc.so.6')

zip(os.environ.keys(),os.environ.values())


#Option 2 for LD_LIBRARY_PATH
#Problem that python doesn't find shared library object not on default path
#THIS IS DIFFERENT FROM PYTHON PATH, so above doesn't fix prob
# do this in bash 'export LD_LIBRARY_PATH=' + path
#Now run Python and should find

#Option 3 for running interactive console: Can't seem to get interactive to launch
#with the same settings as a run configuration, so... 
#The defaults library paths are in /etc/ld.so.conf, can add path there and then
# sudo ldconfig. Makes it global which kinda sucks. Alternatively, can put libXX.so in one of
# the default dirs, e.g /usr/lib or /usr/local/lib
#os.environ['LD_LIBARY_PATH'] = "${workspace_loc}/JoshiLibrary/Debug"
os.environ['LD_LIBARY_PATH'] = "${workspace_loc}/TestBoostPython/Debug"


Spot = 50.0
Strike = 60.0   
r=0.0
d=0.0
Vol =0.2
Expiry = 1.0

#This requires that we compile the "SimpleTestExampleBoostPython.cpp" file into the BoostPythonTest.so file
#also that we have it linked correctly in run configurations (LD_LIBRARY_PATH). I did this by copying into working dir

import BoostPythonTest
from BoostPythonTest import *

print greet()
print BoostPythonTest.BlackScholesCall( Spot, Strike, r, d, Vol, Expiry)
