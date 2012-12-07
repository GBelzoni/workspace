'''
Created on Dec 6, 2012

@author: phcostello
'''

import market_data as md
import trade as td
import Portfolio as pf
import pandas as pd

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
            
        self.result = pd.DataFrame(columns = ('Time','Value','Signal'))
        
        for i in range(1,(maxLoop-timeInd+1)):
            
            timeInd = self.time
            signal = self.upd_signal()
            portfolio_slice = pf.PortfolioSlice(self.portfolio,self.market_data,self.time)
            time = self.market_data.core_data.index[timeInd]
            res_row = {'Time' : time,'Value' : sum(portfolio_slice.value()),'Signal' : signal}
            
            #This can be sped up by dimensioning the array correctly to start with
            self.result = self.result.append(res_row, ignore_index=True)
                        
            #Update so next period value reflects updated portfolio
            self.upd_portfolio()
            self.time +=1
            
            
        
        