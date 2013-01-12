# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../pivotTableTemplate.ui'
#
# Created: Sat Jan 12 19:32:40 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(554, 618)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(290, 60, 98, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 120, 98, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(290, 180, 98, 27))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.splitter_2 = QtGui.QSplitter(Dialog)
        self.splitter_2.setGeometry(QtCore.QRect(10, 20, 201, 581))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.label_4 = QtGui.QLabel(self.splitter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.listFields = QtGui.QListWidget(self.splitter)
        self.listFields.setObjectName(_fromUtf8("listFields"))
        self.widget = QtGui.QWidget(self.splitter_2)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ColLabel = QtGui.QLabel(self.widget)
        self.ColLabel.setObjectName(_fromUtf8("ColLabel"))
        self.verticalLayout.addWidget(self.ColLabel)
        self.listCols = QtGui.QListWidget(self.widget)
        self.listCols.setObjectName(_fromUtf8("listCols"))
        self.verticalLayout.addWidget(self.listCols)
        self.RowLabel = QtGui.QLabel(self.widget)
        self.RowLabel.setObjectName(_fromUtf8("RowLabel"))
        self.verticalLayout.addWidget(self.RowLabel)
        self.listValues = QtGui.QListWidget(self.widget)
        self.listValues.setObjectName(_fromUtf8("listValues"))
        self.verticalLayout.addWidget(self.listValues)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.listRows = QtGui.QListWidget(self.widget)
        self.listRows.setObjectName(_fromUtf8("listRows"))
        self.verticalLayout.addWidget(self.listRows)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "PandasPTGui", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Dialog", "PushButton2", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Dialog", "PushButton3", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.ColLabel.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.RowLabel.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

