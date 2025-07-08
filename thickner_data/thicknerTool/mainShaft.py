# -*- coding: utf-8 -*-
import os
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 250)
        Dialog.move(1000, 0)
        #シャフト全長   
        self.label_L = QtGui.QLabel('mainShaft full Length',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 38, 120, 12))
        self.le_L = QtGui.QLineEdit('6800',Dialog)
        self.le_L.setGeometry(QtCore.QRect(170, 35, 50, 20))
        self.le_L.setAlignment(QtCore.Qt.AlignCenter)
        #レーキ位置
        self.label_rp = QtGui.QLabel('rake Position',Dialog)
        self.label_rp.setGeometry(QtCore.QRect(10, 63, 100, 12))
        self.le_rp = QtGui.QLineEdit('1000',Dialog)
        self.le_rp.setGeometry(QtCore.QRect(170, 60, 50, 20))
        self.le_rp.setAlignment(QtCore.Qt.AlignCenter)
        #レーキブラケットCtoC
        self.label_rbc = QtGui.QLabel('rake Bracket CtoC',Dialog)
        self.label_rbc.setGeometry(QtCore.QRect(10, 88, 100, 12))
        self.le_rbc = QtGui.QLineEdit('684',Dialog)
        self.le_rbc.setGeometry(QtCore.QRect(170, 85, 50, 20))
        self.le_rbc.setAlignment(QtCore.Qt.AlignCenter)
        #スキマー位置
        self.label_sp = QtGui.QLabel('skimmerBrade Psition',Dialog)
        self.label_sp.setGeometry(QtCore.QRect(10, 113, 170, 12))
        self.le_sp = QtGui.QLineEdit('5500',Dialog)
        self.le_sp.setGeometry(QtCore.QRect(170, 110, 50, 20))
        self.le_sp.setAlignment(QtCore.Qt.AlignCenter)
        #スキマーブラケットCtoC
        self.label_skb = QtGui.QLabel('skimmer Bracket CtoC',Dialog)
        self.label_skb.setGeometry(QtCore.QRect(10, 138, 170, 12))
        self.le_skb = QtGui.QLineEdit('800',Dialog)
        self.le_skb.setGeometry(QtCore.QRect(170, 135, 50, 20))
        self.le_skb.setAlignment(QtCore.Qt.AlignCenter)
         #レーキターンバックル間隔
        self.label_rts = QtGui.QLabel('rake Turnbackle spacing',Dialog)
        self.label_rts.setGeometry(QtCore.QRect(10, 163, 170, 12))
        self.le_rts = QtGui.QLineEdit('1000',Dialog)
        self.le_rts.setGeometry(QtCore.QRect(170, 160, 50, 20))
        self.le_rts.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 185, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 185, 80, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 210, 170, 22))

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "mainShaft", None))
        
    def read_data(self):
         global spreadsheet
         selection = Gui.Selection.getSelection()
          # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj
                         self.le_L.setText(spreadsheet.getContents('L0'))
                         self.le_rp.setText(spreadsheet.getContents('lk'))
                         self.le_rbc.setText(spreadsheet.getContents('rbw'))
                         self.le_sp.setText(spreadsheet.getContents('ls'))
                         self.le_skb.setText(spreadsheet.getContents('sbw'))
                         self.le_rts.setText(spreadsheet.getContents('rts'))

    def update(self):
         L0=self.le_L.text()
         lk=self.le_rp.text()
         rbw=self.le_rbc.text()
         ls=self.le_sp.text()
         sbw=self.le_skb.text()
         rts=self.le_rts.text()

         spreadsheet.set('L0',str(L0))
         spreadsheet.set('lk',str(lk))
         spreadsheet.set('rbw',str(rbw))
         spreadsheet.set('ls',str(ls))
         spreadsheet.set('sbw',str(sbw))
         spreadsheet.set('rts',str(rts))

         App.ActiveDocument.recompute() 

    def create(self): 
        fname='mainShaft.FCStd'
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