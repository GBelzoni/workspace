'''
Created on May 2, 2013

@author: phcostello
'''

import pandas as pd
from pandas.io.data import DataReader
from datetime import datetime

import sqlite3 
import pandas.io.sql as psql
import csv

import timeit
from django.utils.encoding import force_unicode


pd.set_printoptions(max_colwidth = 400)

path = "/home/phcostello/Documents/Data/iHub/S3_RawData/"
dbfile = "CrowdSourcingData.sqlite"


   
def readDB(table, startDate, endDate, DateField):  

    #Read parts of table
    con = sqlite3.connect(path+ dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
    
    
    
    sqlText = "select rowid, * from {0} where"\
    "(date({1}) > date('{2}') and "\
    "date({1}) < date('{3}') )".format(table,DateField,startDate,endDate)
    print sqlText
    
    data = psql.read_frame(sqlText, con )
    #print data['twitter.created_at']#, 'number of tweets = ', len(data)
    #cur = con.cursor()
    #cur.execute("PRAGMA table_info(Usernames)")
    #r = cur.fetchone()
    #print cur.description
    
    con.close()
    return data

def to_weka(data,outfile):
    
    data.to_csv(path + outfile,index=False, quoting=csv.QUOTE_NONNUMERIC)

#if __name__ == '__main__':
    #pass
    
outfile = 'SampleDb.csv'
table = "MasterData"
startDate = "2013-03-03"
endDate = "2013-03-05"
DateField = '[twitter.created_at]'

data = readDB(table, startDate, endDate, DateField)
print len(data)  
#data.sort(columns='twitter.created_at', inplace = True, ascending=True)#False)
#data.drop_duplicates(cols = 'twitter.id', take_last= True, inplace=True)
len(data)

data['twitter.user.description'].irow(range(68,73))

#Need to find what weka not a number is
data.replace(None,0,inplace=True)
data.replace('NaN',0,inplace=True)

type(data.ix[10,'interaction.geo.latitude'])

data.icol(2).head()
data[['twitter.text','twitter.created_at']].head()
con = sqlite3.connect(path+ dbfile)#, detect_types=sqlite3.PARSE_DECLTYPES)
psql.write_frame(data, name="testFromPd", con=con,append=False)
con.commit()
con.close()


import random
sampleRows = [random.randrange(start=0, stop=len(data))  for i in range(0,1000)]
sampledData = data.irow(sampleRows)
sampledData[['rowid','twitter.text']].head(10)
sampledData[['rowid','twitter.text']].to_csv(path + 'dataToAnnotate.csv',index=False)

annotated = pd.read_csv(path + 'dataToAnnotate.csv')
annotated.columns

dfout = pd.merge(data,annotated,  on='rowid')       
len(dfout)
to_weka(dfout, outfile)


#print sqlText
