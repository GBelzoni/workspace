'''
Created on Jan 12, 2013

@author: phcostello
'''

import sys
import pandas as pd
from PyQt4 import QtCore, QtGui
from pivotTableTemplate import Ui_Dialog
import PivotGuiInner

'This Module connect the GUIInner state to the GUI window and handles events'

class MyDialog(QtGui.QMainWindow):
    
#  def __init__(self, parent=None):
#    
#    QtGui.QWidget.__init__(self, parent)
#    self.ui = Ui_Dialog()
#    self.ui.setupUi(self)
    
    def __init__(self):
        
        #Call my dialog parent constructor
        super(MyDialog, self).__init__()
        
        #Call template generated from qtdesigner
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        #Add inner state variable
        self.state = PivotGuiInner.PandasPivotGuiInner()
        
        #Register Event Handlers
        self.ui.pushButton.clicked.connect(self.buttonClicked)
        
        #Start gui
        self.show()
        
    def buttonClicked(self):
        
        fieldLabels = self.state.fieldLabels
        
        for item in fieldLabels:
            print item
            item = QtGui.QListWidgetItem(str(item) )
            self.ui.listFields.addItem(item)
            
        for item in fieldLabels:
            print item
            item = QtGui.QListWidgetItem(str(item) )
            self.ui.listCols.addItem(item)
    

def main():
    
    df = pd.DataFrame({'a': 2*'a' ,'b' : 2*'b' , 'c' :[1,1]})
    app = QtGui.QApplication(sys.argv)
    
    gui = MyDialog()
    gui.state.getData(df)
    gui.state.setState()
    gui.show()
    
    
    app.exec_()
    

   

if __name__ == '__main__':
    main()