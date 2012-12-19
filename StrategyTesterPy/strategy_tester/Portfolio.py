'''
Created on Nov 29, 2012

@author: phcostello
'''

import strategy_tester.market_data as md


class Portfolio(object):
    '''
    classdocs
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        self.trades = []
    
    def add_trade(self, trade):
        
        self.trades.append(trade)
    
    # print method 

class PortfolioSlice(object):
    '''
    classdocs
    '''


    def __init__(self, portfolio, market_data, time_index):
        '''
        Constructor
        '''
        
        self.md_slice = md.market_data_slice(market_data, time_index)
        self.portfolio = portfolio
        self.time_index = time_index
        
    def price(self):
        
        price_vec = [ trade.price(self.md_slice) for trade in self.portfolio.trades]
        return price_vec
    
    def value(self):
        
        value_vec = [ trade.price(self.md_slice)*trade.notional for trade in self.portfolio.trades]
        return value_vec
    
    def delta(self):
        
        delta = 0
        for trade in self.portfolio.trades:
            
            try:
                thisDelta = trade.delta(self.md_slice)
                delta += thisDelta
            except:
                continue
            
            return delta 
        
        
if __name__ == '__main__':
    
    import trade as td
    import numpy as np
    import pandas as pd
    
    r = 0.05
    dividend = 0.0
    vol = 0.1
    S = 100.0
    t0 = 0.0
    expiry = 0.001
    K = 100.0
    
     
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
    
    