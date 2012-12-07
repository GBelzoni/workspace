'''
Created on Nov 30, 2012

@author: phcostello
'''

import strategy_tester.market_data as md
import strategy_tester.Portfolio as port


class trade_strategy(object):
    '''
    classdocs
    '''


    def __init__(self, portfolio, market_data, initial_time_index):
        '''
        Constructor
        '''
        ### object combines portfolio and marketdata with updating strategy """
        self.portfolio = portfolio
        self.market_data = market_data
        self.time = initial_time_index
        self.results = []
        
    def upd_sig(self):
        pass
    
    def run_strategy(self):
        pass
    
class ewma_crossover_strategy(trade_strategy):
    def upd_sig(self):
        time = self.time
        md = self.market_data
        pf = self.portfolio
        data0 = port.PortfolioSlice(pf, md, time-1).md_slice.data
        data1 = port.PortfolioSlice(pf, md, time).md_slice.data
                
        #Previous Moving average vals
        mas0 = data0["MAs"]
        mal0 = data0["MAl"]
        #Current MA vals
        mas1 = data1["MAs"]
        mal1 = data1["MAl"]
        
        #Check if there is an upcrossing this step
        if( ( mas0 < mal0 ) and ( mas1 > mal1 ) ):
            signal = "buy"
        elif ( ( mas0 > mal0 ) and ( mas1 < mal1 )):
            signal = "sell"
        else:
            signal = "hold"
        
        return(signal)
     
        
        