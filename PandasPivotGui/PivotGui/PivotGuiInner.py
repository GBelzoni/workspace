'''
Created on Jan 12, 2013

@author: phcostello
'''


import sys
import pandas as pd
from PyQt4 import QtCore, QtGui
from pivotTableTemplate import Ui_Dialog
from twisted import names
from ubuntu_sso.utils.txsecrets import Item

class PivotGuiInner(object):
    
    ''' Base Pivot State Object - inherited depends on data processor '''
    
    def __init__(self):           
        
        #Labels
        self.fieldLabels = []
        self.columnLabels = []
        self.rowLabels = []
        self.valueLabels = []
        
        #Items to filter
        self.itemLabels = []
        
        #Filters
        self.filterField = None
        self.filters = {}
        
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

    def getItems(self):
    
        pass
    
class PandasPivotGuiInner(PivotGuiInner):
    
    def __init__(self):
        
        PivotGuiInner.__init__(self)
        
        self.data = pd.DataFrame()
        
        
    
    
    
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
        
        
    def makePT(self, aggfunc = sum, margins = False):
        '''Create Pivot Table from Inner state'''
        
        cols = self.columnLabels
        rows = self.rowLabels
        values = self.valueLabels
        
        
        
        if (len(rows) == 0) or (len(values) == 0):
            return "you need some rows and values to pivot"
        
        #Filter frame by filters
        filteredFrame = self.data
        
        
        for fil in self.filters.items():
            #print fil
            key = fil[0][0]
            listfil = fil[1]
            ffilter = filteredFrame[key].isin(listfil)
            filteredFrame = filteredFrame[ffilter]

        
        
        result = filteredFrame.pivot_table( rows = rows, 
                                        cols = cols,
                                        values = values, 
                                        aggfunc = aggfunc,
                                        margins = margins) 
        self.PTresult = result
        
        
    
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
    
    
    def getFields(self):
        '''Funtion to get list of field when initialising '''
        
        return self.data.columns.tolist()
    
    def getItems(self, fieldLabel):
        ''' get list of items given string label of field'''
        self.itemLabels = self.data[fieldLabel].unique().tolist() #[str(it) for it in self.data[fieldLabel].unique().tolist()]       
        
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
    pass
    #main()