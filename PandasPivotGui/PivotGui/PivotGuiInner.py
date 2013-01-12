'''
Created on Jan 12, 2013

@author: phcostello
'''


import sys
import pandas as pd
from PyQt4 import QtCore, QtGui
from pivotTableTemplate import Ui_Dialog
from twisted import names

class PivotGuiInner(object):
    
    ''' Base Pivot State Object - inherited depends on data processor '''
    
    def __init__(self):           
        
        #Labels
        self.fieldLabels = []
        self.columnLabels = []
        self.rowLabels = []
        self.valueLabels = []
        
        #Input data to pivot
        self.data = None
        
        #Input output PivotTable
        self.PTresult = None
    
    def getData(self):
        '''To be implemented in inherited class'''
        pass
    
    def setState(self):
        '''To be implemented in inherited class'''
        pass
    
    def makePT(self):
        '''To be implemented in inherited class'''
        pass    
    
    def makePTstr(self):
        '''To be implemented in inherited class'''
        pass    


class PandasPivotGuiInner(PivotGuiInner):
    
    def getData(self,data):
        '''Import pandas pivot table'''
        try:
            if(isinstance(data, pd.core.frame.DataFrame) == False):
                raise NameError('data not Dataframe')

        except NameError:
            raise
        
        self.data = data
        
    def setState(self):
        
        self.fieldLabels = list(self.data.columns.values)
        
        
    def makePT(self):
        '''Create Pivot Table from Inner state'''
    
        cols = self.columnLabels
        rows = self.rowLabels
        values = self.valueLabels
        if (len(rows) == 0) or (len(values) == 0):
            return "you need some rows and values to pivot"
        else:
            result = self.data.pivot_table( rows = rows, 
                                        cols = cols,
                                        values = values) 
            return result
    
    def makePTstr(self):
        
        '''Create Pivot Table from Inner state'''
    
        cols = self.columnLabels
        rows = self.rowLabels
        values = self.valueLabels
        if (len(rows) == 0) or (len(values) == 0):
            return "you need some rows and values to pivot"
        else:
            
        #return data variable as name
#        dataStr = ''
#        ptSubStr1 = '.pivot_table(' + ' rows = '  + str(rows) 
#        + ', cols = ' + str(cols) + ', values =' + str(values) + ')' 
#        
            return 1     
    
  
def main():
    
    df = pd.DataFrame({'a': 2*'a' ,'b' : 2*'b' , 'c' :[1,1]})
    print df
    pg = PandasPivotGuiInner()
    pg.getData(df)
    pg.setState()
    pt = df.pivot_table(rows = 'a' , values = 'c')
    pt = pg.makePT()
    print pt
    pg.rowLabels = 'a'
    pt = pg.makePT()
    print pt
    pg.valueLabels = 'c'
    pt = pg.makePT()
    print  pt
    

if __name__ == '__main__':
    main()