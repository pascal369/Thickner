# -*- coding: utf-8 -*-
import os
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore

tank_data=['13000','13500','14000','14500','15000',]

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 200)
        Dialog.move(1000, 0)
        #槽径
        self.label_D = QtGui.QLabel('tankDia',Dialog)
        self.label_D.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_D = QtGui.QComboBox(Dialog)
        self.comboBox_D.setGeometry(QtCore.QRect(140, 10, 80, 22))
        #バッフル位置 
        self.label_bf = QtGui.QLabel('buffle Position',Dialog)
        self.label_bf.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.le_bf = QtGui.QLineEdit('1750',Dialog)
        self.le_bf.setGeometry(QtCore.QRect(140, 35, 80, 20))
        self.le_bf.setAlignment(QtCore.Qt.AlignCenter)

        #ブレード数
        self.label_n = QtGui.QLabel('nomber Of brade',Dialog)
        self.label_n.setGeometry(QtCore.QRect(10, 63, 100, 12))
        self.le_n = QtGui.QLineEdit('5',Dialog)
        self.le_n.setGeometry(QtCore.QRect(140, 60, 80, 20))
        self.le_n.setAlignment(QtCore.Qt.AlignCenter)
        #ブレード幅
        self.label_bw = QtGui.QLabel('breade width',Dialog)
        self.label_bw.setGeometry(QtCore.QRect(10, 88, 100, 12))
        self.le_bw = QtGui.QLineEdit('700',Dialog)
        self.le_bw.setGeometry(QtCore.QRect(140, 85, 80, 20))
        self.le_bw.setAlignment(QtCore.Qt.AlignCenter)
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 130, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 130, 80, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 155, 170, 22))

        self.comboBox_D.addItems(tank_data)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "skimmerBrade", None))
        
    def read_data(self):
         global spreadsheet
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj
                         self.comboBox_D.setCurrentText(spreadsheet.getContents('D0'))
                         self.le_bf.setText(spreadsheet.getContents('bp'))
                         self.le_n.setText(spreadsheet.getContents('n0'))
                         self.le_bw.setText(spreadsheet.getContents('w1'))

    def update(self):
         D0=self.comboBox_D.currentText()
         bp=self.le_bf.text()
         n=self.le_n.text()
         w1=self.le_bw.text()
         spreadsheet.set('D0',str(D0))
         spreadsheet.set('bp',str(bp))
         spreadsheet.set('n0',str(n))
         spreadsheet.set('w1',str(w1))
         App.ActiveDocument.recompute() 

    def create(self): 

        fname='skimmerBrade_suspend.FCStd'
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, fname) 
        Gui.ActiveDocument.mergeProject(joined_path)

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd') 
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            