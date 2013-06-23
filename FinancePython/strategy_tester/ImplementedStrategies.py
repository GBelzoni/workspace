'''
Created on Jun 23, 2013

@author: phcostello
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.core.numeric import dtype
import time
import pickle
import datetime

import market_data as md
import trade as td
import Portfolio as pf
import TradeStrategyClasses as tsc
import ResultsAnalyser as ra
import DataHandler.DBReader as dr


def DeltaHedgeVanillaCallEg():
    
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
    
    #addsome cash
    MoreCash = {'Cash':1}
    port1.adjustNotional(MoreCash)
    
    prt1Val = port1Slice.value()
    print "Portfolio Value" , prt1Val
    
    prt1Del = port1Slice.delta()
    print "Portfolio Del" , prt1Del 
    
    ts_deltaHedge = tsc.Delta_Hedging(market_data = md1, 
                                  portfolio = port1, 
                                  initial_time_index = 0,
                                  stepsize = stepsize)
    
    ts_deltaHedge.run_strategy()        
    outfile = open('VanillaCallDelta_strat.pkl','wb')
    pickle.dump(ts_deltaHedge,outfile)
    outfile.close()
    print ts_deltaHedge.result.head(20)
    print ts_deltaHedge.result.tail(20)
    print ts_deltaHedge.portfolio.get_notional()
    
def PairTradeSP500(stdWindowLength, entryScale, exitScale):
    
    #Read in data and setup object
    dbpath = "/home/phcostello/Documents/Data/FinanceData.sqlite"
    the_data_reader = dr.DBReader(dbpath)
    SP500 = the_data_reader.readSeries("SP500")
    BA = the_data_reader.readSeries("BA")
    
    dim = 'Adj_Close' #Choose dim to analyse
    SP500AdCl = SP500[dim]
    BAAdCl = BA[dim]
#        print SP500AdCl.head()
#        print BAAdCl.head()
    dataObj = pd.merge(pd.DataFrame(BAAdCl), pd.DataFrame(SP500AdCl), how='inner',left_index = True, right_index = True)
    dataObj.columns = ['y','x']
    
    #Construct data object for pairs trading strat
    pmd = md.pairs_md(dataOb=dataObj,xInd='x',yInd='y')
    maxdate = datetime.date(2013,1,1)
    pmd.core_data = pmd.core_data[:maxdate]
    pmd.fitOLS()
    pmd.generateTradeSigs(stdWindowLength, entryScale, exitScale)
    
    #Setup portfolio
    spreadTrade = td.TradeEquity("spread", notional=0, price_series_label="spread")
    port = pf.Portfolio("portfolio", cashAmt=100)
    port.add_trade(spreadTrade)
    #No more trade types
    port.fixed_toggle()
    
    #Setup Strategy
    pairsStrat = tsc.Reversion_EntryExitTechnical(market_data=pmd, portfolio=port, initial_time_index=1)
    
    return pairsStrat

    tic = time.clock()
    pairsStrat.run_strategy()
    toc = time.clock()
    print "strategy took {} seconds to run".format(toc - tic)
    outfile = open("pickled_pairs.pkl", 'wb')
    pairs_strategy_run = pickle.dump(pairsStrat,outfile)
    outfile.close()
    
def Analysis(pickled_strategy):

    pck_file = open(pickled_strategy)
    strategy = pickle.load(pck_file)
    analyser = ra.PairTradeAnalyser(strategy,referenceIndex=None)
    SP500 = strategy.market_data.core_data['x']
    indSP = SP500/SP500[0]*100
    indSP.index = pd.to_datetime(indSP.index)
    
    #Print trade summary
    analyser.summary()
    
    #Plot results
    fig = plt.figure()
    ax1= fig.add_subplot(3,1,1)
    ax2 = fig.add_subplot(3,1,2)
    ax3= fig.add_subplot(3,1,3)
   
    strategy.market_data.core_data[['spread','entryUpper','exitUpper','entryLower','exitLower']].plot(ax=ax1)
    ax1.legend().set_visible(False)
    #print strategy.result['Value'].head()
    strategy.result['Value'].plot(ax=ax2)
    pd.DataFrame(indSP).plot(ax=ax2)
    rets = analyser.get_returns()
    #rets.plot(ax=ax3)
    #plt.show()
    
    dd = analyser.draw_downs()
    #print dd['Drawdown']
    ts = - dd['Drawdown']
    ts.plot(ax=ax3)
    plt.show()
    
def SimpleAnalysis(strategy):

    pck_file = open(strategy)
    strategy = pickle.load(pck_file)
    pck_file.close()
    analyser = ra.ResultsAnalyser(strategy,referenceIndex=None)
    
    #Print trade summary
    analyser.summary()

if __name__ == '__main__':
         
    PairTradeSP500( 20 ,  2.56509259,    1.56962963)
    Analysis('pickled_pairs.pkl')
    
    #DeltaHedgeVanillaCallEg()
    #SimpleAnalysis('VanillaCallDelta_strat.pkl')
