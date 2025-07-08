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


class Ui_Dialog(object):
    

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 200)
        Dialog.move(1000, 0)

                
        #topHight
        self.label_th = QtGui.QLabel('top hight',Dialog)
        self.label_th.setGeometry(QtCore.QRect(10, 38, 100, 22))
        self.le_th = QtGui.QLineEdit(Dialog)
        self.le_th.setGeometry(QtCore.QRect(140, 35, 100, 20))
        self.le_th.setAlignment(QtCore.Qt.AlignCenter)
        
        #bottom hight
        self.label_bh = QtGui.QLabel('bottom hight',Dialog)
        self.label_bh.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.le_bh = QtGui.QLineEdit(Dialog)
        self.le_bh.setGeometry(QtCore.QRect(140, 60, 100, 20))
        self.le_bh.setAlignment(QtCore.Qt.AlignCenter)

        #post dia
        self.label_dia = QtGui.QLabel('post dia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 88, 100, 22))
        self.le_dia = QtGui.QLineEdit(Dialog)
        self.le_dia.setGeometry(QtCore.QRect(140, 85, 100, 20))
        self.le_dia.setAlignment(QtCore.Qt.AlignCenter)

        #weirHight
        self.label_h0 = QtGui.QLabel('weirHight',Dialog)
        self.label_h0.setGeometry(QtCore.QRect(10, 113, 100, 22))
        self.le_h0 = QtGui.QLineEdit(Dialog)
        self.le_h0.setGeometry(QtCore.QRect(140, 110, 100, 20))
        self.le_h0.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton('create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 135, 100, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 135, 60, 22))
        #importData
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 160, 150, 22))

        
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "senterPost", None))
        
    def read_data(self):
     global spreadsheet
     selection = Gui.Selection.getSelection()
     # Partsグループが選択されているかチェック
     if selection:
         selected_object = selection[0]
         if selected_object.TypeId == "App::Part":
             parts_group = selected_object
             for obj in parts_group.Group:
                 print(obj.Label)
                 if obj.Label=='Spreadsheet_centerPost':
                     spreadsheet = obj
                     self.le_th.setText(spreadsheet.getContents('l1')) 
                     self.le_bh.setText(spreadsheet.getContents('l2')) 
                     self.le_dia.setText(spreadsheet.getContents('dia')) 
                     self.le_h0.setText(spreadsheet.getContents('h0')) 
                     App.ActiveDocument.recompute()
                          
    def update(self):
            #return

            l1=self.le_th.text()
            l2=self.le_bh.text()
            dia=self.le_dia.text()
            h0=self.le_h0.text()

            spreadsheet.set('dia',dia)
            spreadsheet.set('l1',l1)
            spreadsheet.set('l2',l2)
            spreadsheet.set('h0',h0)

            App.ActiveDocument.recompute() 

    def create(self): 
         fname='centerPost.FCStd'
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
        