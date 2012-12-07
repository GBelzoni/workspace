'''
Created on Nov 21, 2012

@author: phcostello
'''

import rpy2.robjects as ro
import numpy
import scipy
import pandas
import matplotlib.pyplot as plt

import strategy_tester.market_data as md
import strategy_tester.trade as td
import strategy_tester.Portfolio as pt
import strategy_tester.TradeStrategyClasses as tsc

from strategy_tester.Portfolio import Portfolio


reload(md)
reload(td)
reload(pt)

from rpy2.robjects.packages import importr

graphics = importr('graphics')
grdevices = importr('grDevices')
base = importr('base')
stats = importr('stats')
zoo = importr('zoo')

#Need to add params to importr as xts and quantmod have conflicts
xts = importr("xts", robject_translations = {".subset.xts": "_subset_xts2",                                            "to.period": "to_period2"})
quantmod = importr('quantmod', robject_translations = {"skeleton.TA": "skeleton_TA2"})

#if __name__ == '__main__':
#    pass

#Read Data
AORD = ro.r('read.table("~/Documents/R/StrategyTester/Data/AORD.csv",header=T, sep=",")')
AORD = zoo.as_zoo(AORD)#, order_by = ro.r.rownames(AORD))

#Read into ST MarketData type
MD1 = md.market_data(AORD)
MD1.names[0]
type(MD1.core_data)


#Plotting with matlibplot
df1 = MD1.core_data['AORD.Close']
type(df1)
df1.plot()
plt.show()


MD1.core_data['AORD.Close'][0]
MD1.core_data.ix[0]
MD1.core_data.index

#Take slice of of MD
MDSlice1 = md.market_data_slice(MD1,1)
#MADSlice1 = md.market_data_slice(MAD1,56)
print MDSlice1.data    
print MDSlice1.time_stamp  


#Create Trades and value
trade_eq = td.Trade("TestEq","Eq", 100)
trade_cash = td.Trade("TestEq","Cash", 100)

trade_eq.price(MDSlice1)
trade_cash.price(MDSlice1)
trade_eq.value(MDSlice1)
trade_cash.value(MDSlice1)

#Create Portfolio and value
port_test = pt.Portfolio("port_test")
port_test.add_trade(trade_eq)
print port_test.trades
port_test.add_trade(trade_cash) 
print port_test.trades

ps_test = pt.PortfolioSlice(port_test, MD1, 1)
ps_test.price()
sum(ps_test.value())

#Test Trade Strategy
#Crossover in the moving averages
reload(tsc)
reload(td)
MAD1 = md.simple_ma_md(AORD,'AORD.Close', 10, 20)
MAD1.core_data['MAl'][0:30]

MAD1.core_data['AORD.Close'][56:100].plot(style = 'k--')
MAD1.core_data['MAl'][56:100].plot(style = 'k')
MAD1.core_data['MAs'][56:100].plot(style = 'k')

#plt.show()

MADSlice0 = md.market_data_slice(MAD1,57)
MADSlice1 = md.market_data_slice(MAD1,58)
MADSlice0.data[['MAl','MAs']]
MADSlice1.data[['MAl','MAs']]

#Test updateSignal
port1 = pt.Portfolio("port1")
[td.name for td in port1.trades]
import strategy_tester.trade as td
reload(td)

trade_cash =td.Trade("Cash","Cash", 0)
trade_cash.notional
port1.add_trade(trade_cash)
[td.name for td in port1.trades]

import strategy_tester.TradeStrategyClasses as tsc
reload(tsc)

TS1 = tsc.MA_Trade_Strategy(MAD1,port1,58)
TS1.portfolio.trades
TS1.upd_signal()
[td.name for td in TS1.portfolio.trades]
#TS1.upd_portfolio()
[td.name for td in TS1.portfolio.trades]
[[td.name, td.notional] for td in TS1.portfolio.trades]
TS1.time
PS2 = pt.PortfolioSlice(TS1.portfolio,TS1.market_data,TS1.time)
PS2.value()
print TS1.result
TS1.run_strategy()
len(TS1.portfolio.trades)
PS2 = pt.PortfolioSlice(TS1.portfolio,TS1.market_data,TS1.time)
sum(PS2.value())

index = TS1.result['Time']
vals = pandas.Series(TS1.result['Value'], index = index) + 5500
vals.plot()
TS1.market_data.core_data['AORD.Close'].plot()
TS1.market_data.core_data['MAl'].plot()
TS1.market_data.core_data['MAs'].plot()

plt.show()
vals[6]


    