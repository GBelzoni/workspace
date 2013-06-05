'''
Created on Feb 21, 2013

@author: phcostello
'''
import pandas as pd
from pandas.io.data import DataReader
from datetime import datetime
import sqlite3 
import pandas.io.sql as psql
import timeit
import csv
import codecs
import StringIO
pd.set_printoptions(max_colwidth = 400)

path = "/home/phcostello/Documents/Data/iHub/S3_RawData/"
infile = "ConcatenatedFiles/ConcAll.csv"
outfile = "CrowdSourcingData.sqlite"
tblName = 'MasterData'

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1  


con.close()
fin.close()

numLines = file_len(path + infile)
linesPerLoop = 30000
numLoops = numLines/linesPerLoop
numLoopsRemainder = numLines%linesPerLoop
print "numLines = ", numLines
print "linesPerLoop = ", linesPerLoop
print "numLoops = ", numLoops
print "num Remainder Loops = ", numLoopsRemainder


#Open concatenated file to transfer to sqlite db
#NOTE make sure to have encoding = 'utf-8' or there is problem trying to
#write strings to db
fin = codecs.open(path+infile, encoding='utf-8')

#Strategy is to read chunks of lines at a time, concat into string, then use
#pandas DataFrame constructor to read csv fields correctly, and parse datetime strings correctly

header = fin.readline() #First line in file is column headers, need to have as fisrt line
                        # in string that will get converted to dataframe

#open db connection with flag set to detect data types. 
con = sqlite3.connect(path+ outfile, detect_types=sqlite3.PARSE_DECLTYPES)
tic = timeit.default_timer() #timer start

for i in range(numLoops): #Change numLoops to 1 for final remainder loop
    lines = [fin.next() for x in xrange(linesPerLoop)] #change linesPerLoop to numLoopsRemainder for final loop
    lines = ''.join(lines)
    line = header + lines
    output = StringIO.StringIO(line)
    data = pd.read_csv(output,encoding='utf-8')
    output.close()

    data['twitter.created_at'] = data['twitter.created_at'].apply(pd.to_datetime)
    data['twitter.user.created_at'] = data['twitter.user.created_at'].apply(pd.to_datetime)
    
    try:
        psql.write_frame(data, tblName , con,append=True)
        con.commit()
    except Exception as e:
        print "Problems with {}".format(tblName), e

    toc = timeit.default_timer() #end timer
    print linesPerLoop*i, "lines done | ", "time = ", tic-toc

#After running this you need to run one more loop with the remainder loops
# do this by setting range(1) in outer loop, and xrange(numLoopsRemainder) in first line of loop


##Code to recode string as utf-8. Better to use encoding='utf-8' kwarg in pd.read_csv
#data = pd.read_csv(path + infile )
#TF = data.applymap( lambda(x): isinstance(x, str))
#strCols = list((TF.sum(0) !=0).index)
#
#data[strCols]
#
#colnames = list(data.columns)
#coltypes = [type(it) for it in data.irow(1)]
#dictNameType = pd.DataFrame(zip( colnames, coltypes))
#strCols = dictNameType.ix[dictNameType[1] == str,0]
#
#data[strCols] = data[strCols].applymap( lambda(x): str(x))
#data[strCols] = data[strCols].applymap( lambda(x): x.decode('unicode-escape'))
#
#ucolnames = [ x.decode('unicode-escape') for x in colnames]
#data.colnames = ucolnames
