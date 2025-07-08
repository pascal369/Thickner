# -*- coding: utf-8 -*-
#from curses import keyname
from ast import Delete
import os
from pickle import TRUE
import sys
import string

import Import
import Spreadsheet
import DraftVecUtils
import Sketcher
import PartDesign
import math
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore




# 画面を並べて表示する
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

        #アーム成
        self.label_H = QtGui.QLabel('armHight',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 13, 100, 22))
        self.le_H = QtGui.QLineEdit('800',Dialog)
        self.le_H.setGeometry(QtCore.QRect(110, 10, 50, 20))
        self.le_H.setAlignment(QtCore.Qt.AlignCenter)
        #アーム立ち上がり h1
        self.label_h1 = QtGui.QLabel('rising h1',Dialog)
        self.label_h1.setGeometry(QtCore.QRect(10, 38, 100, 22))
        self.le_h1 = QtGui.QLineEdit('300',Dialog)
        self.le_h1.setGeometry(QtCore.QRect(110, 35, 50, 20))
        self.le_h1.setAlignment(QtCore.Qt.AlignCenter)

        #アーム長
        self.label_L = QtGui.QLabel('armLength',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.le_L = QtGui.QLineEdit('6500',Dialog)
        self.le_L.setGeometry(QtCore.QRect(110, 60, 50, 20))
        self.le_L.setAlignment(QtCore.Qt.AlignCenter)

        #アーム幅
        self.label_W = QtGui.QLabel('armWidth',Dialog)
        self.label_W.setGeometry(QtCore.QRect(10, 88, 100, 22))
        self.le_W = QtGui.QLineEdit('800',Dialog)
        self.le_W.setGeometry(QtCore.QRect(110, 85, 50, 20))
        self.le_W.setAlignment(QtCore.Qt.AlignCenter)

        #ブレード位置
        self.label_br = QtGui.QLabel('bradePosition',Dialog)
        self.label_br.setGeometry(QtCore.QRect(10, 113, 100, 22))
        self.le_br = QtGui.QLineEdit('800',Dialog)
        self.le_br.setGeometry(QtCore.QRect(110, 110, 50, 20))
        self.le_br.setAlignment(QtCore.Qt.AlignCenter)

        #ブレード間隔
        self.label_brs = QtGui.QLabel('bradeSpasing',Dialog)
        self.label_brs.setGeometry(QtCore.QRect(10, 138, 100, 22))
        self.le_brs = QtGui.QLineEdit('1000',Dialog)
        self.le_brs.setGeometry(QtCore.QRect(110, 135, 50, 20))
        self.le_brs.setAlignment(QtCore.Qt.AlignCenter)

        #ブレード数
        self.label_n0 = QtGui.QLabel('nomberOfbrade',Dialog)
        self.label_n0.setGeometry(QtCore.QRect(10, 163, 100, 22))
        self.le_n0 = QtGui.QLineEdit('5',Dialog)
        self.le_n0.setGeometry(QtCore.QRect(110, 160, 50, 20))
        self.le_n0.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 185, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 185, 60, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 210, 150, 22))
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 235, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)

        fname='rakeArm.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "rakeArm", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  
        
    def read_data(self):
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         print(obj.Label)
                         spreadsheet = obj
                         
                         self.le_H.setText(spreadsheet.getContents('H0')) 
                         self.le_L.setText(spreadsheet.getContents('L0')) 
                         self.le_h1.setText(spreadsheet.getContents('h1')) 
                         self.le_W.setText(spreadsheet.getContents('W0')) 
                         self.le_br.setText(spreadsheet.getContents('br')) 
                         self.le_n0.setText(spreadsheet.getContents('n00')) 
                         self.le_brs.setText(spreadsheet.getContents('brs')) 
                         
                          
    def update(self):
         
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj
                         
                         H=self.le_H.text()#梁成
                         L=self.le_L.text()#梁長
                         h1=self.le_h1.text()#梁長
                         W=self.le_W.text()
                         l1=float(L)-2*(float(H)-float(h1))
                         br=self.le_br.text()
                         n00=self.le_n0.text()
                         brs=self.le_brs.text()
                         
                         #print(l1)
                         #タテラチス個数
                         p0=float(H)
                         n=(float(L)-2*(float(H)-float(h1)))/p0
                         n=int(n)
                         for n in range(1,100):
                             rp03=l1/n
                             if float(rp03)<=float(H):
                                 break
                         n0=n 
                         p0=(l1-75)/n0
                         
                         sita=math.atan(float(H)/(p0+75))*57.3
                         lx=30*math.cos((sita)/57.3)
                         lz=30*math.sin((sita)/57.3)
                         l2=(float(H)**2+float(p0)**2)**0.5
                         #print('aaaaaaaaaaaaaaaaaaaa')
                         spreadsheet.set('L0',L)
                         spreadsheet.set('H0',H)
                         spreadsheet.set('h1',h1)
                         spreadsheet.set('W0',W)
                         spreadsheet.set('p0',str(p0))
                         spreadsheet.set('n0',str(n0+1))
                         spreadsheet.set('sita',str(sita))
                         spreadsheet.set('l2',str(l2))
                         spreadsheet.set('lx',str(lx))
                         spreadsheet.set('lz',str(lz))
                         spreadsheet.set('br',str(br))
                         spreadsheet.set('n00',str(n00))
                         spreadsheet.set('brs',str(brs))
                         
                         App.ActiveDocument.recompute() 
                                
                         return

    def create(self): 
         fname='rakeAssy.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, fname) 
         Gui.ActiveDocument.mergeProject(joined_path)

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