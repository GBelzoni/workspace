'''
Created on Nov 21, 2012

@author: phcostello
'''
import numpy
import pandas
import matplotlib.pyplot as plt
import rpy2.robjects as ro
from rpy2.robjects.packages import importr

import pandas.io.sql as psql
import sqlite3
import statsmodels.tsa.stattools as sttl
import statsmodels.tsa as tsa

zoo = importr('zoo')


class market_data(object):
#    ...
#    classdocs
#    '''

    def __init__(self, dataOb):
        
        ''' Takes input zoo object and makes data object with pandas Dataframe data object '''
        
        try:
            if isinstance(dataOb, ro.vectors.Matrix) == True:
                names = ro.r.colnames(dataOb)
                time_stamp = zoo.index(dataOb)
                self.core_data = pandas.DataFrame(numpy.array(zoo.coredata(dataOb)), index = time_stamp, columns = names)
            elif isinstance(dataOb, pandas.DataFrame):
                self.core_data = dataOb
            else:
                raise NameError('Error: Not supported object')
            
        except NameError:   
            raise        
                               
       

class simple_ma_md(market_data):
    
    def __init__(self, zooOb, sig_index, short_win, long_win):
        #put check in to see if sig_index is available
        self.sig_index = sig_index
        
        #Construct base class data
        market_data.__init__(self, zooOb)        
        
        
        #Construct Moving Averages
        MAs = pandas.rolling_mean(self.core_data[sig_index], short_win)
        MAl = pandas.rolling_mean(self.core_data[sig_index], long_win)
        
        #Add to data
        self.core_data['MAs'] = MAs
        self.core_data['MAl'] = MAl


class pairs_md(market_data):
    
    def __init__(self, dataOb, xInd, yInd):
        #requires dataOb has two indexes that will be pairs in trade
        #define index in data for pairs trade
        self.xInd = xInd
        self.yInd = yInd
        
        #Construct base class data
        market_data.__init__(self, dataOb)   
        self.results = None
        
    def fitOLS(self):
        #Run OLS and create residual series
        import statsmodels.api as sm
        x = sm.add_constant(self.core_data[self.xInd])
        self.results = sm.OLS(self.core_data[self.yInd],x).fit()
        
    def printSummary(self):
        print self.results.summary()
        
    def adfResids(self):
        
        import statsmodels.api as sm
        resid = self.results.resid
        result = sm.tsa.adfuller(resid)
        return result
        
        
    def generateTradeSigs(self, windowLength, entryScale, exitScale):
        
        resid = self.results.resid
        self.core_data['spread'] = self.results.resid
        self.core_data['entryUpper'] = entryScale*pandas.rolling_std(resid,windowLength,min_periods=10)
        self.core_data['entryLower'] = -entryScale*pandas.rolling_std(resid,windowLength,min_periods=10)
        self.core_data['exitUpper'] = exitScale*pandas.rolling_std(resid,windowLength,min_periods=10)
        self.core_data['exitLower'] = -exitScale*pandas.rolling_std(resid,windowLength,min_periods=10)
    
    def plot_spreadAndSignals(self):
        
        dataLabels = ['spread',
                      'entryUpper',
                      'entryLower',
                      'exitUpper',
                      'exitLower']
                        
        plotData = self.core_data[dataLabels]
        plotData.plot()
        plt.show()
        
        
        
        



    
class market_data_slice(object):
    
    def __init__(self, MD, time_index):
        #check type
        self.time_index = time_index
        self.data = MD.core_data.ix[time_index]
        self.time_stamp = MD.core_data.index[time_index]
        
        #variable to control how long till next period. Used to inflate cash trades
        self.period_length = 1 
    
        
    def set_period_length(self, period_length):
               
        self.period_length = period_length 
        
        

        

if __name__ == '__main__':
    
    def test_pairs_md():
    #prepare data
        import DataHandler.DBReader as dbr
        dbpath = "/home/phcostello/Documents/Data/FinanceData.sqlite"
        dbreader = dbr.DBReader(dbpath)
        SP500 = dbreader.readSeries("SP500")
        BA = dbreader.readSeries("BA")
        dim = 'Adj_Close'
        SP500AdCl = SP500[dim]
        BAAdCl = BA[dim]
        dataObj = pandas.merge(pandas.DataFrame(BAAdCl), pandas.DataFrame(SP500AdCl), how='inner',left_index = True, right_index = True)
        dataObj.columns = ['y','x']
        
        pmd = pairs_md(dataOb=dataObj,xInd='x',yInd='y')
        pmd.fitOLS()
#        resid = pmd.results.resid
#        resid.plot()
#        rllstd = pandas.rolling_std(resid,100,min_periods=10)
#        rllstd.plot()
#        plt.show()
        
        
        pmd.printSummary()
        print pmd.adfResids()
        pmd.generateTradeSigs(50, entryScale=1.5, exitScale=0)
        pmd.plot_spreadAndSignals()
        
        
    test_pairs_md()
    
    
        