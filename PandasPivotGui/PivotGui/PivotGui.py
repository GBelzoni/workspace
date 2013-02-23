'''
Created on Jan 12, 2013

@author: phcostello
'''

import sys
import pandas as pd
import numpy as np
from PyQt4 import QtCore, QtGui
from pivotTableTemplate import Ui_Dialog
import PivotGuiInner
from pydoc import gui




'This Module connect the GUIInner state to the GUI window and handles events'

class MyDialog(QtGui.QMainWindow):
    
    def __init__(self):
        
        #Call my dialog parent constructor
        super(MyDialog, self).__init__()
        
        #Call template generated from qtdesigner
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        #Add inner state variable
        self.state = PivotGuiInner.PandasPivotGuiInner()
        
        #Start gui
        self.show()
     
    def listFieldKeyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            #here accept the event and do something
            
            keys = { 'r': 82,
                    'c': 67,
                    'v': 86,
                    'uarrow': 16777235,
                    'darrow': 16777237}
            
            #up key
            if event.key() == 82:
                
                #Clone selected item
                it = self.ui.listFields.currentItem().clone()
                #Add to rows
                self.ui.listRows.addItem(it)    
            
            if event.key() == 67:
                
                #Clone selected item
                it = self.ui.listFields.currentItem().clone()
                #Add to rows
                self.ui.listCols.addItem(it)     
                
            if event.key() == 86:
                
                #Clone selected item
                it = self.ui.listFields.currentItem().clone()
                #Add to rows
                self.ui.listValues.addItem(it)     
                
                    
            print event.key()
            event.accept()
            self.updateState()
            pt = self.state.makePT()
            print pt
            
            lists = [self.state.rowLabels,
                     self.state.columnLabels,
                     self.state.valueLabels]
            
            print lists
        else:
            event.ignore()
            
    
    
    def clearFilter(self):
        
        self.ui.listFields.clear()
        self.ui.listCols.clear()
        self.ui.listRows.clear()
        self.ui.listValues.clear()
        
        self.updateState()
    
    def updateFilter(self, listType, listLabels):
            
            listType.clear()
            
            for item in listLabels:
                item = QtGui.QListWidgetItem(str(item) )
                listType.addItem(item)
    
    
    def initialise(self):
        
        '''updates Gui to reflect the internal state of the pt'''
        
        self.clearFilter()
        #Update the filter fields
        
        fields = self.state.getFields() 
        self.updateFilter( self.ui.listFields, fields ) #This is using pandas
        self.updateState()
        
        #Set filters to be all items in all fields
        for fld in self.state.fieldLabels:
            
            self.state.getItems(fld)
            self.state.filters[(fld, 'All')] = self.state.itemLabels
        
           
    def updateState(self):
        '''Updates internal state to reflect GUI'''
        
        list = self.ui.listFields
        self.state.fieldLabels = [str(list.item(j).text()) for j in range(0,len(list))]
        
        list = self.ui.listRows
        self.state.rowLabels  = [str(list.item(j).text()) for j in range(0,len(list))]
        
        list = self.ui.listCols
        self.state.columnLabels  = [str(list.item(j).text()) for j in range(0,len(list))]
        
        list = self.ui.listValues
        self.state.valueLabels  = [str(list.item(j).text()) for j in range(0,len(list))]
        
#        list = self.ui.listFilters
#        self.state.itemLabels  = [str(list.item(j).text()) for j in range(0,len(list))]
        
        
    def updateFilters( self, item ):
        
        ''' Takes an item that is activated in lists and displays itemField '''
        itLabel = str(item.text())
        self.state.getItems(itLabel)
        self.updateFilter( self.ui.listFilters , self.state.itemLabels)
        
        #to keep track of which field selection will respond to
        self.state.filterField = itLabel
        
        
        x = self.ui.listFilters.item(0)
   
        #Highlight the current filter fields
        
        
    def createFilter(self):
        
        ''' Creates list of items from selected filter fields and saves to dict of filters with key (fieldname, filtername)'''
        filterItems = [str(it.text()) for it in self.ui.listFilters.selectedItems()]
        filterItems = np.array(filterItems)
        filterLabel = self.ui.FilterName.toPlainText()
        filterField = self.state.filterField
        self.state.filters[(filterField,filterLabel)]=filterItems
        
        #print self.state.filters[(filterField,filterLabel)]
        #print self.state.filters.keys()
    
    def makePT(self):
        
        self.state.makePT()    
        self.displayDT()
    
    def displayDT(self):
        
        import IPython.core.display as display
        
        df = self.state.PTresult
        
        display.display(df) 
        
        table = self.ui.displayTable
        table.setColumnCount(len(df.columns))
        table.setRowCount(len(df.index))
       
       
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                table.setItem(i,j,QtGui.QTableWidgetItem(str(df.iget_value(i, j))))

    

    def getResult(self):
            
            return self.state.PTresult



def start(df):
    '''Starts gui when imported'''
    
    import sys
    app = QtGui.QApplication(sys.argv)
    gui = MyDialog()
    gui.state.getData(df)
    gui.show()
    
    app.exec_()
    #sys.exit(app.exec_())
    
    return gui


def main():
    
    #df = pd.DataFrame({'a': 2*'a' ,'b' : 2*'b' , 'c' :[1,1]})
    
    path = '/home/phcostello/Dropbox/iHub/Umati/'
    df = pd.read_csv(path + 'FullData.csv')
    df = df.drop(['Name'],axis = 1)
    app = QtGui.QApplication(sys.argv)
    gui = MyDialog()
    gui.state.getData(df)
    gui.show()
    
        
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()