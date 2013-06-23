'''
Created on Jun 20, 2013

@author: phcostello
'''
import unittest
import DataHandler.DBReader as dr
import sqlite3

import pandas as pd


class Test_DBReader(unittest.TestCase):


    def setUp(self):
        
        conString = "/home/phcostello/Documents/Data/FinanceData.sqlite"
        self.data_reader = dr.DBReader(conString)
        self.verbose = True
        
    def test_construction(self):
        
        listSeries = self.data_reader.seriesList
        self.assertIsInstance(listSeries, pd.core.frame.DataFrame,msg="listSeries is empty")

    def test_ReadingDB(self):
        
        seriesName = 'All_Ordinaries'
        data = self.data_reader.readSeries(seriesName)
        self.assertIsInstance(data, pd.core.frame.DataFrame,msg="Couldn't download All_Ordinaries is empty")
        seriesNameJunk = 'blahblah'
        self.assertRaises(sqlite3.OperationalError, self.data_reader.readSeries(seriesNameJunk))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()