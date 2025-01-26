# -*- coding: utf-8 -*-
from mimetypes import common_types
import os
import sys
import subprocess
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
import importlib

Eqp=['Thickner',]
thickner_type=['suspended_type_thickner','pillar_type_thickner',]
thickner_series=['13.0m','13.5m','14.0m','14.5m','15.0m','15.5m','16.0m','16.5m','17.0m',
                 '17.5m','18.0m','18.5m','19.0m','19.5m','20.0m',]

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName('Dialog')
        Dialog.resize(300, 400)
        Dialog.move(1000, 0)
        
        #Eqp
        self.label_Eqp = QtGui.QLabel('Equipment',Dialog)
        self.label_Eqp.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_Eqp = QtGui.QComboBox(Dialog)
        self.comboBox_Eqp.setGeometry(QtCore.QRect(80, 10, 200, 22))
        #Type
        self.label_Type = QtGui.QLabel('Type',Dialog)
        self.label_Type.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.comboBox_Type = QtGui.QComboBox(Dialog)
        self.comboBox_Type.setGeometry(QtCore.QRect(80, 35, 200, 22))
        #Series
        self.label_Series = QtGui.QLabel('Series',Dialog)
        self.label_Series.setGeometry(QtCore.QRect(10, 63, 100, 12))
        self.comboBox_Series = QtGui.QComboBox(Dialog)
        self.comboBox_Series.setGeometry(QtCore.QRect(80, 60, 200, 22))
        #実行
        self.pushButton = QtGui.QPushButton('Educution',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 85, 100, 22))
        #tool
        self.pushButton2 = QtGui.QPushButton('Tool',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(180, 85, 100, 22))
        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(30, 140, 250, 250))
        self.img.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_Eqp.addItems(Eqp)
        self.comboBox_Eqp.setCurrentIndex(1)
        self.comboBox_Eqp.currentIndexChanged[int].connect(self.onEqp)
        self.comboBox_Eqp.setCurrentIndex(0)

        self.comboBox_Type.setCurrentIndex(1) 
        self.comboBox_Type.currentIndexChanged[int].connect(self.onType)
        self.comboBox_Type.setCurrentIndex(0) 

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.create2)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'thicknerWB', None))
        pass

    def onEqp(self):
         global pic
         self.comboBox_Type.clear()
         self.comboBox_Series.clear()
         key=self.comboBox_Eqp.currentText()
         key2=self.comboBox_Type.currentText()
         if key=='Thickner':#thickner
             self.comboBox_Type.show()
             self.comboBox_Series.show()
             self.comboBox_Type.addItems(thickner_type)  
             key2=self.comboBox_Type.currentText()
             if key2=='suspended_type_thickner':
                 mypath=key2
                 pic='suspended_type_thickner.png'
             elif key2=='pillar_type_thickner':
                 mypath=key2
                 pic='pillar_type_thickner.png'
        
         try:
              base=os.path.dirname(os.path.abspath(__file__))
              joined_path = os.path.join(base, "Sewage_eqp_data",mypath,pic)
              self.img.setPixmap(QtGui.QPixmap(joined_path)) 
         except:
              pass    
    
    def onType(self):
         #global mypath
         #global key
         self.comboBox_Series.clear()
         key=self.comboBox_Eqp.currentText()
         key2=self.comboBox_Type.currentText()
         #print(key,key2)
         
         if key=='Thickner':#thickner
             key2=self.comboBox_Type.currentText()
             if key2=='suspended_type_thickner':
                 self.comboBox_Series.addItems(thickner_series[:5])  
                 mypath='suspended_type_thickner'
                 pic='suspended_type_thickner.png'
             elif key2=='pillar_type_thickner':
                 self.comboBox_Series.addItems(thickner_series[5:])  
                 mypath='pillar_type_thickner'
                 pic='pillar_type_thickner.png'
         
         try:
             base=os.path.dirname(os.path.abspath(__file__))
             joined_path = os.path.join(base, "Sewage_eqp_data",mypath,pic)
             self.img.setPixmap(QtGui.QPixmap(joined_path))   
         except:
             pass             
    def create2(self): 
        key2=self.comboBox_Eqp.currentText()
        if key2=='Thickner':
            import thicknertool
            thicknertool

    def create(self): 
            key=self.comboBox_Eqp.currentText()
            key3=self.comboBox_Series.currentText()
            key2=self.comboBox_Type.currentText()
            mypath=key3
            if key2=='suspended_type_thickner':
                fname='suspendAssy_'+key3+'.FCStd'
            elif key2=='pillar_type_thickner':
                fname='pillarAssy_'+key3+'.FCStd'
         
            elif key=='Thickner':
                if key2=='suspended_type_thickner':
                    import thicknerAssy_S
                    thicknerAssy_S 
                elif key2=='pillar_type_thickner':
                    import thicknerAssy_P
                    thicknerAssy_P   
           
            base=os.path.dirname(os.path.abspath(__file__)) 
            joined_path = os.path.join(base, 'Sewage_eqp_data',key2,mypath,fname) 
            print(joined_path)
            doc=App.activeDocument()
            Gui.ActiveDocument.mergeProject(joined_path)

            App.ActiveDocument.recompute()  
            Gui.ActiveDocument.ActiveView.fitAll()  
         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        
           