# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

#Created by Patrick Costello 5 Jan 2013
#Boiler Plate

import math
import numpy as np
import scipy as sp
import pandas as pd
reload(pd)
import matplotlib.pyplot as plt

print pd.version.version

# <codecell>

#Reading Data - given by Matt Johnson
df = pd.read_csv('ymData.csv')
print df.head(5)
#Can also use parse_dates arguement but really slow
#df = pd.read_csv('ymData.csv',parse_dates = [0])
#better to do in seperate step
df['time'] = pd.to_datetime(df['time'])
print df.head(5)

# <codecell>

#Time munging
import datetime
from dateutil.parser import parse
now = datetime.datetime.now()
from pandas.tseries.offsets import Hour, Minute, Day
day = Day(7)
print (now).weekday()
print now

# <codecell>

#Analysing Data

print df.ix[14590:14620]
print df.columns

#Get levels of observable
print df['type'].unique()
#print df.drop_duplicates(['type'])['type']

#Filtering on type = ASK_BEST
df2 = df[df['type'] == 'ASK_BEST']
df2.ix[5590:5630]

# <codecell>

#Creating session ids
#Must be a better way
df2 = df['time'][0:50]

from datetime import time
t = time(8,0,0)
t2 = time(22,20,1)

ranges = { 'sydAM': [ time(8,0,0),time(12,0,0)] ,
          'sydPM' : [time(12,0,0),time(16,30,0)] ,
          'ldnAM' : [time(16,30,0), time(23,59,59)] ,
          'ldnPM' : [time(0,0,0), time(8,0,0)] }

def session_label( time):
    for it in ranges:
        if(ranges[it][0] <= time < ranges[it][1]):
            return it


print [ session_label( t.time()) for t in df2]

# <codecell>

#Adding integer key
print df.count()[0]
df['key'] = range(df.count()[0])
df.head()

#Using list comprehension below seems a bit slow, but df.map has issues with datetime objects

#Adding weekday monday = 0
df['weekday'] = [x.day for x in df['time']]

#Adding session
#Must be a way to use cut with Datetime objects
#Add just time portion of date
df[ 'time2'] = [ t.time() for t in df['time']]
df[ 'date'] = [d.date() for d in df['time']]

#Add session label
df['session'] = 'None'
df['session'].ix[ (df['time2'] >= time(8,0,0)) & (df['time2'] < time(12,0,0)) ] = 'sydAM'             
df['session'].ix[ (df['time2'] >= time(12,0,0)) & (df['time2'] < time(16,30,0)) ] = 'sydPM'             
df['session'].ix[ (df['time2'] >= time(16,30,0)) & (df['time2'] <= time(23,59,59,99))] = 'ldnAM'             
df['session'].ix[ (df['time2'] >= time(0,0,0)) & (df['time2'] < time(8,0,0)) ] = 'ldnPM' 



df.head()

# <codecell>

#Pivoting Data so we get ASK BID TRAD columns
table = pd.pivot_table(df,rows = ['key','weekday','session','time','date'], cols = ['type'])

# <codecell>

#Filling NA's so that last value is carried forward
#print table.head(10)
table = table.fillna(method='ffill')

#print table['value'].ix[5600:5610]
table.columns
print table.head()

# <codecell>

#Inserting mids
#print table['value'].head()
table['value','mid'] = ((table['value','ASK_BEST'] + table['value','BID_BEST'])/2)

#print (table['value']*table['size']).head()

#Inserting volweighted mids
AB = ['ASK_BEST','BID_BEST']
vsum = (table['value'] *table['size'])[AB].sum(axis = 1, skipna=False)
ssum = (table['size'])[AB].sum(axis = 1, skipna=False)
table['value','vmid'] = vsum/ssum
#print table['value'].ix[500000:500020]

#Inserting tradedirection
table['tradeDirection'] = 'None'
biddir = (table['value','TRADE'] == table['value','BID_BEST']).map(int)
askdir = (table['value','TRADE'] == table['value','ASK_BEST']).map(int)
table['tradeDirection'] = askdir - biddir
print table.head()
print table[table['tradeDirection']==0]

# <codecell>

#Flattening
#table2 = table.stack()
#print table2.head()
table2 = table.reset_index()
print table2.head()

# <codecell>

#Grouping Simple

#Make groups by perform no calcs
byday = table2.groupby([table2['session'],table2['date'],table2['weekday']])

#Make functions to group by
agfunc = lambda x : (x['size','TRADE']*x['tradeDirection']).sum()
avPfunc = lambda x : (x['size','TRADE']*x['value','TRADE']).sum()/ x['size','TRADE'].sum()

#Do groupings    
ag = byday.apply(agfunc)
avP = byday.apply(avPfunc)

print ag.head()
print avP.head()

#Move index to do merge, some issue merging series rather than df's
ag = ag.reset_index()
avP = avP.reset_index()
agp = pd.merge( ag, avP, on =['session','weekday','date'])

#Rename columns. Have to create a list same length as columns to do renaming
columns = agp.columns.tolist()
columns[3]= 'directedVolume'
columns[4]= 'vwPrice'
agp.columns = columns
print agp.head()
del agp['weekday']
#print group.head()

# <codecell>

type(agp)

#agp = agp.set_index('date')

agp['vwPrice'].plot()

