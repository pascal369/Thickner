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
lattice=['6x38','9x38','6x44','9x44','4.5x50','6x50','9x50','6x65','9x65','6x75',
      '9x75','6x90','9x90',]
class Ui_Dialog(object):
    global column_list
    alphabet_list = list(string.ascii_uppercase)
    column_list=[]
    for i in range(0,26):
        column_list.append(alphabet_list[i])
    for i in range(0,26):
        for j in range(0,26):
            column_list.append(alphabet_list[i] + alphabet_list[j])

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 450)
        Dialog.move(1000, 0)

        #tankDia
        self.label_D = QtGui.QLabel('tankDia',Dialog)
        self.label_D.setGeometry(QtCore.QRect(10, 13, 100, 22))
        self.spinBoxL=QtGui.QSpinBox(Dialog)
        self.spinBoxL.setGeometry(140, 10, 100, 50)
        self.spinBoxL.setMinimum(1000)  # 最小値
        self.spinBoxL.setMaximum(20000)  # 最大値
        self.spinBoxL.setSingleStep(50) #step
        self.spinBoxL.setAlignment(QtCore.Qt.AlignCenter)

        #depth of water
        self.label_hw = QtGui.QLabel('depth of water hw',Dialog)
        self.label_hw.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.le_hw = QtGui.QLineEdit(Dialog)
        self.le_hw.setGeometry(QtCore.QRect(140, 60, 100, 20))
        self.le_hw.setAlignment(QtCore.Qt.AlignCenter)
        
        #ブラケット高 h1
        self.label_h1 = QtGui.QLabel('bracketHight',Dialog)
        self.label_h1.setGeometry(QtCore.QRect(10, 88, 100, 22))
        self.le_h1 = QtGui.QLineEdit(Dialog)
        self.le_h1.setGeometry(QtCore.QRect(140, 85, 100, 20))
        self.le_h1.setAlignment(QtCore.Qt.AlignCenter)

        #ブラケット角 ba
        self.label_ba = QtGui.QLabel('bracketAngle',Dialog)
        self.label_ba.setGeometry(QtCore.QRect(10, 113, 100, 22))
        self.le_ba = QtGui.QLineEdit(Dialog)
        self.le_ba.setGeometry(QtCore.QRect(140, 110, 100, 20))
        self.le_ba.setAlignment(QtCore.Qt.AlignCenter)


        #梁成 H0
        self.label_H0 = QtGui.QLabel('beamHight',Dialog)
        self.label_H0.setGeometry(QtCore.QRect(10, 138, 100, 22))
        self.spinBoxH0=QtGui.QSpinBox(Dialog)
        self.spinBoxH0.setGeometry(140, 133, 100, 50)
        self.spinBoxH0.setMinimum(300)  # 最小値
        self.spinBoxH0.setMaximum(2000)  # 最大値
        self.spinBoxH0.setSingleStep(50) #step
        self.spinBoxH0.setAlignment(QtCore.Qt.AlignCenter)

        #弦材 chord member
        self.label_GL = QtGui.QLabel('chordMember',Dialog)
        self.label_GL.setGeometry(QtCore.QRect(10, 188, 100, 22))
        self.comboBox_GL = QtGui.QComboBox(Dialog)
        self.comboBox_GL.setGeometry(QtCore.QRect(140, 185, 100, 22))
        #ラチス材 Lattice member
        self.label_Ls = QtGui.QLabel('latticeMember',Dialog)
        self.label_Ls.setGeometry(QtCore.QRect(10, 213, 100, 22))
        self.comboBox_Ls = QtGui.QComboBox(Dialog)
        self.comboBox_Ls.setGeometry(QtCore.QRect(140, 210, 100, 22))
        
        #作成
        self.pushButton = QtGui.QPushButton('create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 235, 100, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 235, 60, 22))
        #importData
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 260, 150, 22))
        
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 285, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        #self.comboBox_D.addItems(tankDia)
        self.comboBox_GL.addItems(katakou)
        self.comboBox_Ls.addItems(lattice)

        self.spinBoxL.valueChanged[int].connect(self.spinMove) 
        self.spinBoxH0.valueChanged[int].connect(self.spinMoveh)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)

        fname='feedWell.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'png',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "feedWell", None))
        
    def spinMove(self):
         dL=self.spinBoxL.value()
         spreadsheet_feedWell.set('D0',str(dL))
         L0=dL-500
         spreadsheet_support.set('L0',str(L0))
         App.ActiveDocument.recompute() 
    def spinMoveh(self):
         hL=self.spinBoxH0.value()
         spreadsheet_support.set('H0',str(hL))
         App.ActiveDocument.recompute()      

         
    def read_data(self):
         #return
         global spreadsheet_feedWell
         global spreadsheet_support
         global angle
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     print(obj.Label)
                     if obj.Label[:20]=='Spreadsheet_feedWell':
                         spreadsheet_feedWell = obj
                     elif obj.Label[:20] == "Spreadsheet_support":
                         spreadsheet_support = obj  
                     elif obj.Label == "AngleSteel004":   
                         angle=obj    

                 self.le_hw.setText(spreadsheet_feedWell.getContents('hw')) #水深
                 self.le_h1.setText(spreadsheet_feedWell.getContents('h1')) #ブラケット
                 self.le_ba.setText(spreadsheet_feedWell.getContents('ba')) #ブラケット
                 self.spinBoxL.setValue(int(spreadsheet_feedWell.getContents('D0')))
                 self.spinBoxH0.setValue(int(spreadsheet_support.getContents('H0')))
                 self.comboBox_GL.setEditable(True)    
                 self.comboBox_Ls.setEditable(True)    
                 self.comboBox_GL.setCurrentText(spreadsheet_support.getContents('shp')[1:]) #弦材
                 self.comboBox_Ls.setCurrentText(spreadsheet_support.getContents('Lshp')[1:]) #ラチス材
                 App.ActiveDocument.recompute()
                          
    def update(self):
            #return
            D0=self.spinBoxL.value()
            hw=self.le_hw.text()
            h1=self.le_h1.text()
            ba=self.le_ba.text()
            
            H0=self.spinBoxH0.value()
            GL=self.comboBox_GL.currentText()
            Ls=self.comboBox_Ls.currentText()
            L0=float(D0)-500
            Bshp=self.comboBox_GL.currentText()
            angle.size = str(Bshp)

         #玄材ゲージライン 
            for i in range(17,32):
                Bshp3=spreadsheet_support.getContents('A'+str(i))
                if Bshp==Bshp3[1:]:
                    break
            row_B=i  
            
            GL0=spreadsheet_support.getContents('D'+str(row_B)) 
            
            #ラチス個数
            for n in range(1,100):
                rp03=(float(L0)-2*float(GL0))/n
                if float(rp03)<=float(H0):
                    break
            rn0=n  

            #ラチス材幅、板厚
            Lshp=self.comboBox_Ls.currentText()
            for i in range(34,46):
                Lshp3=spreadsheet_support.getContents('A'+str(i))
                #print(Lshp,Lshp3)
                if Lshp==Lshp3[1:]:
                    break
            row_L=i  

            Lt0=spreadsheet_support.getContents('B'+str(row_L))     
            Lb0=spreadsheet_support.getContents('C'+str(row_L))     
        
            spreadsheet_feedWell.set('D0',D0)
            spreadsheet_feedWell.set('hw',hw)
            spreadsheet_feedWell.set('h1',h1)
            spreadsheet_feedWell.set('ba',ba)

            spreadsheet_support.set('L0',str(L0))
            spreadsheet_support.set('H0',H0)
            spreadsheet_support.set('shp',GL)
            spreadsheet_support.set('Lshp',Ls)
            spreadsheet_support.set('Lb0',Lb0)

            App.ActiveDocument.recompute() 
            
    def create(self): 
         fname='feedWell.FCStd'
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
        # スクリプトのウィンドウを取得
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd') 
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint) 
        