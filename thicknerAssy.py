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
import FreeCAD

thickner_series=['13_0m','13_5m','14_0m','14_5m','15_0m','15_5m','16_0m','16_5m','17_0m',
                 '17_5m','18_0m','18_5m','19_0m','19_5m','20_0m',]

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

        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'Thickner', None))
         
    def create(self):
         doc=App.activeDocument()
         mypath=self.comboBox_Series.currentText()
         key=self.comboBox_Series.currentIndex()
         if key<=4:
             fname='suspend_thickner_' + mypath + '.FCStd'
             mypath2='suspended_type_thickner'
         elif key>4:
             fname='pillar_thickner_'+mypath+'.FCStd'
             mypath2='pillar_type_thickner'
         
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'Sewage_eqp_data',mypath2,mypath,fname)
         #try:
         #    joined_path = os.path.join(base, 'Sewage_eqp_data',mypath2,mypath,fname) 
         #    print(joined_path)
         #    Gui.ActiveDocument.mergeProject(joined_path) 
         #except:
         #     print('aaaaaaaaaaa')
         #     pass
         #Gui.SendMsgToActiveView("ViewFit")
          # --- インポート前のオブジェクトリストを取得 ---
         old_obj_names = [o.Name for o in doc.Objects]
         
         # マージ実行
         Gui.ActiveDocument.mergeProject(joined_path)
         doc.recompute() # 一旦再計算して内部IDを確定させる
         # --- インポート後に増えたオブジェクトを特定 ---
         new_objs = [o for o in doc.Objects if o.Name not in old_obj_names]
         
         if not new_objs:
             print("Error: オブジェクトが読み込まれませんでした。")
             return
         #latticeBeamというラベルを持つものを優先的に探す
         move_target = None
         for o in new_objs:
             if "suspend"  in o.Label[:7] or "suspend"  in o.Name[:7]:
                 move_target = o
             elif "pillar"  in o.Label[:6] or "pillar"  in o.Name[:6]:
                 move_target = o    
         
         # 見つからなければ、新しく入ってきた最初のオブジェクトをターゲットにする
         if not move_target:
             move_target = new_objs[0]
         view = Gui.ActiveDocument.ActiveView
         callbacks = {}
         def move_cb(info):
             pos = info["Position"]
             # 重要：ビュー平面上の3D座標を取得
             p = view.getPoint(pos)
             if move_target:
                 move_target.Placement.Base = p
                 #view.softRedraw()
         def click_cb(info):
             if info["State"] == "DOWN" and info["Button"] == "BUTTON1":
                 # コールバック解除
                 view.removeEventCallback("SoLocation2Event", callbacks["move"])
                 view.removeEventCallback("SoMouseButtonEvent", callbacks["click"])
                 App.ActiveDocument.recompute()
                 print("Placed: " + move_target.Label)
         # イベント登録
         callbacks["move"] = view.addEventCallback("SoLocation2Event", move_cb)
         callbacks["click"] = view.addEventCallback("SoMouseButtonEvent", click_cb)

         
    def setParts(self):
         global mainShaft
         global skimmerBrade  
         global centerCage
         global rake
        
         # ドキュメントを取得
         doc = App.activeDocument()
         if doc:
             group_names = []
             for obj in doc.Objects:
                 if obj.Label[:9]=='mainShaft':
                      mainShaft=obj
                      print(mainShaft.Placement) 
                 elif obj.Label[:12]=='skimmerBrade':
                      skimmerBrade=obj 
                 elif obj.Label[:4]=='rake':
                      rake=obj      

                 elif obj.Label=='センターケージ':  
                      centerCage=obj
                 elif obj.Label=='レーキ':
                      rake=obj        
         

    def spinMove(self):
         
         key=self.comboBox_Series.currentIndex()
         r1 = 3*self.spinBox.value()
         try:
             if key<=4:
                 mainShaft.Placement.Rotation=App.Rotation(App.Vector(0,0,1),-r1)
                 skimmerBrade.Placement.Rotation=App.Rotation(App.Vector(0,0,1),-r1)
                 App.ActiveDocument.recompute()
             elif key>4:
                 centerCage.Placement.Rotation=App.Rotation(App.Vector(0,0,1),-r1) 
                 rake.Placement.Rotation=App.Rotation(App.Vector(0,0,1),-r1)
                 App.ActiveDocument.recompute()
         except:
              pass      
         App.ActiveDocument.recompute()
         

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        # スクリプトのウィンドウを取得
        #script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        ## 閉じるボタンを無効にする
        #script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)               