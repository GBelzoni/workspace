'''
Created on Dec 8, 2012

@author: phcostello
'''
import unittest
import time

class Test(unittest.TestCase):

    def setUp(self):
        
        import strategy_tester.market_data as md
        import strategy_tester.trade as td
        import strategy_tester.Portfolio as pt
        import strategy_tester.TradeStrategyClasses as tsc
        
        import rpy2.robjects as ro
        from rpy2.robjects.packages import importr
        zoo = importr('zoo')
              
        #Create moving average market data type
        AORD = ro.r('read.table("~/Documents/R/StrategyTester/Data/AORD.csv",header=T, sep=",")')
        AORD = zoo.as_zoo(AORD)#, order_by = ro.r.rownames(AORD))
        MAD1 = md.simple_ma_md(AORD,'AORD.Close', 10, 20)
        
        #Create empty cash trade
        trade_cash =td.Trade("Cash","Cash", 0)
        #Setup empty cash portfolio
        port1 = pt.Portfolio("port1")
        port1.add_trade(trade_cash)
        [td.name for td in port1.trades]
        
        #Setup MA trade Strategy
        #Note have checked that time 58 will have 'buy' signal
        self.trade_strat = tsc.MA_Trade_Strategy(MAD1,port1,59)
        
        
    def tearDown(self):
        pass


    def test_upd_signal(self):
        #Have manually gone through data AORD and found out where first buy is at
        self.assertTrue(self.trade_strat.upd_signal() == 'buy')

    def tes_upd_portfolio(self):
        
        #Test buy check that adds trade and that notional is updated
        
        #Test sell check that adds trade and that notional is updated
        pass
        
    
    def test_run_strategy(self):
        
        start_time = time.clock()
        self.trade_strat.run_strategy()
        print time.clock() - start_time, "seconds"
        print self.trade_strat.result
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()