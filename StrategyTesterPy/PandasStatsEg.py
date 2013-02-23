'''
Created on Feb 23, 2013

@author: phcostello
'''

import numpy as np
import pandas as pd
import scipy as sp
import pandas.io.sql as psql
import sqlite3
import matplotlib.pyplot as plt

# if __name__ == '__main__':

con = sqlite3.connect("/home/phcostello/Documents/Data/FinanceData.sqlite")

tableName = "SP500"
readTbSQL = "SELECT * FROM {}".format(tableName)
data = psql.read_frame(readTbSQL,  con, index_col='Date',)     
data.head()
data.index


#Convert index to datetime
from datetime import datetime
from dateutil.parser import parse
data.index[0]
parse(data.index[0])
data.index = [parse(x)for x in data.index]
data.head()

#
dataCl = data[['Close']]
dataCl.head()



dataCl.plot()
plt.show()
### Check if stationary

## Fit basic model and check errors

## Look at autocorrelation

## Do seasonality

## Do GARCH

## Do VAR

  