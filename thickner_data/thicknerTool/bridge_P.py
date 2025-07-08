# -*- coding: utf-8 -*-
#from curses import keyname
from ast import Delete
import os
from pickle import TRUE
import sys
import math
import string
from tkinter.tix import ComboBox
import Import
import Spreadsheet
import DraftVecUtils
import Sketcher
import PartDesign
import Draft
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
#from prt_data.CSnap_data import paramCSnap

tankDia=['13000','13500','14000','14500','15000','15500','16000','16500','17000','17500',
         '18000','18500','19000','19500','20000']
katakou=['40x40x3','40x40x5','50x50x4','50x50x6','65x65x6','65x65x8','75x75x6','75x75x9',
         '75x75x12','90x90x7','100x100x10','100x100x13']
class Ui_Dialog(object):
    

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 150)
        Dialog.move(1000, 0)

        #tankDia
        self.label_D = QtGui.QLabel('tankDia',Dialog)
        self.label_D.setGeometry(QtCore.QRect(10, 13, 100, 22))
        self.comboBox_D = QtGui.QComboBox(Dialog)
        self.comboBox_D.setGeometry(QtCore.QRect(140, 10, 100, 22))
        
        #hight
        self.label_h0 = QtGui.QLabel('hight',Dialog)
        self.label_h0.setGeometry(QtCore.QRect(10, 38, 100, 22))
        self.le_h0 = QtGui.QLineEdit('300',Dialog)
        self.le_h0.setGeometry(QtCore.QRect(140, 35, 100, 20))
        self.le_h0.setAlignment(QtCore.Qt.AlignCenter)

       #no of beam
        self.label_n = QtGui.QLabel('no of beam',Dialog)
        self.label_n.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.le_n0 = QtGui.QLineEdit('8',Dialog)
        self.le_n0.setGeometry(QtCore.QRect(140, 60, 100, 20))
        self.le_n0.setAlignment(QtCore.Qt.AlignCenter) 

        #作成
        self.pushButton = QtGui.QPushButton('create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 85, 90, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 85, 60, 22))
        #importData
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 110, 150, 22))
        
        self.comboBox_D.addItems(tankDia)
        
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "feedWell", None))
        
    def read_data(self):
         #return
         global spreadsheet
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     print(obj.Label)
                     if obj.Label=='Spreadsheet_bridge':
                         spreadsheet = obj

                 self.comboBox_D.setEditable(True)         
                 self.comboBox_D.setCurrentText(spreadsheet.getContents('dia')) #池径
                 self.le_h0.setText(spreadsheet.getContents('hight'))
                 self.le_n0.setText(spreadsheet.getContents('n'))
                 
                 App.ActiveDocument.recompute()
                          
    def update(self):
            #return
            dia=self.comboBox_D.currentText()
            hight=self.le_h0.text()
            n=self.le_n0.text()
            spreadsheet.set('dia',dia)
            spreadsheet.set('hight',hight)
            spreadsheet.set('n',n)
            
            App.ActiveDocument.recompute() 
    def create(self): 
         fname='bridge_P.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, fname) 
         Gui.ActiveDocument.mergeProject(joined_path)
         return

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd') 
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint) 
        