# -*- coding: utf-8 -*-
import os
import sys
import FreeCADGui as Gui
from PySide import QtGui,QtCore
from FreeCAD import Base
import FreeCAD, Part , math
from math import pi
import FreeCAD as App
import FreeCADGui
from hdrl_data import ParamStraight
from hdrl_data import ParamEndLine
from hdrl_data import ParamCircular
from hdrl_data import ParamEdge
#from hdrl_data import ParamChannel
from hdrl_data import HandData
        
class ViewProvider:
    def __init__(self, obj):
        obj.Proxy = self
        return
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 480)
        Dialog.move(1000, 0)
        #タイプ
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(30, 15, 60, 12))
        self.label_type.setObjectName("label_type")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(90, 15, 160, 22))
        self.comboBox_type.setObjectName("comboBox_type")
        #仕様
        self.label_siyo = QtGui.QLabel('Spec',Dialog)
        self.label_siyo.setGeometry(QtCore.QRect(30, 40, 60, 12))
        self.label_siyo.setObjectName("label_st")
        self.comboBox_siyo = QtGui.QComboBox(Dialog)
        self.comboBox_siyo.setGeometry(QtCore.QRect(90, 40, 160, 22))
        self.comboBox_siyo.setObjectName("comboBox_st")

        #長さL1
        self.label_l1 = QtGui.QLabel('L1',Dialog)
        self.label_l1.setGeometry(QtCore.QRect(30, 67, 60, 12))
        self.spinBoxL1=QtGui.QSpinBox(Dialog)
        self.spinBoxL1.setGeometry(90, 65, 60, 40)
        self.spinBoxL1.setMinimum(100)  # 最小値
        self.spinBoxL1.setMaximum(50000)  # 最大値
        self.spinBoxL1.setValue(1500)  # 
        self.spinBoxL1.setSingleStep(10) #step
        self.spinBoxL1.setAlignment(QtCore.Qt.AlignCenter)
        #Step
        self.label_step = QtGui.QLabel('ステップ',Dialog)
        self.label_step.setGeometry(QtCore.QRect(30, 117, 50, 16))
        self.le_step = QtGui.QLineEdit('10',Dialog)
        self.le_step.setGeometry(QtCore.QRect(90, 115, 160, 16))
        self.le_step.setAlignment(QtCore.Qt.AlignCenter)
        


        #長さL2
        self.label_l2 = QtGui.QLabel('L2',Dialog)
        self.label_l2.setGeometry(QtCore.QRect(163, 67, 60, 12))
        
        self.spinBoxL2=QtGui.QSpinBox(Dialog)
        self.spinBoxL2.setGeometry(190, 65, 60, 40)
        self.spinBoxL2.setMinimum(100)  # 最小値
        self.spinBoxL2.setMaximum(50000)  # 最大値
        self.spinBoxL2.setValue(1500)  # 
        self.spinBoxL2.setSingleStep(10) #step
        self.spinBoxL2.setAlignment(QtCore.Qt.AlignCenter)

        #コーナー角度
        self.label_cn = QtGui.QLabel('angleK[deg]',Dialog)
        self.label_cn.setGeometry(QtCore.QRect(143, 142, 60, 12))
        self.label_cn.setObjectName("label_cn")
        self.lineEdit_cn = QtGui.QLineEdit(Dialog)
        self.lineEdit_cn.setGeometry(QtCore.QRect(207, 140, 43, 20))
        self.lineEdit_cn.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_cn.setObjectName("lineEdit_cn")
        #実行 Create
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(145, 160, 100, 22))
        #self.pushButton.setObjectName("pushButton")
        #更新 upDate
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(145, 185, 100, 22))
        #self.pushButton.setObjectName("pushButton")
        #import
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(145, 205, 100, 22))

        #リバース
        self.checkbox = QtGui.QCheckBox('Reverse',Dialog)
        self.checkbox.setGeometry(QtCore.QRect(30, 185, 60, 23))
        self.checkbox.setChecked(False)
        #手すり高
        self.label_l = QtGui.QLabel('height h',Dialog)
        self.label_l.setGeometry(QtCore.QRect(30, 142, 115, 20))
        self.label_l.setAlignment(QtCore.Qt.AlignLeft)
        self.label_l.setObjectName("label_l")
        self.lineEdit_l = QtGui.QLineEdit(Dialog)
        self.lineEdit_l.setGeometry(QtCore.QRect(90, 140, 50, 20))
        self.lineEdit_l.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_l.setObjectName("lineEdit_l")
        #手すりピッチ
        self.label_p = QtGui.QLabel('pitch p',Dialog)
        self.label_p.setGeometry(QtCore.QRect(30, 160, 115, 20))
        self.label_p.setAlignment(QtCore.Qt.AlignLeft)
        self.label_p.setObjectName("label_p")
        self.lineEdit_p = QtGui.QLineEdit(Dialog)
        self.lineEdit_p.setGeometry(QtCore.QRect(90, 160, 50, 20))
        self.lineEdit_p.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_p.setObjectName("lineEdit_p")
        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(50, 255, 200, 200))
        self.img.setAlignment(QtCore.Qt.AlignCenter)
        self.retranslateUi(Dialog)
        #比重
        self.mtrl = QtGui.QLabel('Specific gravity of material',Dialog)
        self.mtrl.setGeometry(QtCore.QRect(30, 235, 150, 12))
        self.le_mtrl = QtGui.QLineEdit(Dialog)
        self.le_mtrl.setGeometry(QtCore.QRect(185, 230, 60, 20))
        self.le_mtrl.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_type.addItems(HandData.type)
        self.comboBox_siyo.addItems(HandData.siyo)

        self.comboBox_siyo.setCurrentIndex(1)
        self.comboBox_siyo.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_siyo.setCurrentIndex(0)

        self.comboBox_type.currentIndexChanged[int].connect(self.on_type)
        self.lineEdit_l.setText(QtGui.QApplication.translate("Dialog", '1100', None))
        self.lineEdit_cn.setText(QtGui.QApplication.translate("Dialog", '90', None))
        self.lineEdit_p.setText(QtGui.QApplication.translate("Dialog", '1000', None))
        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_type.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.upDate)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        self.spinBoxL1.valueChanged[int].connect(self.spinMove) 
        self.spinBoxL2.valueChanged[int].connect(self.spinMove) 
       
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Handrail", None))

    def read_data(self):#管長
        
        selection = Gui.Selection.getSelection()
        for obj in selection:
            try:
                myShape=obj
                l1=(myShape.l1)
                #print('aaaaaaaaaaaaaaaaaaa')
                try:
                    l2=(myShape.l2)
                except:
                    pass
                #print('aaaaaaaaaaaaaaaaaaa')
                h=(myShape.h)
                p=(myShape.p)
                #print('aaaaaaaaaaaaaaaaaaa')
                
                self.spinBoxL1.setValue(int(l1))
                self.spinBoxL2.setValue(int(l2))
                self.lineEdit_l.setText(h)
                self.lineEdit_p.setText(p)

                self.comboBox_type.setCurrentText(myShape.type)
            except:
                myShape=None        
        App.ActiveDocument.recompute()   
        #Gui.runCommand('a2p_updateImportedParts',0)
    def upDate(self):
        selection = Gui.Selection.getSelection()
        for obj in selection:
            try:
                myShape=obj
                l1=self.spinBoxL1.value()
                l2=self.spinBoxL2.value()
                h=self.lineEdit_l.text()
                p=self.lineEdit_p.text()
                myShape.l1=l1
                myShape.l2=l2
                myShape.h=h
                myShape.p=p

            except:
                myShape=None 
        App.ActiveDocument.recompute()  
        #Gui.runCommand('a2p_updateImportedParts',0) 
    def spinMove(self):
        #print('aaaaaaaaaaaaaaaaaa')
        step=self.le_step.text()
        self.spinBoxL1.setSingleStep(int(step)) 
        self.spinBoxL2.setSingleStep(int(step))
        selection = Gui.Selection.getSelection()
        for obj in selection:
            try:
                myShape=obj
                l1=self.spinBoxL1.value()
                l2=self.spinBoxL2.value()
                myShape.l1=l1
                myShape.l2=l2
            except:
                myShape=None  
        #Gui.runCommand('a2p_updateImportedParts',0)        
        App.ActiveDocument.recompute()      
    def on_type(self):
        global key
        global spec_siyo
        
        key = self.comboBox_type.currentText()[:2]
        try:
            #l=float(self.lineEdit_l.text())
            h=float(self.lineEdit_l.text())
            l1=float(self.spinBoxL1.value())
            l2=float(self.spinBoxL2.value())
            k=float(self.lineEdit_cn.text())
            p=float(self.lineEdit_p.text())
            #print(p)

        except:
            pass

        spec_siyo=self.comboBox_siyo.currentIndex()

        if key=='00':
            pic=str(spec_siyo)+'_直線01L.jpg'

        elif key=='01':
            pic=str(spec_siyo)+'_端部01L.jpg'

        elif key=='02':
            pic=str(spec_siyo)+'_コーナー01L.jpg'

        elif key=='03':
            pic=str(spec_siyo)+'_arc01.jpg'

        elif key=='04':
           pic=str(spec_siyo)+'_edge01R.jpg'   

        elif key=='05':
           pic=str(spec_siyo)+'_edge01L.jpg'   

        elif key=='06':
           pic=str(spec_siyo)+'_channel01.jpg'  


        if spec_siyo < 2:
           self.le_mtrl.setText(QtGui.QApplication.translate("Dialog", "7.85", None))  
        else:
           self.le_mtrl.setText(QtGui.QApplication.translate("Dialog", "2.70", None))     

        try:
            base=os.path.dirname(os.path.abspath(__file__))
            joined_path = os.path.join(base, "hdrl_data",pic)
            self.img.setPixmap(QtGui.QPixmap(joined_path))
        except:
            pass    

    def create(self):
        global L0
        global l
        global h
        global l1
        global l2
        global k
        global p
        g0=float(self.le_mtrl.text())

        if key=='00':
            label='StraightLine'
        elif key=='01':
            label='Corner with end'
        elif key=='02':
            label='Corner' 
        elif key=='03':
            label='Circular_arc'   
        elif key=='04':
            label='Edge_R'   
        elif key=='05':
            label='Edge_L'  
        elif key=='06':
            label='Channel'   

        obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        obj.addProperty("App::PropertyEnumeration", "spec",label)
        obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
        obj.spec=HandData.siyo
        i=self.comboBox_siyo.currentIndex()
        obj.spec=HandData.siyo[i] 

        h=float(self.lineEdit_l.text())
        l1=float(self.spinBoxL1.value())
        p=float(self.lineEdit_p.text())

        if key=='03':
            pass
        else:
            l2=self.spinBoxL2.value()
        k=self.lineEdit_cn.text()
        obj.addProperty("App::PropertyFloat", "h",label).h=h
        obj.addProperty("App::PropertyFloat", "p",label).p=p
        if self.checkbox.isChecked():
            obj.addProperty("App::PropertyBool",'Reverse',label).Reverse = True
        else:
            obj.addProperty("App::PropertyBool",'Reverse',label).Reverse = False
            
        if key=='00' :
            obj.addProperty("App::PropertyFloat", "l1",label).l1=l1
            obj.addProperty("App::PropertyEnumeration", "type",label)
            obj.type=HandData.type
            i=self.comboBox_type.currentIndex()
            obj.type=HandData.type[i] 
            ParamStraight.StraightLine(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 
        elif key=='01' or key=='02' or key=='06':  
            
            obj.addProperty("App::PropertyFloat", "l1",label).l1=l1
            obj.addProperty("App::PropertyFloat", "l2",label).l2=float(l2)
            obj.addProperty("App::PropertyFloat", "k",label).k=float(k)
            obj.addProperty("App::PropertyEnumeration", "type",label)
            obj.type=HandData.type
            i=self.comboBox_type.currentIndex()
            obj.type=HandData.type[i] 
            ParamEndLine.EndLine(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 
        elif key=='03':
            obj.addProperty("App::PropertyFloat", "R",label).R=l1
            obj.addProperty("App::PropertyFloat", "k",label).k=float(k)
            obj.addProperty("App::PropertyEnumeration", "type",label)
            obj.type=HandData.type
            i=self.comboBox_type.currentIndex()
            obj.type=HandData.type[i] 
            ParamCircular.circular_arc(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()    
        elif key=='04' or key=='05':  
            obj.addProperty("App::PropertyEnumeration", "type",label)
            obj.type=HandData.type
            i=self.comboBox_type.currentIndex()
            obj.type=HandData.type[i] 
            ParamEdge.edge(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()  
            
        

class Main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()
        # スクリプトのウィンドウを取得
        script_window = FreeCADGui.getMainWindow().findChild(QtGui.QDialog, 'd')
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)





