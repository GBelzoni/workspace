'''
Created on Jun 13, 2013

@author: phcostello
'''
import unittest
import DataHandler.DataDownloader as dd
import pandas as pd


class Test_DataDownLoader(unittest.TestCase):


    def setUp(self):
        
        conString = "/home/phcostello/Documents/Data/FinanceData.sqlite"
        self.data_downloader = dd.DataDownloader(conString)
        self.verbose = True
        
    def test_construction(self):
        
        listSeries = self.data_downloader.seriesList
        self.assertIsInstance(listSeries, pd.core.frame.DataFrame)
    
    def tearDown(self):
        pass

    def test_connect(self):
        
        if self.verbose:
            print "test_connect"
        
        self.data_downloader.connect()
        
    def test_listTypes(self):
        
        self.assertGreater(len(self.data_downloader.listTypes()), 0.0,'Length of types > 0') 
        
    def test_listSeries(self):
        
        if self.verbose:
            print "test_listSeries"
            print self.data_downloader.listSeries()
            
    
    def test_infoType(self):
        ### Returns info corresponding to all of a given seriesType ###
        
        if self.verbose:
            infoType = self.data_downloader.infoType('index')
            print "test_infoType"
            print infoType
            
    def test_infoSeries(self):
        
        dd = self.data_downloader
        seriesList = dd.listSeries()
        infoSeries = dd.infoSeries(seriesList)
        
        if self.verbose:
            print "test_infoSeries"    
            print infoSeries
                
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()