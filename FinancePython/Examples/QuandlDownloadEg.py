'''
Created on Jun 19, 2013

@author: phcostello
'''


import Quandl
import pandas as pd
import datetime

start = datetime.datetime(2013,2,23)
end = datetime.datetime.now().date()

str(end)

quandlAuthToken = 'ai3HEfkXjxkuhLzdn2n8'

data =  Quandl.get("QUANDL/AUDUSD",
                   authtoken = quandlAuthToken,
                   trim_start ="2013-1-1", 
                   trim_end="2013-10-5")
colnames = list(data.columns)
colnames = [ col.replace(" ","_") for col in colnames]
data.columns = colnames

data = data.reset_index()

data.head()
data.columns