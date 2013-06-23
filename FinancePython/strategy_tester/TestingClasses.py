'''
Created on Jun 23, 2013

@author: phcostello
'''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.core.numeric import dtype
#from scipy.optimize import minimize

from scipy.optimize import minimize, anneal, brute

import time
import pickle
import datetime

import market_data as md
import trade as td
import Portfolio as pf
import TradeStrategyClasses as tsc
import ResultsAnalyser as ra
import DataHandler.DBReader as dr

#
#class StrategyTesting(object):
#    '''
#    classdocs
#    '''
#    
#    
#    #split data in training and test
#    
#    #train strategy
#        
#        #get training data
#        
#        #initialise optim parameters
#        
#        #train strategy - do opitmisation
#        #ie we have opt_parms = optimize( strategy(params), init_params)), where strategy is
#                
#            #Strategy(params)
#            
#                #fit any derived data such as technicals, given params
#                #initialise portfolio depending on params and market data
#                #runStrategy
#                #return target to optimise, e.g. sharpe ratio
#       
#        #save optim params
#        
#        #save results
#            
#    #test strategy
#        
#        #run strategy on test set using last optim results
#        
#        #Check performance
#            
#    #report  
#        
#    
#
#    def __init__(selfparams):
#        '''
#        Constructor
#        '''
#        
#        self.dummy = 'dummy'
        
from ImplementedStrategies import PairTradeSP500

#Read in data and setup object
dbpath = "/home/phcostello/Documents/Data/FinanceData.sqlite"
the_data_reader = dr.DBReader(dbpath)
SP500 = the_data_reader.readSeries("SP500")
BA = the_data_reader.readSeries("BA")

dim = 'Adj_Close' #Choose dim to analyse
SP500AdCl = SP500[dim]
BAAdCl = BA[dim]
dataObj = pd.merge(pd.DataFrame(BAAdCl), pd.DataFrame(SP500AdCl), how='inner',left_index = True, right_index = True)
dataObj.columns = ['y','x']

#Construct data object for pairs trading strat
pmd = md.pairs_md(dataOb=dataObj,xInd='x',yInd='y')
maxdate = datetime.date(2013,1,1)
pmd.core_data = pmd.core_data[:maxdate]
pmd.fitOLS()



def optimFunc(pars):
    
    stdWindowLength = pars[0]
    entryScale= pars[1]
    exitScale= pars[2]
    
#    #Read in data and setup object
#    dbpath = "/home/phcostello/Documents/Data/FinanceData.sqlite"
#    the_data_reader = dr.DBReader(dbpath)
#    SP500 = the_data_reader.readSeries("SP500")
#    BA = the_data_reader.readSeries("BA")
#    
#    dim = 'Adj_Close' #Choose dim to analyse
#    SP500AdCl = SP500[dim]
#    BAAdCl = BA[dim]
##        print SP500AdCl.head()
##        print BAAdCl.head()
#    dataObj = pd.merge(pd.DataFrame(BAAdCl), pd.DataFrame(SP500AdCl), how='inner',left_index = True, right_index = True)
#    dataObj.columns = ['y','x']
#    
#    #Construct data object for pairs trading strat
#    pmd = md.pairs_md(dataOb=dataObj,xInd='x',yInd='y')
#    maxdate = datetime.date(2013,1,1)
#    pmd.core_data = pmd.core_data[:maxdate]
#    pmd.fitOLS()
    pmd.generateTradeSigs(stdWindowLength, entryScale, exitScale)
    
    #Setup portfolio
    spreadTrade = td.TradeEquity("spread", notional=0, price_series_label="spread")
    port = pf.Portfolio("portfolio", cashAmt=100)
    port.add_trade(spreadTrade)
    #No more trade types
    #port.fixed_toggle()
    
    #Setup Strategy
    pairsStrat = tsc.Reversion_EntryExitTechnical(market_data=pmd, portfolio=port, initial_time_index=1)
    
    tic = time.clock()
    pairsStrat.run_strategy()
    toc = time.clock()
    print "strategy took {} seconds to run".format(toc - tic)
    ra1 = ra.ResultsAnalyser(pairsStrat)
    
    sharpe_ratio = ra1.sharpe_ratio()
    res = -1000*sharpe_ratio
    print "parameters", pars
    print "result", res
    return res
    

    
    
#print (optimFunc([20,2,1]) - optimFunc([17,2,1]))/20
print optimFunc([20,2.4,2])

x0=[20.0,2.4,2]
#res = minimize(optimFunc,x0=[100.0,2.0,1.0],tol = 0.001)
res = brute(optimFunc, ranges = (slice(10,50,5),slice(2,3,0.2),slice(1.4,3,0.2)))

print res

#[ 20.36111111   2.56509259   1.56962963]

        