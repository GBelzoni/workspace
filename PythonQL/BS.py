'''
Created on Dec 17, 2012

@author: phcostello
'''
#
#class MyClass(object):
#    '''
#    classdocs
#    '''
#
#
#    def __init__(selfparams):
#        '''
#        Constructor
#        '''


import strategy_tester.market_data as md
import GenerateData as gd
import matplotlib.pyplot as plt
import pandas as pd

paths = [ gd.GenerateLogNormalTS(100, 0.05, 0.1, 100).get_data() for i in range(0,100)]

path1 = gd.GenerateLogNormalTS(100, 0.05, 0.1, 100).get_data()

path1 = pd.DataFrame(path1)

md1 = md.market_data(path1)

#[plt.plot(path) for path in paths ]
#plt.show()


   
