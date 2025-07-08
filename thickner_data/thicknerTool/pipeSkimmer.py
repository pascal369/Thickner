# -*- coding: utf-8 -*-
#from curses import keyname
from ast import Delete
import os
from pickle import TRUE
import sys
import math
import string

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

dia_data=['10','12','16','20','22','24','30',]

class Ui_Dialog(object):
    

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 450)
        Dialog.move(1000, 0)

        #pipeSkimmerLength L
        self.label_L = QtGui.QLabel('fullLength',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 13, 100, 22))
        self.le_L = QtGui.QLineEdit('6500',Dialog)
        self.le_L.setGeometry(QtCore.QRect(140, 10, 60, 20))
        self.le_L.setAlignment(QtCore.Qt.AlignCenter)
        #Opening Length
        self.label_L3 = QtGui.QLabel('weirLength l3',Dialog)
        self.label_L3.setGeometry(QtCore.QRect(10, 38, 100, 22))
        self.le_L3 = QtGui.QLineEdit('1000',Dialog)
        self.le_L3.setGeometry(QtCore.QRect(140, 35, 60, 20))
        self.le_L3.setAlignment(QtCore.Qt.AlignCenter)
        #noberOfweir
        self.label_n0 = QtGui.QLabel('noberOfweir n0',Dialog)
        self.label_n0.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.le_n0 = QtGui.QLineEdit('1000',Dialog)
        self.le_n0.setGeometry(QtCore.QRect(140, 60, 60, 20))
        self.le_n0.setAlignment(QtCore.Qt.AlignCenter)
        #innerPipe Length L1
        self.label_L1 = QtGui.QLabel('innerPipe Length l1',Dialog)
        self.label_L1.setGeometry(QtCore.QRect(10, 88, 100, 22))
        self.le_L1 = QtGui.QLineEdit('450',Dialog)
        self.le_L1.setGeometry(QtCore.QRect(140, 85, 60, 20))
        self.le_L1.setAlignment(QtCore.Qt.AlignCenter)

        #開閉機 L2
        self.label_L2 = QtGui.QLabel('open/closeMachine l2',Dialog)
        self.label_L2.setGeometry(QtCore.QRect(10, 113, 120, 22))
        self.le_L2 = QtGui.QLineEdit(Dialog)
        self.le_L2.setGeometry(QtCore.QRect(140, 110, 60, 20))
        self.le_L2.setAlignment(QtCore.Qt.AlignCenter)
        #開閉機 h2
        self.label_h2 = QtGui.QLabel('open/closeMachine h2',Dialog)
        self.label_h2.setGeometry(QtCore.QRect(10, 138, 120, 22))
        self.le_h2 = QtGui.QLineEdit(Dialog)
        self.le_h2.setGeometry(QtCore.QRect(140, 135, 60, 20))
        self.le_h2.setAlignment(QtCore.Qt.AlignCenter)
        #軸受位置 L4
        self.label_L4 = QtGui.QLabel('brgPosition',Dialog)
        self.label_L4.setGeometry(QtCore.QRect(10, 163, 100, 22))
        self.le_L4 = QtGui.QLineEdit(Dialog)
        self.le_L4.setGeometry(QtCore.QRect(140, 160, 60, 20))
        self.le_L4.setAlignment(QtCore.Qt.AlignCenter)


        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 185, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 185, 60, 22))
        #importData
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 210, 150, 22))
        #spinBox
        self.label_spin=QtGui.QLabel('Animation',Dialog)
        self.label_spin.setGeometry(QtCore.QRect(10, 235, 150, 22))
        self.spinBox=QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(80, 235, 50, 30)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 260, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.spinBox.valueChanged[int].connect(self.spinMove) 

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)

        fname='pipeSkimmer.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'png',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "pipeSkimmer", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  
        
    def spinMove(self):
         r1 = self.spinBox.value()
         try:
             pipeA.Placement.Rotation=App.Rotation(App.Vector(1,0,0),-r1)
             Gui.runCommand('a2p_SolverCommand',0)
             App.ActiveDocument.recompute()
         except:
              return
         
    def read_data(self):
         global spreadsheet
         global pipeA
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     print(obj.Label)
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj
                     elif obj.Label=='pipeA':
                         pipeA=obj    
                         
                 self.le_L.setText(spreadsheet.getContents('L0')) #パイプ全長

                 self.le_L1.setText(spreadsheet.getContents('l1')) #パイプ内側長
                 self.le_L2.setText(spreadsheet.getContents('l2')) #開閉台位置
                 self.le_h2.setText(spreadsheet.getContents('h2')) #開閉台位置
                 self.le_L4.setText(spreadsheet.getContents('l4')) #軸受位置
                 self.le_L3.setText(spreadsheet.getContents('l3')) #越流堰長
                 self.le_n0.setText(spreadsheet.getContents('n0')) #越流堰数
                
                 App.ActiveDocument.recompute()
                          
    def update(self):
           
            L0=float(self.le_L.text())
            l1=float(self.le_L1.text())
            l2=float(self.le_L2.text())
            h2=float(self.le_h2.text())
            l4=float(self.le_L4.text())
            l3=float(self.le_L3.text())
            n0=int(self.le_n0.text())
            #n0=(L0-(200+l4-19))/(l3+50)
            #n0=int(n0+1)
            #print(n0)
            #l3=(L0-(l1+200))/n0-90
            #l3=(L0-500)/n0-90
            

            l3=int(l3)
            spreadsheet.set('L0',str(L0))#L0
            spreadsheet.set('l1',str(l1))#l1
            spreadsheet.set('l2',str(l2))#l2
            spreadsheet.set('h2',str(h2))#l2
            spreadsheet.set('l3',str(l3))#l3
            spreadsheet.set('n0',str(n0))#n0
            spreadsheet.set('l4',str(l4))#l3

            App.ActiveDocument.recompute() 
            try:
                Gui.runCommand('a2p_updateImportedParts',0)
            except:    
                return
    def create(self): 
         fname='pipeSkimmer.FCStd'
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
        