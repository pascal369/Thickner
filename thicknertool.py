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

tankDia=['13.0','13.5','14.0','14.5','15.0','15.5','16.0','16.5','17.0',
         '17.5','18.0','18.5','19.0','19.5','20.0']
thickner_type=['suspended','pillar','common',]
suspended_parts=['Body_S','mainShaft','skimmerBrade_suspend','mainShaftBrg','turnBackle',
                 'drivePart','bridge_S']
pillar_parts=['Body_P','centerPost','skimmerBrade','centerCage','bridge_P','drivePart_P']
common_parts=['rakeArm','rakeBrade','feedWell','pipeSkimmer','bufflePlate','turnBackle',]

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName('Dialog')
        Dialog.resize(300, 400)
        Dialog.move(1000, 0)
        #type
        self.label_Type = QtGui.QLabel('Type',Dialog)
        self.label_Type.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_Type = QtGui.QComboBox(Dialog)
        self.comboBox_Type.setGeometry(QtCore.QRect(130, 10, 150, 22))
        #Parts
        self.label_Parts = QtGui.QLabel('Parts',Dialog)
        self.label_Parts.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.comboBox_Parts = QtGui.QComboBox(Dialog)
        self.comboBox_Parts.setGeometry(QtCore.QRect(130, 35, 150, 22))
        #tankDia
        self.label_D = QtGui.QLabel('tankDia[mm]',Dialog)
        self.label_D.setGeometry(QtCore.QRect(10, 63, 80, 12))
        self.comboBox_D = QtGui.QComboBox(Dialog)
        self.comboBox_D.setGeometry(QtCore.QRect(130, 60, 150, 22))

        #execution
        self.pushButton2 = QtGui.QPushButton('Execution',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(60, 85, 70, 22))
        #update
        self.pushButton1 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton1.setGeometry(QtCore.QRect(140, 85, 60, 22))
        #importData
        self.pushButton3 = QtGui.QPushButton('ImportData',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(210, 85, 70, 22))
        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(30, 110, 250, 250))
        self.img.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_Type.addItems(thickner_type) 

        self.comboBox_Type.setCurrentIndex(1)
        self.comboBox_Type.currentIndexChanged[int].connect(self.onType)
        self.comboBox_Type.setCurrentIndex(0)

        self.comboBox_Parts.setCurrentIndex(1)
        self.comboBox_Parts.currentIndexChanged[int].connect(self.onParts)
        self.comboBox_Parts.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton1, QtCore.SIGNAL("pressed()"), self.update)  
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'thicknerTool', None))
    
    def read_data(self):
         global key
         #global D
         global Spreadsheet_feedWell
         global Spreadsheet_support
         global Spreadsheet_pipeSkimmer
         global Spreadsheet_turnBackle
         key=self.comboBox_Parts.currentText()
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     #print(obj.Label)
                     if obj.Label=='feedWell':
                          feedWell=obj
                     if obj.TypeId == "Spreadsheet::Sheet":
                         #print(obj.Label)
                         if obj.Label=='Spreadsheet_feedWell':
                              Spreadsheet_feedWell=obj
                         elif obj.Label=='Spreadsheet_support':
                              Spreadsheet_support=obj  
                         elif obj.Label=='Spreadsheet_pipeSkimmer':
                              Spreadsheet_pipeSkimmer=obj   
                         elif obj.Label=='Spreadsheet_turnBackle':
                              Spreadsheet_turnBackle=obj     

                         if key=='feedWell':
                             self.comboBox_D.setCurrentText(Spreadsheet_support.getContents('D0')) 
                         elif key=='pipeSkimmer':
                             self.comboBox_D.setCurrentText(Spreadsheet_pipeSkimmer.getContents('D0')) 
                         D=self.comboBox_D.currentText()

    def update(self):
         
         D=self.comboBox_D.currentText()
         D=float(D)*1000
         if D<=6000:
              return
         Spreadsheet_support.set('D0',str(D))
         L0=D-500.0
         dia=D*0.2
         w0=(float(L0)-float(dia))/4-145-200
         l0=(dia)+240
         Spreadsheet_turnBackle.set('w0',str(w0))
         Spreadsheet_turnBackle.set('l0',str(l0))
         App.ActiveDocument.recompute() 
 
    def onParts(self):
         key=self.comboBox_Parts.currentText()    
         if key=='Body_S':
              pic='Body_S.png'
         elif key=='Body_P':
              pic='Body_P.png'     
         elif key=='mainShaft':
              pic='mainShaft.png' 
         elif key=='mainShaftBrg':
              pic='mainShaftBrg.png' 
         elif key=='turnBackle':
              pic='turnBackle.png'     
         elif key=='skimmerBrade':
              pic='skimmerBrade.png' 
         elif key=='skimmerBrade_suspend':
              pic='skimmerBrade_suspend.png'           
         elif key=='centerWell_S':
              pic='centerWell_S.png'   
         elif key=='drivePart':
              pic='drivePart.png'  
         elif key=='drivePart_P':
              pic='drivePart_P.png'        
         elif key=='bridge_S':
              pic='bridge_S.png'  
         elif key=='bridge_P':
              pic='bridge_P.png'  
         elif key=='centerPost':
              pic='centerPost.png' 
         elif key=='centerCage':
              pic='centerCage.png'   
         elif key=='rakeArm':
              pic='rakeArm.png'         
         elif key=='feedWell':
              pic='feedWell.png'         
         elif key=='bufflePlate':
              pic='bufflePlate.png'        
         elif key=='rakeBrade':
              pic='rakeBrade.png'   
         elif key=='pipeSkimmer':
              pic='pipeSkimmer.png'    
         
         try:
              mypath='thicknerTool'
              base=os.path.dirname(os.path.abspath(__file__))
              joined_path = os.path.join(base, "Sewage_eqp_data",mypath,'png',pic)
              self.img.setPixmap(QtGui.QPixmap(joined_path)) 
         except:
              pass                           
    def onType(self):
         key=self.comboBox_Type.currentText()
         self.comboBox_Parts.clear()
         self.comboBox_D.clear()
         if key=='suspended':
              self.comboBox_D.addItems(tankDia[:5])
              self.comboBox_Parts.addItems(suspended_parts)
         elif key=='pillar':
              self.comboBox_D.addItems(tankDia[5:])
              self.comboBox_Parts.addItems(pillar_parts)   
         elif key=='common':
              self.comboBox_D.addItems(tankDia)
              self.comboBox_Parts.addItems(common_parts)       
         
    def create(self):
         #if float(D)<=6000:
         #    return
         key2=self.comboBox_Parts.currentText()
         if key2=='centerCage':
              from sewage_eqp_data.thicknerTool import centerCage
              centerCage
              return
         elif key2=='wellSuport':
              fname='wellSuport.FCStd'
              mypath='thicknerTool'       
         elif key2=='rakeArm':
              from sewage_eqp_data.thicknerTool import rakeArm
              rakeArm 
              return
         elif key2=='bufflePlate':
              from sewage_eqp_data.thicknerTool import bufflePlate
         elif key2=='pipeSkimmer':
              from sewage_eqp_data.thicknerTool import pipeSkimmer
              pipeSkimmer 
              return
         elif key2=='feedWell':
              from sewage_eqp_data.thicknerTool import feedWell
              feedWell 
              return
         elif key2=='centerPost' :
              #print('aaaaaaaaaaaaaaaaa')
              from sewage_eqp_data.thicknerTool import centerPost
              centerPost
              return 
         elif key2=='mainShaft' :
              from sewage_eqp_data.thicknerTool import mainShaft
              return 
         elif key2=='mainShaftBrg' :
              fname='mainShaftBrg.FCStd'    
              mypath='thicknerTool'      
         elif key2=='turnBackle' :
              fname='turnBackle.FCStd'    
              mypath='thicknerTool'    
         elif key2=='drivePart' :
              fname='drivePart.FCStd'    
              mypath='thicknerTool'  
         elif key2=='drivePart_P' :
              fname='driveUnit.FCStd'    
              mypath='thicknerTool'        
         elif key2=='bridge_S' :
              from sewage_eqp_data.thicknerTool import bridge
              return 
         elif key2=='bridge_P' :
              from sewage_eqp_data.thicknerTool import bridge_P
              return    
         elif key2=='rakeBrade' :
              fname='rakeBrade.FCStd'    
              mypath='thicknerTool'      
         elif key2=='skimmerBrade_suspend' :
              from sewage_eqp_data.thicknerTool import skimmerBrade
              return        
         elif key2=='skimmerBrade' :
              from sewage_eqp_data.thicknerTool import skimmerBrade_P
              return        
         elif key2=='Body_S' or key2=='Body_P' :
              dia=self.comboBox_D.currentText()
              fname='body'+dia+'m.FCStd'    
              mypath='thicknerTool'     


         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'Sewage_eqp_data',mypath,fname) 
         #print(joined_path) 
         Gui.ActiveDocument.mergeProject(joined_path) 
         
         Gui.SendMsgToActiveView("ViewFit")

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)               