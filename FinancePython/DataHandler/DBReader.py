'''
Created on Jun 19, 2013

@author: phcostello
'''
from DataHandlerBase import DataHandlerBase
import pandas.io.sql as psql
import pandas as pd

class DBReader(DataHandlerBase):
    '''
    Simple class to read series from db
    '''

    def readSeries(self, seriesName):
        ''' Just reads data from db ''' 

        self.connect()
        sql = "SELECT * FROM {}".format(seriesName)
        try:
            data = psql.read_frame(sql, self.con)
        except Exception as e:
            print "Problem reading {0}, error is {1}".format(seriesName,e)
        
        try:
            data = data.set_index('Date') #Set date index
        except Exception as e:
            print "Problem setting date index in series {0}, error is {1}".format(seriesName,e)   
        
        try:
            data.index = pd.to_datetime(data.index)
            return data
        except Exception as e:
            print "Problem converting date index using pd.to_datetime in series {0}, error is {1}".format(seriesName,e)   
        
        