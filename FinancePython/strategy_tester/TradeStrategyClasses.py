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
from numpy.core.numeric import dtype
import time
import pickle
import datetime

class Trade_Strategy(object):
    '''
    classdocs
    '''

    def __init__(self, 
                 market_data, 
                 portfolio, 
                 initial_time_index,
                 parameters = None):
        '''
        Constructor
        '''
        self.market_data = market_data
        self.portfolio = portfolio
        self.time = initial_time_index
        self.result = pd.DataFrame
        self.parameters = parameters
        
    def upd_signal(self):
        pass
    
    def upd_portfolio(self):
        pass
    
    def run_strategy(self):
        pass

class Delta_Hedging(Trade_Strategy):
    
    #TODO fix market data object so that you don't have to put in increment size in constructor
    # should read from market data object. Maybe md slice object
    
    def __init__(self, market_data, portfolio, initial_time_index, stepsize):
        '''
        Constructor
        '''
        Trade_Strategy.__init__(self, market_data, portfolio, initial_time_index)
        self.stepsize = stepsize
        
    
    def upd_signal(self):
        
        portSlice = pf.PortfolioSlice(portfolio = self.portfolio, 
                                      market_data = self.market_data,
                                      time_index = self.time)
        
        delta = portSlice.delta()
        
        return delta
        
    def upd_portfolio(self):
        
        #Update portfolio by making delta neutral
        delta = self.upd_signal()
        
        #Define hedging trade
        trade = {'underlying' : -delta}
        
        #Adjust notional to hedge
        self.portfolio.adjustNotional(trade)
        
        #Adjust cash to reflect heding notional change
        portSlice = pf.PortfolioSlice(portfolio = self.portfolio, 
                                      market_data = self.market_data,
                                      time_index = self.time)
        portSlice.adjustCash(trade)
        
        
        
    
    def run_strategy(self):
        
        #Run strategy making sure to inflate notional each step
        timeInd = self.time
        maxLoop = len(self.market_data.core_data)
        num_results = maxLoop - timeInd 
            
        self.result = np.zeros((num_results,),dtype=[('Time','f4'),('Value','f4'),('Signal','f4')])
        #pd.DataFrame(columns = ('Time','Value','Signal'))
        
        
        for i in range(1,(num_results-1)):
                     
            timeInd = self.time
            signal = self.upd_signal()
            portfolio_slice = pf.PortfolioSlice(self.portfolio,self.market_data,self.time)
            md_slice = portfolio_slice.md_slice
            md_slice.period_length = self.stepsize
            #print "del Before" , portfolio_slice.delta()
            
            time = self.market_data.core_data.index[timeInd]
            
            #update portfolio so which delta hedges for this period
            self.upd_portfolio()
            #print "del After" , portfolio_slice.delta()
            #Record result
            res_row = (time, sum(portfolio_slice.value()),signal)
            #print res_row
            self.result[i]  = res_row          
            
            
            #Increase time to next period - make sure to inflate the cash by the interest rate
            self.portfolio.trades['Cash'].inflate(md_slice)
            self.time +=1
            
        
        self.result = pd.DataFrame(data = self.result)     
        
class Stop_Loss(Trade_Strategy):
    
    def __init__(self, market_data, portfolio, initial_time_index, stepsize):
        '''
        Constructor
        '''
        Trade_Strategy.__init__(self, market_data, portfolio, initial_time_index)
        self.stepsize = stepsize
    
    
    def upd_signal(self):
        
        portSlice = pf.PortfolioSlice(portfolio = self.portfolio, 
                                      market_data = self.market_data,
                                      time_index = self.time)
        
        delta = portSlice.delta()
        
        return delta
        
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
        
        
        for i in range(1,(num_results-1)):
                     
            timeInd = self.time
            signal = self.upd_signal()
            portfolio_slice = pf.PortfolioSlice(self.portfolio,self.market_data,self.time)
            md_slice = portfolio_slice.md_slice
            md_slice.period_length = self.stepsize
            #print "del Before" , portfolio_slice.delta()
            
            time = self.market_data.core_data.index[timeInd]
            
            #update portfolio so which delta hedges for this period
            self.upd_portfolio()
            #print "del After" , portfolio_slice.delta()
            #Record result
            res_row = (time, sum(portfolio_slice.value()),signal)
            #print res_row
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
  
