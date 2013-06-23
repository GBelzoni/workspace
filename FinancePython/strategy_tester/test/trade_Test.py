'''
Created on Dec 8, 2012

@author: phcostello
'''
import unittest
import numpy as np
import pandas as pd
import GenerateData as gd
import strategy_tester.market_data as md
import strategy_tester.trade as td



class Test(unittest.TestCase):


    def setUp(self):
        #setup market data#
        #First setup data as list
        data = np.array([1,0.05,100,0.1])
        data.resize(1,4)
        
        #Then converst to types needed for pricing
        columns = ["zero",
                   "rate",
                   "underlying",
                   "vol"]
        
        data = pd.DataFrame(data, columns = columns)
        md_cash = md.market_data(data)

        #need to add to self to use in test functions
        self.md_slice = md.market_data_slice(md_cash,time_index=0)
        


    def tearDown(self):
        pass


    def test_cash(self):
        
        
        md_slice = self.md_slice
                
        #setup cash trades to test
        Cash_Trade = td.TradeCash("TestCash", notional=100)
        
        
        #Do tests
        self.assertEqual(Cash_Trade.price(),1)
        self.assertEqual(Cash_Trade.value(),100)
        
        Cash_Trade.inflate(md_slice)
        print Cash_Trade.notional
        

    def test_equity(self):
        md_slice = self.md_slice
                
        #setup cash trades to test
        Equity_Trade = td.TradeEquity("TestEquity", notional=100,price_series_label="underlying")
        self.assertEqual( Equity_Trade.price(md_slice),100)
        
    def test_vanilla_euro_call(self):
        md_slice = self.md_slice
        
        #setup trades
        # Strik = 105
        # Underlying = 100
        # 12m expiry
        # vol = 10%
        # dividend =0 
        # risk free = 0.05
        # val = $4.046
        
        Vanilla_Euro_call = td.TradeVanillaEuroCall("TestEuroCall",
                                                     notional=100, 
                                                     strike=105, 
                                                     expiry=1)
        
        self.assertTrue(round(Vanilla_Euro_call.price(md_slice),3),4.046)

        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()