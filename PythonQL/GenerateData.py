'''
Created on Dec 13, 2012

@author: phcostello
'''

import numpy as np
import pandas as pd
import math
import random

class GenerateData(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.data = np.array([])
        
        
    def get_data(self):
        
        return self.data


class GenerateLogNormalTS(GenerateData):
    
        def __init__(self, S0, mu, covariance, stepsize, steps):
            
            GenerateData.__init__(self)
            
            self.S0 = S0
            self.mu = mu
            self.covariance = covariance
            self.stepsize = stepsize
            self.steps = steps
            #generate 10k lognormal samples with mean=0 and stddev=1
            samples = [random.normalvariate(0,1) for r in xrange(steps)]
            S = S0
            self.data =[S]
            for val in samples:
                S += S*(mu*stepsize+ covariance*math.sqrt(stepsize)*val)
                self.data.append(S)  

class GenerateNormalTS(GenerateData):
    
        def __init__(self, S0, mu, covariance, stepsize, steps):
            
            GenerateData.__init__(self)
            
            self.S0 = S0
            self.mu = mu
            self.covariance = covariance
            self.stepsize = stepsize
            self.steps = steps
            #generate 10k lognormal samples with mean=0 and stddev=1
            samples = [random.normalvariate(0,1) for r in xrange(steps)]
            S = S0
            self.data =[S]
            for val in samples:
                S += (mu*stepsize+ covariance*math.sqrt(stepsize)*val)
                self.data.append(S)