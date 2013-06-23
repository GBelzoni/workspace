'''
Created on Nov 29, 2012

@author: phcostello
'''
import strategy_tester.market_data as md
import math
import FinanceAnalyticFunctions as faf

from scipy.stats import norm
from strategy_tester.market_data import market_data, market_data_slice


class Trade(object):
    '''
    classdocs
    '''

    def __init__(self, name, type, notional):
        '''
        Constructor
        '''
        self.name = name
        self.type = type
        self.notional = notional
        
    def price(self, market_data_slice):
        
        return "No price function implemented"
                
    def value(self, market_data_slice):
        
        return self.price(market_data_slice) * self.notional
    
class TradeCash(Trade):
    ### Basic risk free cash trade ###
    def __init__(self,name, notional,  rate_label = "rate"):
        Trade.__init__(self, name = name, type="Cash", notional=notional)           
        self.rate_label = rate_label
            
    def price(self , market_data_slice):
        ### Assume nominal units so price = 1. ##
        
        return 1
    
    def value(self , market_data_slice):
        ### Assume nominal units so price = 1. ##
        return self.notional
    
    def inflate(self,market_data_slice):
            
        rate = market_data_slice.data[self.rate_label]
        period_length = market_data_slice.period_length
        self.notional *= math.exp( rate * period_length)
        
    
    
class TradeEquity(Trade):
    
    ### simple equity ts ###
    
    def __init__(self, name, notional, price_series_label = 0):
        Trade.__init__(self, name = name, type="Equity", notional=notional)
        self.price_series_label = price_series_label
    
    def price(self, market_data_slice):
        return market_data_slice.data[self.price_series_label]
    
    def delta(self, market_data_slice):    
        
        return 1  

class TradeVanillaEuroCall(Trade):
    
    ### simple equity ts ###
    
    def __init__(self, name, notional, strike, expiry):
        
        Trade.__init__(self, name = name, type="VanillaEuroCall", notional=notional)
        self.strike = strike
        self.expiry = expiry
        
    def price(self, market_data_slice):
        
        ### wrapper for bs analytic price ###
        
        r = market_data_slice.data['rate']
        vol = market_data_slice.data['vol']
        S = market_data_slice.data['underlying']
        t0 = market_data_slice.time_stamp
        K = self.strike
        expiry = self.expiry
        dividend = 0
        
        price = faf.BS_call(S, K, t0, expiry, r, dividend, vol)
        
        return price
        
    def delta(self, market_data_slice):    
        
        #Calcs delta of trade. This is delta_option_price * notional_option
        
        r = market_data_slice.data['rate']
        vol = market_data_slice.data['vol']
        S = market_data_slice.data['underlying']
        t0 = market_data_slice.time_stamp
        K = self.strike
        expiry = self.expiry
        dividend = 0
        
        epsilon = 0.0001
        
        pricepldel = faf.BS_call(S+epsilon,K,t0,expiry,r,dividend,vol)
        pricemindel = faf.BS_call(S-epsilon,K,t0,expiry,r,dividend,vol)
    
        delta_price = (pricepldel - pricemindel)/(2* epsilon)
        delta = delta_price * self.notional
        
        return delta
    
if __name__ == '__main__':
   
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
    md_cash = md.market_data(data)

    #need to add to self to use in test functions
    md_slice = md.market_data_slice(md_cash,time_index=0)
    
    #Setup vanilla option trade
    tradeCall = TradeVanillaEuroCall(name = "Call",
                                        notional = 1,
                                        strike = 100,
                                        expiry = 0.5)
                                        
    price = tradeCall.price(md_slice)
    print "price = ", price
    delta = tradeCall.delta(md_slice)   
    print "delta = ", delta      
          
        