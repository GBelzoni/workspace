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

    def __init__(self, zooOb):
        
### Takes input zoo object and makes data object with pandas Dataframe data object ###
        
        try:
            if isinstance(zooOb, ro.vectors.Matrix) == True:
                names = ro.r.colnames(zooOb)
                time_stamp = zoo.index(zooOb)
                self.core_data = pandas.DataFrame(numpy.array(zoo.coredata(zooOb)), index = time_stamp, columns = names)
                self.time_stamp = time_stamp
                self.names =  names
            elif isinstance(zooOb, pandas.DataFrame):
                self.core_data = zooOb
                self.time_stamp = zooOb.index
                self.names = list(zooOb.columns)
            else:
                raise NameError('Error: Not supported object')
            #self.length = self.core_data.
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
        

        