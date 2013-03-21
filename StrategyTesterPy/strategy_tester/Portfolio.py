'''
Created on Nov 29, 2012

@author: phcostello
'''

import strategy_tester.market_data as md
import strategy_tester.trade as td


class PortfolioError(Exception):
    
    '''
    Errors for portfolio
    '''
    
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg


class Portfolio(object):
    '''
    classdocs
    '''

    def __init__(self, name, cashAmt = 0, rate_Label_ = 'rate'):
        '''
        Constructor
        Sets up initial portfolio with only cash in it.
        cashAmt - can initialise amt to start with
        rate_lable - what interest rate cash will grow by
        '''
        
        #All portfolios must have Cash numerair
        tradeCash = td.TradeCash(name = "Cash", 
                                 notional = cashAmt, 
                                 rate_label = rate_Label_ )
        
        self.name = name
        self.trades = {"Cash" : tradeCash}
        self.tradesFixed = False
    
    def add_trade(self, trade):
        
        '''
        adds trade object to portfolio
        '''
        #Throw error if try to add second cash trade.
        if trade.type == "Cash":
            raise PortfolioError("Can only have one cash trade")
        
        #Throw error if trades in portfolio are fixed
        if self.tradesFixed == False:
            self.trades[ trade.name ] = trade
        else:
            raise PortfolioError("Adding trade when Portfolio fixed on")
              
    
    def fixed_toggle(self):
        ### flag to disable adding new trades ###
        self.tradesFixed = not(self.tradesFixed)
    
    
    def get_notional(self):
        
        return [td.notional for td in self.trades.values()]
        
    def adjustNotional(self, adjustments):
        
        ###Adjustments are dictionary of trade Name and adjustment ammount####
        for ad in adjustments.items():
            
            try:
                self.trades[ad[0]].notional += ad[1]
            except AttributeError:
                print "Error notional adjustment, Didn't find {} in portfolio".format(ad[0])
        
        
        

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
        
        price_vec = [ trade.price(self.md_slice) for trade in self.portfolio.trades.values()]
        return price_vec
    
    def value(self):
        
        value_vec = [ trade.price(self.md_slice)*trade.notional for trade in self.portfolio.trades.values()]
        return value_vec
    
    def adjustCash(self, tradeNotionalChnge):
        
        delCash = 0
        
        ###Cash is adjusted to reflect change in portfolio value due to change in notional### 
        for td in tradeNotionalChnge.keys():
            
            #Work out price of trade with notional being adjusted
            thisTradePrice = self.portfolio.trades[td].price(self.md_slice)
            #add to cash adjustment for change in notional
            delCash += thisTradePrice * tradeNotionalChnge[td]
        
        self.portfolio.trades['Cash'].notional -= delCash
        
    
    def delta(self):
        
        delta = 0
        for trade in self.portfolio.trades.values():
            
            try:
                thisDelta = trade.delta(self.md_slice)
                delta += thisDelta * trade.notional
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
    tradeEquity = td.TradeEquity(name = "Equity", 
                                 notional = 1, 
                                 price_series_label = "underlying")
    
    
    port1 = Portfolio("port1", cashAmt = 100,  rate_Label_ = 'rate')
    port1.add_trade(tradeEquity)
    port1.add_trade(tradeCall)
    
    port1Slice = PortfolioSlice(portfolio = port1, 
                                market_data= md1, 
                                time_index = 0)
    
    prt1Val = port1Slice.value()
    
    
    print "Portfolio Trades", port1.trades.keys()
    print "Portfolio Value" , prt1Val
    
    prt1Del = port1Slice.delta()
    print "Portfolio Del" , prt1Del
    
    print "Notional before", port1.get_notional()
    
    adjNotional = { 'Call': 0.5 , 'Equity': 1}
    port1.adjustNotional(adjNotional)
    print "Notional after", port1.get_notional()
    
    