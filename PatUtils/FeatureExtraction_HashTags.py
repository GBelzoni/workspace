'''
Created on May 2, 2013

@author: phcostello
'''

import pandas as pd
import numpy as np
from pandas.io.data import DataReader
from datetime import datetime
import sqlite3 
import pandas.io.sql as psql
import csv
import timeit

pd.set_printoptions(max_colwidth = 400)

def showTables(con, display = True):

    cur = con.cursor()
    cur.execute("SELECT name, type FROM sqlite_master")
    tbls = pd.DataFrame(cur.fetchall())
    if(display):
        print tbls
    return tbls
    
   
def readDB(con, table, startDate, endDate, DateField=None, fields = None):  

    #Read parts of table
    #Default if fields = None is to read rowid, *
    if fields == None:
        fieldTxt = '*'
    else:
        fieldTxt = '[' + '],['.join(fields) + ']'

    #Default if DateField = None then reads all dataRange
    if DateField == None:
        sqlText = "select rowid, {1} from {0}".format(table,fieldTxt)
    else:
        sqlText = "select rowid, {1} from {0} where"\
        "(date({2}) > date('{3}') and "\
        "date({2}) < date('{4}') )".format(table,fieldTxt,DateField,startDate,endDate)

    print sqlText
    data = psql.read_frame(sqlText, con )
    return data

def to_weka(data,outfile):
    
    data.to_csv(outfile,index=False, quoting=csv.QUOTE_NONNUMERIC)


path = "/home/phcostello/Documents/Data/iHub/S3_RawData/"
dbfile = "CrowdSourcingData.sqlite"
con = sqlite3.connect(path+ dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
tbls = showTables(con)
print tbls

table = "HT_Annotated"
DateField = '[twitter.created_at]'
startDate = "2011-03-03"
endDate = "2015-03-05"
outfile = 'SampleDb.csv'

fields = ['match_rowid',\
          'twitter.links',\
'twitter.user.verified',\
'twitter.user.listed_count',\
'twitter.text',\
'twitter.mentions',\
'twitter.mention_ids',\
'klout.score',\
'twitter.hashtags',\
'twitter.user.statuses_count',\
'twitter.user.followers_count',\
'twitter.user.friends_count',\
'twitter.user.geo_enabled',\
'language.confidence',\
'twitter.user.lang',\
'twitter.created_at',\
'twitter.user.created_at',\
'Newsworthy']



data = readDB(con, table, startDate, endDate, DateField,fields)
columns = list(data.columns)
columns
data.head()

len(data)

#count items in string lists
fieldstocount = ['twitter.links',\
'twitter.mentions',\
'twitter.hashtags']
def countlist(x):
    if x == None:
        return 0
    else:
        return len(x.split(','))
counts = data[fieldstocount].applymap(countlist)
counts['match_rowid'] = data['match_rowid']
print len(counts)
counts.head()


#Check fields that are t/f
fieldsTF = ['twitter.links' ,\
            'twitter.user.verified',\
            'twitter.mentions',\
            'twitter.user.geo_enabled']
data[fieldsTF].head()
def isTF(x):
    #Have to take care of two case, where x is None and where x in NaN
    if x == None or ( isinstance(x , np.float64) and np.isnan(x)):
        return False
    else:
        return True
truefalse = data[fieldsTF].applymap(isTF)
truefalse['match_rowid']=data['match_rowid']
print len(truefalse)
truefalse.head()

#Create twitter age
twitterAgeFields = ['twitter.created_at' ,\
            'twitter.user.created_at']
#Convert to unicode string to datetime
data[twitterAgeFields].head()
data[twitterAgeFields].ix[0,0]
dt = pd.to_datetime(data[twitterAgeFields].ix[0,0])
dt = data[twitterAgeFields].applymap(pd.to_datetime)
dt.ix[0,0]                                     
twitterage = pd.DataFrame()
twitterage= dt['twitter.created_at'].apply( lambda x: x.year) - dt['twitter.user.created_at'].apply( lambda x: x.year) 
twitterage = pd.DataFrame(twitterage)
twitterage.columns = ['twitterage']
twitterage['match_rowid']=data['match_rowid']
print len(twitterage)
twitterage.head()

#Word count
def wordcount(x):
    if x == None:
        return 0
    else:
        return len(x.split(' '))
wordcounts = pd.DataFrame(data['twitter.text']).applymap(wordcount)
wordcounts['match_rowid'] = data['match_rowid']
wordcounts.columns= ['wordcounts','match_rowid']
print len(wordcounts)
wordcounts.head()

features = pd.DataFrame()
features = pd.merge(counts,truefalse ,on= 'match_rowid')
features = pd.merge(features,twitterage ,on= 'match_rowid')
features = pd.merge(features,wordcounts ,on= 'match_rowid')
print len(features)
features.head()
features.columns = ['links_number','mentions_number','Hashtags_number',\
                    'match_rowid','links_exist','user_verified','mentions_exist',\
                    'geo_location_exist', 'twitter_age','wordcounts']


#Write to weka friendly csv using custom function above
to_weka(features, 'features.csv')

#Write to db
psql.write_frame(features, "Features" , con)
con.commit()

import os
os.getcwd()



#Selection random rows from dataframe
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
