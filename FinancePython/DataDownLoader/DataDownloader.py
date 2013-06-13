'''
Created on Jun 13, 2013

@author: phcostello
'''

import pandas as pd
import datetime

#we want fx, yahoo_equity, yahoo_index, qandl_futures

#We want list of:
#data type
#indexes
#index constituents
#fx series
#futures series
#options


#Get info
#What indexes are there
#All series, with type, source, range
#by series type
#by index

#Update functionality
#set series to update,
#by index
#by series
#by type

#Add series

#Read functionality

#Update functionality
#set series to update,
#by index
#by series
#by type

#We want to have lists of indexes
#list of series, type
#list of data range for each 
import pandas as pd
from pandas.io.data import DataReader
from datetime import datetime

import sqlite3 
import pandas.io.sql as psql
import logging
from compiler.ast import Continue



t = datetime.now()
print datetime.date(t)

class DataDownloader(object):
    '''
    Class to manage finance data
    '''

    def __init__(self,conString):
        '''
        Constructor - takes connection string to dataBase
        '''
        self.conString = conString
        self.con = None
        self.seriesList = self.__getAllSeriesInfo()
        
    
    def connect(self): 
        ### connect to the constring data member ###
        
        
        
        try:
            self.con = sqlite3.connect( self.conString, detect_types=sqlite3.PARSE_DECLTYPES)
            cur = self.con.cursor()    
            cur.execute('SELECT * FROM SeriesList')
            data = cur.fetchone()
                            
    
        except sqlite3.OperationalError, e:
    
                print "DataDownloader.connect failed. Couldn't find 'SeriesList'"
                print "Error %s:" % e.args[0]
                
            
        
    def disconnect(self):
        
        ### disconnect from the db ###
        self.con.close()
       
    def __getAllSeriesInfo(self):
        
        ### pandas dataframe with Info of all data in db ###
        ###
        ### Retrieved columns are:
        ### SeriesName      
        ### LookupTicker    
        ### Type            
        ### Index           
        ### Source          
        ### StartRange      
        ### EndRange        
        ### Frequency       
        
        series_table_name = "SeriesList"
        sqlTxt = "SELECT * FROM {0}".format(series_table_name)
        
        self.connect()
        info = psql.read_frame(sqlTxt, self.con)
        self.disconnect()
        
        return info
        
    def infoType(self, seriesType):
        ### Returns info corresponding to all of a given seriesType ###
        
        infoType = self.seriesList[self.seriesList['Type']==seriesType]
        
        if len(infoType) == 0:
            print 'DataDownloader.infoType: return list length =0. Check if seriesType {0} exists'.format(seriesType)
        
        return infoType
    
    def infoSeries(self,seriesList):
        
        seriesInfo = self.seriesList.set_index(keys='SeriesName',drop=False) #make Series name index so can be subsetted on
        seriesInfo = seriesInfo.loc[seriesList] #Return the queried rows
        seriesInfo.reset_index(drop=True , inplace=True)
        return seriesInfo
    
    def listTypes(self):
        
        types = set(self.seriesList['Type'])
        return types
    
    def listSeries(self):
        
        return self.seriesList['SeriesName']
    
    def updateRangeInfo(self,seriesNames, logfile = None):
        
        errortables = []
        
        if logfile !=None:
            logging.basicConfig(filename= logfile, filemode='w', level = logging.ERROR)
        
        
        self.connect()
        
        for name in seriesNames:
            
            logging.info("updateRangeInfo for {}".format(name))
            sqlRead = "SELECT Date FROM {0}".format(name)
            
            
            #Read series data range
            try:
                dates = psql.read_frame(sqlRead, 
                                       con = self.con
                                       )
            except Exception as e:
                errortables.append(name)
                logging.error("updateRangeInfo: Reading table, encountered error <<{0}>>".format(e))
                continue
               
               
            #Convert to datetime objects
            dates = dates.apply(pd.to_datetime)
            StartRange = dates.min().iloc[0] #still series object so have to get data
            EndRange = dates.max().iloc[0]
            
            #Construct sql update query
            sqlWrite = "UPDATE SeriesList SET StartRange = '{0}', ".format(StartRange)
            sqlWrite += "EndRange = '{0}' ".format(EndRange)
            sqlWrite += "WHERE SeriesName = '{0}';".format(name)
            
            #print sqlWrite
            
            cur = self.con.cursor()
            
            try:
                cur.execute(sqlWrite)
            
            except Exception as e:
                logging.error("updateRangeInfo: Error executing write dates, encountered error <<{0}>>".format(e))
                errortables.append(name)
                continue
            
            else:     
                self.con.commit()
                
            
        self.disconnect()
        return errortables
        
    def updateSeriesData(self,seriesNames, maxDate = None, logfile = None):
        
#        start = datetime(2010,1,1)
#        end = datetime.date(datetime.now())
#    
        errortables = []
        
        if logfile !=None:
            logging.basicConfig(filename= logfile, filemode='w', level = logging.ERROR)
        
        #Get info for series
        info = self.infoSeries(seriesNames)
        
        #Connect to db
        self.connect()
        
        for series in info.iterrows():
            
            #Read relevant info
            series = series[1]
            endDate = pd.to_datetime(series['EndRange'])
            seriesName = series['SeriesName']
            lookupTicker = series['LookupTicker']
            source = series['Source']
            
            #add logging message
            logging.info("updateData for {0}".format(seriesName))
            
            #Update Tables that have are less than maxDate
            if endDate >= maxDate :
                logging.info("Table {0} already up to date".format(seriesName))
                
            else:
                try:
                    data = self.readData(lookupTicker, source, endDate+1, maxDate)
                except:
                    errortables.append[seriesName]
                    continue
                try:
                    self.writeFrameToDB(data, seriesName)
                except:
                    errortables.append[seriesName]
                    continue
                
        self.disconnect()
       
        return errortables
        
        
    def readData(self, lookupTicker, source, start, end):
        
        #Read the data
        try:  
            data = DataReader(lookupTicker, source , start, end)
            data = data.reset_index()
            logging.info("Read ticker {}".format(lookupTicker))
        except:
            logging.error("importData: Can't read ticker {}".format(lookupTicker))
            raise
        else:
            return data
        
    def writeFrameToDB(self, df, SeriesName):
        
        #Write to db
        try:
            self.connect()
            psql.write_frame( df, SeriesName, self.con, if_exists='append')
            self.con.commit()
            logging.info("Wrote series ()".format(SeriesName))
        except:
            logging.error("Problems with {}".format(SeriesName))
            raise
        finally:
            self.disconnect()
    
        
    def update(self, series_list):
        pass
        
  
if __name__ == "__main__":
    
    conString = "/home/phcostello/Documents/Data/FinanceData.sqlite"
    dd = DataDownloader(conString)
    
    #dd.updateRangeInfo(['HANG_SENG_INDEXx','All_Ordinaries'])#,logfile='log_range_update.txt')
    
    #dd.updateSeriesData(['HANG_SENG_INDEX'])
    
    start = datetime(2013,2,21)
    end = datetime.date(datetime.now())
    
    data = dd.readData('^AORD', 'yahoo', start, end)
    print data
    dd.writeFrameToDB(data, SeriesName='All_Ordinaries')
    
    import pandas as pd    
    l1 = ['a','b','c','h','i']
    l2 = ['a','b','c','d','e']
    df = pd.DataFrame(zip(l1,l2))
    
    df.set_index(keys=0,drop=False,inplace=True)
    df.reset_index( drop=True)



        