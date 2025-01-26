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

AShp_data=['40x40x5','50x50x6','65x65x6','75x75x6',
      '90x90x7','100x100x10','100x100x13']

CShp_data=['75x40x5','100x50x5','125x65x6','150x75x9','180x75x7']

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
        Dialog.resize(250, 475)
        Dialog.move(1000, 0)
        
        #主材
        self.label_mShp = QtGui.QLabel('主材 L-',Dialog)
        self.label_mShp.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_mShp = QtGui.QComboBox(Dialog)
        self.comboBox_mShp.setGeometry(QtCore.QRect(110, 10, 100, 22))

        #ラチス材
        self.label_LShp = QtGui.QLabel('ラチス材 L-',Dialog)
        self.label_LShp.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.comboBox_LShp = QtGui.QComboBox(Dialog)
        self.comboBox_LShp.setGeometry(QtCore.QRect(110, 35, 100, 22))
        #横架材
        self.label_hShp = QtGui.QLabel('横架材 [-',Dialog)
        self.label_hShp.setGeometry(QtCore.QRect(10, 63, 100, 12))
        self.comboBox_hShp = QtGui.QComboBox(Dialog)
        self.comboBox_hShp.setGeometry(QtCore.QRect(110, 60, 100, 22))

        #ケージ幅
        self.label_W = QtGui.QLabel('ケージ幅W',Dialog)
        self.label_W.setGeometry(QtCore.QRect(10, 88, 100, 22))
        self.le_W = QtGui.QLineEdit('1800',Dialog)
        self.le_W.setGeometry(QtCore.QRect(110, 85, 50, 20))
        self.le_W.setAlignment(QtCore.Qt.AlignCenter)

        #ケージ長
        self.label_L = QtGui.QLabel('ケージ長L',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 113, 100, 22))
        self.le_L = QtGui.QLineEdit('4900',Dialog)
        self.le_L.setGeometry(QtCore.QRect(110, 110, 50, 20))
        self.le_L.setAlignment(QtCore.Qt.AlignCenter)

        #ガセット厚
        self.label_Gt = QtGui.QLabel('ガセット厚',Dialog)
        self.label_Gt.setGeometry(QtCore.QRect(10, 138, 100, 22))
        self.le_Gt = QtGui.QLineEdit('6',Dialog)
        self.le_Gt.setGeometry(QtCore.QRect(110, 135, 50, 20))
        self.le_Gt.setAlignment(QtCore.Qt.AlignCenter)

        #ガセット寸法a
        self.label_Gta = QtGui.QLabel('ガセット a',Dialog)
        self.label_Gta.setGeometry(QtCore.QRect(10, 163, 100, 22))
        self.le_Gta = QtGui.QLineEdit('6',Dialog)
        self.le_Gta.setGeometry(QtCore.QRect(110, 160, 50, 20))
        self.le_Gta.setAlignment(QtCore.Qt.AlignCenter)

        #レーキ幅
        self.label_rw = QtGui.QLabel('rakeWidth',Dialog)
        self.label_rw.setGeometry(QtCore.QRect(10, 188, 100, 22))
        self.le_rw = QtGui.QLineEdit('800',Dialog)
        self.le_rw.setGeometry(QtCore.QRect(110, 185, 50, 20))
        self.le_rw.setAlignment(QtCore.Qt.AlignCenter)


        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 210, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 210, 60, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 235, 150, 22))
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 260, 235, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        


        self.comboBox_mShp.addItems(AShp_data)
        self.comboBox_mShp.setEditable(True)

        self.comboBox_LShp.addItems(AShp_data)
        self.comboBox_LShp.setEditable(True)

        self.comboBox_hShp.addItems(CShp_data)
        self.comboBox_hShp.setEditable(True)



        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)

        fname='centerCage.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "centerCage", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  
        
    def read_data(self):
         global mShp
         global LShp
         global hShp
         global spreadsheet
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     #print(obj.Label)
                     if obj.Label=="mShp":
                         mShp=obj
                     elif obj.Label[:4]=='LShp':
                         LShp=obj  
                     elif obj.Label=='hShp':
                         hShp=obj     
                     elif obj.Label=='Spreadsheet_centerCage':
                         spreadsheet = obj


                         self.comboBox_mShp.setCurrentText(spreadsheet.getContents('mShp')[1:])
                         self.comboBox_LShp.setCurrentText(spreadsheet.getContents('LShp')[1:])
                         self.comboBox_hShp.setCurrentText(spreadsheet.getContents('hShp')[1:])
                         self.le_W.setText(spreadsheet.getContents('W0')) 
                         self.le_L.setText(spreadsheet.getContents('L0')) 
                         self.le_Gt.setText(spreadsheet.getContents('gt')) 
                         self.le_Gta.setText(spreadsheet.getContents('Gta')) 
                         self.le_rw.setText(spreadsheet.getContents('rw')) 

                          
    def update(self):
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj
                         #print(hShp)
                         mShp_S=self.comboBox_mShp.currentText()#主材
                         LShp_S=self.comboBox_LShp.currentText()#ラチス材
                         hShp_S=self.comboBox_hShp.currentText()#横架材
                         #print(hShp.Label,hShp_S)
                         hShp.size=hShp_S
                         LShp.size=LShp_S
                         mShp.size=mShp_S
                         W0=self.le_W.text()#ケージ幅
                         L0=self.le_L.text()#ケージ長
                         gt=self.le_Gt.text()#ガセット幅
                         Gta=float(self.le_Gta.text())#がセットa
                         rw=self.le_rw.text()
                         #主材ゲージ 幅
                         for i in range(23,29):
                             mShp3=spreadsheet.getContents('A'+str(i))
                             #print(mShp3)
                             if mShp_S==mShp3[1:]:
                                 break
                         row_m=i
                         #print(row_m,mShp3,mShp) 
                         mg0=spreadsheet.getContents('C'+str(row_m))#主材ゲージ 
                         mb0=spreadsheet.getContents('B'+str(row_m))#主材幅
                         #print(mg0,mb0)
                         #ラチス材幅
                         for i in range(23,29):
                             LShp3=spreadsheet.getContents('A'+str(i))
                             if LShp_S==LShp3[1:]:
                                 print(LShp,LShp3[1:])
                                 break
                         row_L=i
                         Lb0=float(spreadsheet.getContents('B'+str(row_L)) )
                         #横架材幅
                         for i in range(23,29):
                             hShp3=spreadsheet.getContents('D'+str(i))
                             #print(hShp3[1:],hShp_S)
                             if hShp_S==hShp3[1:]:
                                 break
                         row_L=i 
                         Lh0=spreadsheet.getContents('E'+str(row_L)) 
                         hb0=spreadsheet.getContents('F'+str(row_L))
                         hg=float(Lh0)/2
                         #print(Lh0,hg)
                         n0=(float(L0)-float(Lh0))/(float(W0)-2*float(mg0))
                         n0=int(n0)+1
                         p0=float(L0)/n0-float(mb0)/2#分割ピッチ
                         sita=round((math.atan(float(p0)/(float(W0)-float(mg0)*2)))*57.3,1)
                         #print(p0,float(W0)-2*float(mg0),sita)
                         la=Gta-2*Lb0
                         lx=-float(W0)/2+float(mb0)/2-Lb0/2*math.sin(sita/57.3)+la*math.sin((90-sita)/57.3)
                         lz=hg+Lb0/2*math.cos(sita/57.3)+la*math.cos((90-sita)/57.3)
                         ll=((float(W0)-float(mb0))**2+p0**2)**0.5
                         spreadsheet.set('W0',W0)#ゲージ幅
                         spreadsheet.set('L0',L0)#梁長L0
                         spreadsheet.set('mShp',mShp_S)#主材
                         spreadsheet.set('LShp',LShp_S)#ラチス材
                         spreadsheet.set('hShp',hShp_S)#横架材
                         spreadsheet.set('gt',gt)#がセット厚
                         spreadsheet.set('Gta',str(Gta))#ガセットa
                         spreadsheet.set('sita',str(sita))#sita
                         spreadsheet.set('mg0',mg0)#主材ゲージ
                         spreadsheet.set('mb0',mb0)#主材幅
                         spreadsheet.set('lx',str(lx))#lx
                         spreadsheet.set('lz',str(lz))#lz
                         spreadsheet.set('ll',str(ll))#ll
                         spreadsheet.set('n0',str(n0))#n0
                         spreadsheet.set('hg',str(hg))
                         spreadsheet.set('hb0',str(hb0))
                         spreadsheet.set('p0',str(p0))
                         spreadsheet.set('Lb0',str(Lb0))
                         spreadsheet.set('rw',str(rw))
                         #print(Gta)
                         
                        
                         App.ActiveDocument.recompute() 
                                
                         return

    def create(self): 
         fname='centerCage.FCStd'
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