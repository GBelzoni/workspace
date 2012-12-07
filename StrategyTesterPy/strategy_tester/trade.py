'''
Created on Nov 29, 2012

@author: phcostello
'''
import strategy_tester.market_data as md


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
        
        ### Prices trade given trade type###
        #This needs a lot of work. Should be linked to market data type to price
        if self.type == "Cash":
            return 1
        elif self.type == "Eq":
            return market_data_slice.data['AORD.Close']
        else:
            return "Trade Type Not recognized"
        
    def value(self, market_data_slice):
        
        return self.price(market_data_slice) * self.notional
        
        