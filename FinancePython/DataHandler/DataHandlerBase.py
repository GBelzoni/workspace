'''
Created on Jun 20, 2013

@author: phcostello
'''


import sqlite3 
import pandas.io.sql as psql


class DataHandlerBase(object):
    '''
    Base class for interacting with finance database
    Has constructor and db connect/disconnect funtions
    Has general info retrieval about the db functions 
    '''

    def __init__(self,conString):
        """ Constructor - takes path_string to location of database """
        self.conString = conString
        self.con = None
        self.seriesList = self.__getAllSeriesInfo()
        self.quandlAuthToken = 'ai3HEfkXjxkuhLzdn2n8'
    
    def connect(self): 
        ''' connect to the constring data member '''
       
        try:
            self.con = sqlite3.connect( self.conString, detect_types=sqlite3.PARSE_DECLTYPES)
            cur = self.con.cursor()    
            cur.execute('SELECT * FROM SeriesList')
            data = cur.fetchone()
                            
    
        except sqlite3.OperationalError, e:
    
                print "DataDownloader.connect failed. Couldn't find 'SeriesList'"
                print "Error %s:" % e.args[0]
        
    def disconnect(self):
        
        ''' disconnect from the db '''
        self.con.close()
       
    def __getAllSeriesInfo(self):
        
        """Internal function read in db info to class data member,
        Info in db is in table SeriesList
        """
        
        series_table_name = "SeriesList"
        sqlTxt = "SELECT * FROM {0}".format(series_table_name)
        self.connect()
        info = psql.read_frame(sqlTxt, self.con)
        self.disconnect()
        
        return info
        
    def infoType(self, seriesType):
        ''' Returns db info corresponding to all of a given seriesType '''
        
        infoType = self.seriesList[self.seriesList['Type']==seriesType]
        
        if len(infoType) == 0:
            print 'DataDownloader.infoType: return list length =0. Check if seriesType {0} exists'.format(seriesType)
        
        return infoType
    
    def infoSeries(self,seriesList):
        '''Returns db info for series in list. Make sure arg is a list even in case of one series '''
        seriesInfo = self.seriesList.set_index(keys='SeriesName',drop=False) #make Series name index so can be subsetted on
        seriesInfo = seriesInfo.loc[seriesList] #Return the queried rows
        seriesInfo.reset_index(drop=True , inplace=True)
        return seriesInfo
    
    def listTypes(self):
        '''Returns the existing types of series currently in db''' 
        types = set(self.seriesList['Type'])
        return types
    
    def listSeries(self):
        '''Returns existing series currently in db. Good for checking if doubling up'''
        return set(self.seriesList['SeriesName'])
        