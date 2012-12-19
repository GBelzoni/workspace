'''
Created on Dec 6, 2012

@author: phcostello
'''

import market_data as md
import trade as td
import Portfolio as pf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from scikits.statsmodels.examples.es_misc_poisson2 import self

class Trade_Strategy(object):
    '''
    classdocs
    '''

    def __init__(self, market_data, portfolio, initial_time_index):
        '''
        Constructor
        '''
        self.market_data = market_data
        self.portfolio = portfolio
        self.time = initial_time_index
        self.result = pd.DataFrame
        
    def upd_signal(self):
        pass
    
    def upd_portfolio(self):
        pass
    
    def run_strategy(self):
        pass


class Delta_Hedging(Trade_Strategy):
    
    def upd_signal(self):
        
        portSlice = pf.PortfolioSlice(portfolio = self.portfolio, 
                                      market_data = self.market_data,
                                      time_index = self.time)
        
        delta = portSlice.delta()
        
    def upd_portfolio(self):
        
        #Update portfolio by making delta neutral
        delta = self.upd_signal()
        
        #upd portfolio
        name = "Hedge" + str(self.time)
        thisHedge = td.TradeEquity(name = name,
                                   notional = - delta, 
                                   price_series_label = 'underlying')
        
        self.portfolio.add_trade(thisHedge)
        
        #update cash for trade
        md_slice = md.market_data_slice(self.market_data, self.time)
        self.portfolio.trades[0].notional -= thisHedge.value(md_slice)
        
    
    def run_strategy(self):
        
        #Run strategy making sure to inflate notional each step
        timeInd = self.time
        maxLoop = len(self.market_data.core_data)
        num_results = maxLoop - timeInd 
            
        self.result = np.zeros((num_results,),dtype=[('Time','f4'),('Value','f4'),('Signal','f4')])
        #pd.DataFrame(columns = ('Time','Value','Signal'))
        
        for i in range(0,(num_results)):
                     
            timeInd = self.time
            signal = self.upd_signal()
            portfolio_slice = pf.PortfolioSlice(self.portfolio,self.market_data,self.time)
            md_slice = portfolio_slice.md_slice
            
            time = self.market_data.core_data.index[timeInd]
            
            #update portfolio so which delta hedges for this period
            self.upd_portfolio()
            
            #Record result
            res_row = (time, sum(portfolio_slice.value()),signal)
            self.result[i]  = res_row          
            
            #Increase time to next period - make sure to inflate the cash by the interest rate
            self.portfolio.trades[0].inflate(md_slice)
            self.time +=1
            
        
        self.result = pd.DataFrame(data = self.result)     
        
 