class Reversion_EntryExitTechnical(Trade_Strategy): 
    
    '''
    Implements a reversion strategy where the marked data has upper and lower
    signals.
    '''
    
    def __init__(self, market_data, portfolio, initial_time_index):
        '''
        Constructor
        
        market_data object requires columns - "spread", "entryUpper", "exitUpper", "entryLower", "exitLower"
        Note that the "spread" column indicates just the general series being traded,
        originally implemented for pairs trade spread, hence name
        
        portfolio object requires a trade object with "price_series_label" = "spread"
        '''
        
        Trade_Strategy.__init__(self, market_data, portfolio, initial_time_index)
        self.tradeEnteredFlag = False
        self.started = False
        
    def upd_signal(self):
        
        ### This returns the update signal from the current data ###
        time = self.time
        
        Data0 = pf.PortfolioSlice( self.portfolio, self.market_data, time-1)
        Data0 = Data0.md_slice.data
        Data1 = pf.PortfolioSlice( self.portfolio, self.market_data, time)                                  
        Data1 = Data1.md_slice.data
        
        #Previous vals
        spread0  = Data0["spread"]    
        upperEntry0 = Data0["entryUpper"]
        upperExit0 = Data0["exitUpper"]
        lowerEntry0 = Data0["entryLower"]
        lowerExit0 = Data0["exitLower"]
        
        #Current vals
        spread1 = Data1["spread"]
        upperEntry1 = Data1["entryUpper"]
        upperExit1 = Data1["exitUpper"]
        lowerEntry1 = Data1["entryLower"]
        lowerExit1 = Data1["exitLower"]
        
        #Check if there is an upcrossing this step
        #If upcrossing then fade trade, ie sell
        signal = ""
        #Enter Signals
        if  ( spread0 < upperEntry0) and ( spread1 > upperEntry1 ):
            signal = ["Enter","sell"]
        elif ( spread0 > lowerEntry0 ) and ( spread1 < lowerEntry1 ):
            signal = ["Enter" , "buy"]
        #Exit Signals
        elif ( spread0 > upperExit0 ) and ( spread1 < upperExit1 ):
            signal = ["Exit","buy"]
        elif ( spread0 < lowerExit0 ) and ( spread1 > lowerExit1 ):
            signal = ["Exit","sell"]
        #Do nothing signal
        else:
            signal = ["hold","hold"]
                    
        return(signal)
        
    def upd_portfolio(self, tradeSize):
        
        '''
        THis updates portfolio given signal
        We need a 'spread' trade in the strategy portfolio so we can adjust that notional
        '''
        
        #We enter trade when crossing entry barrier and no trade on
        #We exit signal when crossing exit barrier and trade on
        signal = self.upd_signal()
        entered = self.tradeEnteredFlag
        
        #Check if started
        if self.started == False:
            #If not then check if spread is between entry levels, if not then don't start
            Data = pf.PortfolioSlice( self.portfolio, self.market_data, self.time)                                  
            Data = Data.md_slice.data
            spread=Data['spread']
            upperEntry = Data['entryUpper']
            lowerEntry = Data['entryLower']
            if lowerEntry < spread and spread < upperEntry:
                self.started = True
            else:
                return
        
        if signal[1] == "sell" and  \
         (( signal[0]=="Enter" and entered == False ) or \
           (signal[0]=="Exit" and entered == True)):
                      
            #Define hedging trade
            trade = {'spread' : - tradeSize}
            
            #Adjust notional to hedge
            self.portfolio.adjustNotional(trade)
            
            #Adjust cash to reflect heding notional change
            portSlice = pf.PortfolioSlice(portfolio = self.portfolio, 
                                          market_data = self.market_data,
                                          time_index = self.time)
            portSlice.adjustCash(trade)
            
            #Set tradeEntered flag to false
            self.tradeEnteredFlag = not(self.tradeEnteredFlag)
        
            
        elif signal[1] == 'buy' and \
        (( signal[0]=="Enter" and entered == False ) or \
           (signal[0]=="Exit" and entered == True)):
            
            #Define hedging trade
            trade = {'spread' : tradeSize}
            
            #Adjust notional to hedge
            self.portfolio.adjustNotional(trade)
            
            #Adjust cash to reflect heding notional change
            portSlice = pf.PortfolioSlice(portfolio = self.portfolio, 
                                          market_data = self.market_data,
                                          time_index = self.time)
            portSlice.adjustCash(trade)
            self.tradeEnteredFlag = not(self.tradeEnteredFlag)
        
    def run_strategy(self):
        timeInd = self.time
        maxLoop = len(self.market_data.core_data)
        num_results = maxLoop - timeInd 
            
        self.result = np.zeros((num_results,),dtype=[('Time','datetime64'),('Value','f4'),('Signal','a10')])
        #pd.DataFrame(columns = ('Time','Value','Signal'))
        
        for i in range(0,(num_results)):
                     
            timeInd = self.time
            signal = self.upd_signal()
            portfolio_slice = pf.PortfolioSlice(self.portfolio,self.market_data,self.time)
            time = self.market_data.core_data.index[timeInd]
            #res_row = {'Time' : time,'Value' : sum(portfolio_slice.value()),'Signal' : signal}
            res_row = (time, sum(portfolio_slice.value()),signal[0])
            #This can be sped up by dimensioning the array correctly to start with
            #self.result = self.result.append(res_row, ignore_index=True)
            self.result[i]  = res_row          
            #Update so next period value reflects updated portfolio
            self.upd_portfolio(tradeSize=1)
            self.time +=1
            
        #Format to pandas dataframe with Time index
        self.result = pd.DataFrame(data = self.result)
        self.result.set_index('Time',inplace=True)
        
    def print_trades(self):
        print [td.name for td in self.portfolio.trades]
    
         

