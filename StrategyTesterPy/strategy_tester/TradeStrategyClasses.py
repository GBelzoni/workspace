'''
Created on Dec 6, 2012

@author: phcostello
'''

import market_data as md
import trade as td
import Portfolio as pf


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
        print "Signal", signal
        if signal == 'buy':
            
            #Create Trade
            trade = td.Trade(name = "Trade"+str(trade_number), 
                             type = "Eq", 
                             notional = 100)
            print "created buy"
            #Add to portfolio
            self.portfolio.add_trade(trade)
            
            #update cash for trade
            md_slice = md.market_data_slice(self.market_data, self.time)
            self.portfolio.trades[0].notional += trade.value(md_slice)
            
        elif signal == 'sell':
            
            trade = td.Trade(name = "Trade"+str(trade_number), 
                             type = "Eq", 
                             notional = -100)
        
            #Add to portfolio
            self.portfolio.add_trade(trade)
            
            #update cash for trade
            md_slice = md.market_data_slice(self.market_data, self.time)
            self.portfolio.trades[0].notional += trade.value(md_slice)
            
        
    def run_strategy(self):
        timeInd = self.time
        maxLoop = self.market_data.core_data.
            
            #object@Results = data.frame( Time = 0,  Value = 0, Signal = "hold") 
            object$Results = data.frame(matrix(nrow = (maxLoop-timeInd), ncol =3))
            colnames(object$Results)=c("Time","Value","Signal")

            for( i in 1:(maxLoop-timeInd))
            {
                signal = updSig(object)
                PS = PortfolioSlice(object$MarketData  ,object$Portfolio, timeInd)
                timeInd = object$CurrentTime
                time = index(object$MarketData$Data)[timeInd]
                object$Results[i,] = c(time,sum(Value(PS)),signal)
                object = updatePortfolio(object)
            }    
            object$Results$Time =as.numeric(object$Results$Time)
            return(object)
        }
        