class MA_Trade_Strategy(Trade_Strategy): 
    
    ###Implements methods for MA trade strategy ###
        
    def upd_signal(self):
        
        ### This returns the update signal from the current data ###
        time = self.time
        
        Data0 = pf.PortfolioSlice( self.portfolio, self.market_data, time-1)
        Data0 = Data0.md_slice.data
        Data1 = pf.PortfolioSlice( self.portfolio, self.market_data, time)                                  
        Data1 = Data1.md_slice.data
        
        #Previous Moving average vals
        MAs0  = Data0["MAs"]    
        MAl0 = Data0["MAl"]
     
        #Current MA vals
        MAs1 = Data1["MAs"]
        MAl1 = Data1["MAl"]
      
        #Check if there is an upcrossing this step
        signal = ""
        if  ( MAs0 < MAl0 ) and ( MAs1 > MAl1 ):
            signal = "buy"
        elif ( MAs0 > MAl0 ) and ( MAs1 < MAl1 ):
            signal = "sell"
        else:
            signal = "hold"
                    
        return(signal)
        
    def upd_portfolio(self):
        
        signal = self.upd_signal()
        trade_number = 1
        trade = None
        if signal == 'buy':
            
            #Create Trade
            trade = td.Trade(name = "Trade"+str(trade_number), 
                             type = "Eq", 
                             notional = 1)
            
            #Add to portfolio
            self.portfolio.add_trade(trade)
            
            #update cash for trade
            md_slice = md.market_data_slice(self.market_data, self.time)
            self.portfolio.trades[0].notional -= trade.value(md_slice)
            
        elif signal == 'sell':
            
            trade = td.Trade(name = "Trade"+str(trade_number), 
                             type = "Eq", 
                             notional = -1)
        
            #Add to portfolio
            self.portfolio.add_trade(trade)
            
            #update cash for trade
            md_slice = md.market_data_slice(self.market_data, self.time)
            self.portfolio.trades[0].notional -= trade.value(md_slice)
        
          
        
    def run_strategy(self):
        timeInd = self.time
        maxLoop = len(self.market_data.core_data)
        num_results = maxLoop - timeInd 
            
        self.result = np.zeros((num_results,),dtype=[('Time','f4'),('Value','f4'),('Signal','a10')])
        #pd.DataFrame(columns = ('Time','Value','Signal'))
        
        for i in range(0,(num_results-100)):
                     
            timeInd = self.time
            signal = self.upd_signal()
            portfolio_slice = pf.PortfolioSlice(self.portfolio,self.market_data,self.time)
            time = self.market_data.core_data.index[timeInd]
            #res_row = {'Time' : time,'Value' : sum(portfolio_slice.value()),'Signal' : signal}
            res_row = (time, sum(portfolio_slice.value()),signal)
            #This can be sped up by dimensioning the array correctly to start with
            #self.result = self.result.append(res_row, ignore_index=True)
            self.result[i]  = res_row          
            #Update so next period value reflects updated portfolio
            self.upd_portfolio()
            self.time +=1
            
        
        self.result = pd.DataFrame(data = self.result) 
    
    def print_trades(self):
        print [td.name for td in self.portfolio.trades]
    
    def plot(self):
        
        self.market_data.core_data['AORD.Close'].plot()
        self.market_data.core_data['MAl'].plot()
        self.market_data.core_data['MAs'].plot()
        plt.show()
        
        
if __name__ == '__main__':
    
import trade as td
import numpy as np
import pandas as pd
import Portfolio as pf
import GenerateData as gd
import matplotlib.pyplot as plt

steps = 100

r = 0.3
dividend = 0 
vol = 0.1
S0 = 100.0
t0 = 0.0
expiry = 1
K = 100.0


#Generate Series
rseries = pd.Series(steps*[r])
dividendseries = pd.Series(steps*[dividend])
volseries = pd.Series(steps*[vol])


ts = gd.GenerateLogNormalTS(S0, mu=0.03, covariance=vol, steps=steps)
ts = ts.get_data()
plt.plot(ts)
plt.show()

    
    #setup market data#
    #First setup data as list
    data = np.array([r,S,vol])
    data.resize(1,3)
    
    #Then convert to types needed for pricing
    columns = ["rate",
               "underlying",
               "vol"]
    
    
    data = pd.DataFrame(data, columns = columns)
    md1 = md.market_data(data)

    #need to add to self to use in test functions
    md_slice = md.market_data_slice(md1,time_index=0)
    
    #Setup vanilla option trade
    tradeCall = td.TradeVanillaEuroCall(name = "Call",
                                        notional = 1,
                                        strike = 100,
                                        expiry = 0.5)
                                        
    price = tradeCall.price(md_slice)
    print "price = ", price
    delta = tradeCall.delta(md_slice)   
    print "delta = ", delta
    
    #Setup portfolio
    tradeCash = td.TradeCash(name = "Cash", 
                             notional = 100, 
                             rate_label = 'rate')
    
    tradeEquity = td.TradeEquity(name = "Equity", 
                                 notional = 1, 
                                 price_series_label = "underlying")
    
    
    port1 = Portfolio("port1")
    port1.add_trade(tradeCash)
    port1.add_trade(tradeEquity)
    port1.add_trade(tradeCall)
    
    port1Slice = PortfolioSlice(portfolio = port1, 
                                market_data= md1, 
                                time_index = 0)
    
    prt1Val = port1Slice.value()
    print "Portfolio Value" , prt1Val
    
    prt1Del = port1Slice.delta()
    print "Portfolio Del" , prt1Del         
  