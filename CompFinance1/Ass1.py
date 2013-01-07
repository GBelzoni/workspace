'''
Created on Jan 5, 2013

@author: phcostello
'''
import math
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt

#if __name__ == '__main__':

from pandas.io.data import DataReader
from datetime import datetime

fromDate = datetime(2011,1,1)
toDate = datetime(2012,1,1)

tickers = ['GOOG','^GSPC','AAPL']

s = dict()
dataframes = dict()
for ticker in tickers:    
   
    df = DataReader(ticker,  "yahoo", fromDate, toDate)
    df['Cumlative'] = df['Adj Close'] / df['Adj Close'][0]
    daily = df['Adj Close'][1:].values / df['Adj Close'][:-1].values - 1
    s[ticker] = math.sqrt(250) * np.average(daily) / np.std(daily)
    dataframes[ticker] = df



df = dataframes['AAPL']
plt.plot(df.index,df['Adj Close'])
plt.show()

s
daily = df['Adj Close'][1:].values / df['Adj Close'][:-1].values - 1
plt.plot(daily)
plt.show()

s[ticker] = math.sqrt(250) * np.average(daily) / np.std(daily)
df.head()


sharpes = list(reversed(sorted(s.iteritems(), key=operator.itemgetter(1))))

sp500 = DataReader("^GSPC",  "yahoo", datetime(2000,1,1), datetime(2012,1,1))
apple = DataReader("AAPL","yahoo", datetime(2000,1,1), datetime(2012,1,1))




print goog["Adj Close"]

plt.plot(goog["Adj Close"])
plt.show()