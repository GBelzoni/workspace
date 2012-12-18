'''
Created on Dec 7, 2012

@author: phcostello
'''
import unittest
from strategy_tester.market_data import market_data
from strategy_tester.market_data import *
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
zoo = importr('zoo')
import pandas  


class MarketDataTest(unittest.TestCase):

    def setUp(self):
        #unittest.TestCase.setUp(self)
          
        #Setup
        
        self.AORD = ro.r('read.table("~/Documents/R/StrategyTester/Data/AORD.csv",header=T, sep=",")')
        self.zooData = zoo.zoo(self.AORD)        
        self.AORDcsv = pandas.read_csv("/home/phcostello/Documents/R/StrategyTester/Data/AORD.csv",parse_dates=True)
        
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)    
        
    def test_MD_zoo_constructor(self):
        #Make sure that not constructing from allowable type throws error
        with self.assertRaises(NameError):
            market_data(self.AORD)
      
    def test_MD_readcsv_constructor(self):
        
         #Make sure that not constructing from allowable type throws error
        with self.assertRaises(NameError):
            market_data(self.AORD)
            
         
            
    def test_MD_simpleMovingAverage_constructor(self):
        # Test that non zoo data throws
        with self.assertRaises(NameError):
            simple_ma_md(self.AORD,'AORD.Close', 10, 20)
        
        #Test the moving averages are contructed with length >= 1
        md_moving_average = simple_ma_md(self.zooData, 'AORD.Close',10, 20)
        lenS = len(md_moving_average.core_data['MAs'])
        lenL = len(md_moving_average.core_data['MAl'])
        self.assertGreater(lenS, 1, 'Short MA has length <=1')
        self.assertGreater(lenL, 1, 'Long MA has length <=1')         
    
        

    def testMADSlice(self):
        #Check slicing is working for MAD
        MD = simple_ma_md(self.zooData, 'AORD.Close',10, 20)
        MADSlice = market_data_slice(MD,20)
        malval = round(MADSlice.data['MAl'],3)
        masval = round(MADSlice.data['MAs'],3)
        areMAcorrect = malval == 5636.895 and masval == 5699.72
        #print "Vals = ", masval, malval #and MADSlice.data['MAs'] == 5713.830
        self.assertTrue(areMAcorrect, 'MA have incorrect values for time = 20')
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()