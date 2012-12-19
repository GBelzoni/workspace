'''
Created on Nov 21, 2012

@author: phcostello
'''
import numpy
import pandas
import rpy2.robjects as ro
from rpy2.robjects.packages import importr

zoo = importr('zoo')

class market_data(object):
#    ...
#    classdocs
#    '''

    def __init__(self, dataOb):
        
### Takes input zoo object and makes data object with pandas Dataframe data object ###
        
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
        