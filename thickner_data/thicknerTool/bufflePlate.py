# -*- coding: utf-8 -*-
import os
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore

tank_data=['13000','13500','14000','14500','15000','15500','16000','16500','17000',
           '17500','18000','18500','19000','19500','20000']

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 150)
        Dialog.move(1000, 0)

        #槽径
        self.label_D = QtGui.QLabel('tankDia',Dialog)
        self.label_D.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_D = QtGui.QComboBox(Dialog)
        self.comboBox_D.setGeometry(QtCore.QRect(110, 10, 100, 22))
        #越流水路幅
        self.label_W = QtGui.QLabel('waterWay Width',Dialog)
        self.label_W.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.le_W = QtGui.QLineEdit('450',Dialog)
        self.le_W.setGeometry(QtCore.QRect(110, 35, 50, 20))
        self.le_W.setAlignment(QtCore.Qt.AlignCenter)
        #サポート数
        self.label_SN = QtGui.QLabel('nober of Support',Dialog)
        self.label_SN.setGeometry(QtCore.QRect(10, 63, 100, 12))
        self.le_SN = QtGui.QLineEdit('12',Dialog)
        self.le_SN.setGeometry(QtCore.QRect(110, 60, 50, 20))
        self.le_SN.setAlignment(QtCore.Qt.AlignCenter)
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 85, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 85, 60, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 110, 150, 22))

        self.comboBox_D.addItems(tank_data)
        self.comboBox_D.setEditable(True)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "buffulePlate", None))
        
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
                         #print('aaaaaaaaaaaaaaaaaaa')
                         spreadsheet = obj
                         self.comboBox_D.setCurrentText(spreadsheet.getContents('dia'))
                         self.le_W.setText(spreadsheet.getContents('W0'))
                         self.le_SN.setText(spreadsheet.getContents('n'))

    def update(self):
         dia=self.comboBox_D.currentText()
         W0=self.le_W.text()
         n=self.le_SN.text()
         spreadsheet.set('dia',str(dia))
         spreadsheet.set('W0',str(W0))
         spreadsheet.set('n',str(n))
         App.ActiveDocument.recompute() 
         

    def create(self): 
        fname='bufflePlate.FCStd'
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