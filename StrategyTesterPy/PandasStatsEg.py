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


import strategy_tester.market_data as md

SP500 = md.read_db(con, "SP500")
BA = md.read_db(con,"BA")

dim = 'Adj Close'
SP500AdCl = SP500[dim]
BAAdCl = BA[dim]


#tableName = "SP500"
#readTbSQL = "SELECT * FROM {}".format(tableName)
#data = psql.read_frame(readTbSQL,  con, index_col='Date',)     
#data.head()
#data.index

data = BAAdCl - 0.0409*SP500AdCl -15.1802
data.plot()
plt.show()

#Do OLS - Choose BA and SP500 as have checked if cointegrated in R
BAAdCl.head()
SP500AdCl.head()
mergeData = pd.merge(pd.DataFrame(BAAdCl), pd.DataFrame(SP500AdCl), how='inner',left_index = True, right_index = True)
mergeData.head()
import statsmodels.api as sm
mergeData.columns
y = mergeData.icol(0)
x = mergeData.icol(1)
x = sm.add_constant(x)
results = sm.OLS(y,x).fit()

print results.summary()


#Create returns
dataCladv = dataCl.shift(1)
merged = pd.merge(dataCl,dataCladv,left_index=True,right_index=True)
merged.head()
rets = dataCl/dataCladv - 1
rets.head()

dataCl,data

#Calculate as above
rets = dataCl.pct_change()
rets.plot()
plt.show()

ret_index = (1 + rets).cumprod()
ret_index.ix[0]=1 #First value is nan so have to set to one
ret_index.head() 
ret_index.plot()
plt.show()

#sharpe ratio - vanilla definition, usually is s.r. of returns in excess over benchmark
daily_sr = lambda x : x.mean() / x.std()

daily_sr(rets)

### Check if stationary
import statsmodels.api as sm
rets2 = rets.ix[1:]
result = sm.tsa.adfuller(rets2)
print result

import statsmodels.tsa.stattools as sttl
sttl.adfuller(rets2)
result = sttl.adfuller(ret_index,maxlag=1,regression = 'nc',store=True,regresults=True)
rstore = result[3]
rstore
import statsmodels.tsa as tsa

## ar model ?? can't get working
mod1 = tsa.ar_model.AR(ret_index,freq='D')
fittedMod = mod1.fit(maxlag=1)
yyy = tsa.ar_model.ARResults(mod1,params='aic')
fittedMod._methods

###Arima
ARMAmod1 = tsa.arima_model.ARMA(rets2,freq='D')
fittedMod = ARMAmod1.fit(order=(2,1),trend='c', method='css-mle',disp=-1)
fittedMod._wrap_methods
fittedMod._wrap_attrs
fittedMod._results
fittedMod._methods
r1 = fittedMod._results
r1.params
r1.pvalues
r1.predict





## Fit basic model and check errors

## Look at autocorrelation

## Do seasonality

## Do GARCH

## Do VAR

  