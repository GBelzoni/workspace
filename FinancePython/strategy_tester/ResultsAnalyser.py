'''
Created on Jun 23, 2013

@author: phcostello
'''

import pandas as pd

class ResultsAnalyser(object):
    '''
    This class analyses fitted trade strategy object
    '''

    def __init__(self, strategy, referenceIndex = None):
        '''
        Takes a pandas dataframe object with a 'Date' index which should be of type date or datetime
        'Value' column which is timeseries of portfolio value
        'Signal' which is the trade signal
        '''
        self.result = strategy.result
        if referenceIndex != None:
            self.refIndex = strategy.market_data.core_data[referenceIndex]
        else:
            self.refIndex = None

        
    def return_result(self):
        
        return self.result
    
    def get_returns(self,useReference=False):
        
        ''' Calcs returns vs above referenceIndex, if None type then usual returns '''
        
        #data = self.result['Value'][self.result['Value'].notnull()] #Horrible line, but is just filtering out notnull values
        retsPort = pd.DataFrame(self.result['Value'].pct_change())
        
        if useReference == True:
            if self.refIndex == None:
                raise ValueError('No reference index set')
            
            retsRef = self.refIndex.pct_change()
            rets = pd.merge(retsPort,retsRef, left_index=True,right_index=True)
            
        else:
            
            rets = retsPort
            rets['Reference'] = 0
            
        rets.columns = ['Portfolio','Reference']
        
        return rets
        
    def sharpe_ratio(self, useMarketRef=False):
        
        ''' Calcs sharpe ratio vs marketRef, if None then riskfree rate assumed to be 0'''
        
        rets = self.get_returns(useReference=useMarketRef)
        
        #rets = rets.iloc[2:]
        retsOverRef = rets['Portfolio'] - rets['Reference']
        
        sr = rets.mean()/rets.std()
        return sr[0]
    
    def draw_downs(self, percent = False):
        
        '''Calcs timeseries of current percentage drawdown'''
        
        #Calculate percentag Drawdowns 
        value = self.result['Value']
        startt= value.index[0]
        Max = value[startt]
        dd = 0
        startDd = startt
        endDd = startt
        lengthDd = 0
        
        result = [[startt,Max,dd, startDd, endDd, lengthDd]]
        
        for t in value.index:
            
            Max = max(Max,value[t])
            if Max == value[t]:
                startDd = t
                dd = 0
            
            if percent:
                thisDd = (Max - value[t])/Max
            else:
                thisDd = (Max - value[t])
                    
            dd = max(dd, thisDd )
            if not(Max == value[t]):
                endDd = t
            
            lengthDd = startDd - endDd
            
            thisResult = [t,Max,dd, startDd, endDd, lengthDd]
            result.append(thisResult) 
        
        #Format results to dataframe
        columns = ['Time','MaxVal','Drawdown','StartDD','EndDD','LengthDD']
        result = pd.DataFrame(data=result, columns=columns)   
        result.set_index('Time', inplace=True)
        
        return result

    def max_draw_down_magnitude(self, percent = False):
        
        '''Calcs max drawdown'''
        
        dd = self.draw_downs(percent)
            
        maxDD = max(dd['Drawdown'])
        maxDDr = dd[dd['Drawdown'] == maxDD]
        
        return maxDDr.iloc[-1]
    
    def max_draw_down_timelength(self, percent = False):
        
        '''Calcs max drawdown'''
        
        dd = self.draw_downs(percent)
        
        thisDD = dd.iloc[2:] #get rid of non types at start of series
        maxDD = min(thisDD['LengthDD'])
        maxDDr = thisDD[thisDD['LengthDD'] == maxDD]
        return maxDDr.transpose()
 
 
    def summary(self):
        
        '''Calcs summary of Sharpe and max drawdown'''
        
        print "Sharpe Ratio", self.sharpe_ratio()
        print "MaxDrawDown (level)"
        print self.max_draw_down_magnitude()
        print ""
        print "MaxDrawDown (percent)"
        print self.max_draw_down_magnitude(percent = True)
        print ""
        print "MaxDrawDown time (level)"
        print self.max_draw_down_timelength()
        print ""
        print "MaxDrawDown time (percent)"
        print self.max_draw_down_timelength(percent = True)

class PairTradeAnalyser(ResultsAnalyser):
    '''
    This class analyses fitted trade strategy object
    '''
    
    def __init__(self, strategy, referenceIndex):
        '''
        Constructor
        '''
        ResultsAnalyser.__init__(self,strategy, referenceIndex)
        self.yscaling = strategy.market_data.results.params[0]
        self.adfPvalue= strategy.market_data.adfResids()[1]
    
    def summary(self):
            print "Summary for Pair Trade Strategy"
            print "Scaling", self.yscaling
            print "Adf p-value", self.adfPvalue
            print "Sharpe Ratio", self.sharpe_ratio()
            print ""
            print "MaxDrawDown (level)"
            print self.max_draw_down_magnitude()
            print ""
            print "MaxDrawDown (percent)"
            print self.max_draw_down_magnitude(percent = True)
            print ""
            print "MaxDrawDown time (level)"
            print self.max_draw_down_timelength().loc['LengthDD']
            print ""
            print "MaxDrawDown time (percent)"
            print self.max_draw_down_timelength(percent = True).loc['LengthDD']
        
        
        