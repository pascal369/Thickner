# -*- coding: utf-8 -*-
from operator import pos
import os
import sys
import subprocess
import numpy as np
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore


thickner_series=['13.0m','13.5m','14.0m','14.5m','15.0m','15.5m','16.0m','16.5m','17.0m',
                 '17.5m','18.0m','18.5m','19.0m','19.5m','20.0m',]

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName('Dialog')
        Dialog.resize(300, 125)
        Dialog.move(1500, 0)

        #Series
        self.label_Series = QtGui.QLabel('Series',Dialog)
        self.label_Series.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_Series = QtGui.QComboBox(Dialog)
        self.comboBox_Series.setGeometry(QtCore.QRect(80, 10, 200, 22))
        #Create
        self.pushButton2 = QtGui.QPushButton('Create',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(80, 35, 100, 22))
        
        #ImportData
        self.pushButton = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(180, 35, 100, 22))
        #pipeSkimmer
        self.pushButton3 = QtGui.QPushButton('pipeSkimmer',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(180, 60, 100, 22))

        #spinBox
        self.label_spin=QtGui.QLabel('Animation',Dialog)
        self.label_spin.setGeometry(QtCore.QRect(10, 60, 150, 22))
        self.spinBox=QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(80, 60, 50, 30)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)


        self.comboBox_Series.addItems(thickner_series) 

        self.spinBox.valueChanged[int].connect(self.spinMove) 
        

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.setParts)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.onPipe)


        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'suspendedTypeThickner', None))
         
    def create(self):
          mypath=self.comboBox_Series.currentText()
          key=self.comboBox_Series.currentIndex()
          if key<=4:
              fname='suspendAssy_' + mypath + '.FCStd'
              mypath2='suspended_type_thickner'
          elif key>4:
              fname='pillar_thickner_'+mypath+'.FCStd'
              mypath2='pillar_type_thickner'
          
          base=os.path.dirname(os.path.abspath(__file__))
          try:
              joined_path = os.path.join(base, 'Sewage_eqp_data',mypath2,mypath,fname) 
              #print(joined_path)
              Gui.ActiveDocument.mergeProject(joined_path) 
          except:
               #print('aaaaaaaaaaa')
               pass
          Gui.SendMsgToActiveView("ViewFit")
    def onPipe(self):
        from sewage_eqp_data.thicknerTool import pipeSkimmer     
    def setParts(self):
         global movingPart
         # ドキュメントを取得
         doc = App.activeDocument()
         if doc:
             group_names = []
             for obj in doc.Objects:
                 if obj.Label=='movingPart':
                      movingPart=obj     
    def spinMove(self):
         
         key=self.comboBox_Series.currentIndex()
         r1 = self.spinBox.value()
         movingPart.Placement.Rotation=App.Rotation(App.Vector(0,0,1),-r1)
         App.ActiveDocument.recompute()
         

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        # スクリプトのウィンドウを取得
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)               