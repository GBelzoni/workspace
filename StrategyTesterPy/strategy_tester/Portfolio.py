'''
Created on Nov 29, 2012

@author: phcostello
'''

import market_data as md

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
    
        