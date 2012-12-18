import os
print "Path at terminal when executing this file"
print os.getcwd()
print "This file path, relative to os.getcwd()"
print __file__
print "This file full path (following symlinks)"
full_path = os.path.realpath(__file__)
print full_path
print "This file directory and name"
path, file = os.path.split(full_path)
print path, '-->', file
print "This file directory only"
print os.path.dirname(full_path)