if __name__ == '__main__':
    
    def DeltaHedgeVanillaCallEg():
    
#        import strategy_tester.market_data as md    
#        import strategy_tester.trade as td
#        import strategy_tester.Portfolio as pf
        
        import numpy as np
        import pandas as pd
        import Portfolio as pf
        import GenerateData as gd
        import matplotlib.pyplot as plt
        
        steps = 3000
        stepsize = 1.0/steps
        r = 0.05
        dividend = 0.0 
        vol = 0.2
        S0 = 50.0
        t0 = 0.0
        expiry = 1.0
        K = 50.0
        
        #setup market data#
        #Generate Series
        rseries = steps*[r]
        dividendseries = steps*[dividend]
        volseries = steps*[vol]
        underlyingSeries = gd.GenerateLogNormalTS(S0, mu=0.03, covariance=vol, stepsize=stepsize,steps=steps-1).get_data()
        
        data2 = [rseries,dividendseries,volseries, underlyingSeries]
        data2 = np.array(data2)
        data2.shape
        data2 = data2.transpose()
        data2[1,:]
        
        columns = ['rate','dividend','vol','underlying']
        data = pd.DataFrame(data2, columns = columns)
        
        data.index = list(np.arange(0,steps,dtype='float64')/steps)
        md1 = md.market_data(data)
        
        #need to add to self to use in test functions
        md_slice = md.market_data_slice(md1,time_index=0)
        md_slice.data
        
        tradeUnderlying = td.TradeEquity('underlying',
                                          notional= 0,
                                          price_series_label = 'underlying')
        
        tradeCall = td.TradeVanillaEuroCall(name = "Call",
                                            notional = 0,
                                            strike = K,
                                            expiry = expiry)
                                            
        price = tradeCall.price(md_slice)
        print "price = ", price
        delta = tradeCall.delta(md_slice)   
        print "delta = ", delta
        
        #Setup portfolio
        #First initialise trade type but empty portfolio
        port1 = pf.Portfolio("port1")
        port1.add_trade(tradeUnderlying)
        port1.add_trade(tradeCall)
        
        #Second initialise starting value
        initPort = {'Call':1} 
        port1.adjustNotional(initPort)
        delta = tradeCall.delta(md_slice) 
        print "delta", delta
        trade = {'underlying':-delta}
        port1.adjustNotional(trade)
        port1Slice = pf.PortfolioSlice(portfolio = port1, 
                                    market_data= md1, 
                                    time_index = 0)
        
        initHedgPort = {'Call':1, "underlying":-delta}
        port1Slice.adjustCash(initHedgPort)
        
        
        prt1Val = port1Slice.value()
        print "Portfolio Value" , prt1Val
        
        prt1Del = port1Slice.delta()
        print "Portfolio Del" , prt1Del 
        
        ts_deltaHedge = Delta_Hedging(market_data = md1, 
                                      portfolio = port1, 
                                      initial_time_index = 0,
                                      stepsize = stepsize)
        
        ts_deltaHedge.run_strategy()        
        
        print ts_deltaHedge.result.head(20)
        print ts_deltaHedge.result.tail(20)
        print ts_deltaHedge.portfolio.get_notional()
        
    
        
    
      