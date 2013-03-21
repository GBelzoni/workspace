'''
Created on Mar 21, 2013

@author: phcostello
'''

class TestStrategy(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.market_data = None
        self.initial_portfolio = None
        self.training_dates = None
        self.test_dates = None
        self.parameters = None
        self.trained_parameters = None
        self.trained_strategy = None
        self.test_strategy = None
    
    def run_strategy(self, params0, dateRange):
        #returns strategy
        pass
    
    def train_model(self,dateRange):
        #returns optimised strategy
        pass
    
    def test_model(self,dateRange):
        #runs trained parameters on test data
        
    
    