'''
Created on Dec 8, 2012

@author: phcostello
'''
import unittest

import strategy_tester.trade as td
import strategy_tester.market_data as md
import strategy_tester.Portfolio as pf
import numpy as np
import pandas as pd
from strategy_tester.Portfolio import PortfolioError


class Test(unittest.TestCase):


    def setUp(self):
       
        r = 0.05
        vol = 0.1
        S = 100.0
        
         
        #setup market data#
        #First setup data as list
        data = np.array([r,S,vol])
        data.resize(1,3)
        
        #Then convert to types needed for pricing
        columns = ["rate",
                   "underlying",
                   "vol"]
        
        
        data = pd.DataFrame(data, columns = columns)
        self.md1 = md.market_data(data)
    
        #need to add to self to use in test functions
        self.md_slice = md.market_data_slice(self.md1,time_index=0)
        
        #Setup vanilla option trade
        self.tradeCall = td.TradeVanillaEuroCall(name = "Call",
                                            notional = 0,
                                            strike = 100,
                                            expiry = 0.5)
        #Setup portfolio
        self.tradeEquity = td.TradeEquity(name = "Equity", 
                                     notional = 0, 
                                     price_series_label = "underlying")
        
        
        self.port1 = pf.Portfolio("port1")
        
        
    
   

    def tearDown(self):
        pass


    def test_fixed_toggle(self):
        
        port1 = self.port1
        trade = self.tradeEquity
        
        #Fix trades then try adding trade - should raise exception
        port1.fixed_toggle()
        self.assertRaises(PortfolioError,port1.add_trade, trade)
        
        #Call fixed_toggle and add trade, should work
        port1.fixed_toggle()
        port1.add_trade(trade)
        self.assertEqual(len(port1.trades), 2)
        
    def test_adjustNotional(self):
        
        print "adjustNotional Test"
        port1 = self.port1
        trade = self.tradeEquity
        
        #add equity trade type to portfolio
        port1.add_trade(trade)
        print port1.get_notional()
        
        #adjust equity type so that we have 1 share
        trades = {'Equity':100}
        port1.adjustNotional(trades)
        print port1.get_notional()
        self.assertTrue( port1.get_notional() == [0,100])
        
    def test_adjustCash(self):
        
        print "adjust_cash test"
        port = self.port1
        trade = self.tradeEquity
        tradeCall = self.tradeCall
        
        portSlice = pf.PortfolioSlice(self.port1, self.md1, time_index=0)
        print portSlice.value()
        #add equity trade type to portfolio
        port.add_trade(trade)
        port.add_trade(tradeCall)
        print portSlice.value()
        
        #Change notional on equity by 1, i.e. we bought a share
        trades = {'Equity':1}
        port.adjustNotional(trades)
        print portSlice.value()
        portSlice.adjustCash(trades)
        print portSlice.value()
        
        trades = {'Equity': 2,
                  'Call': -3}
        
        port.adjustNotional(trades)
        portSlice.adjustCash(trades)
        print portSlice.value()
       

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()