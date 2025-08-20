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
import FreeCAD
import csv

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
        #import
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(180, 110, 100, 22))
        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(30, 135, 260, 250))
        self.img.setAlignment(QtCore.Qt.AlignTop)

        #質量計算
        self.pushButton_m = QtGui.QPushButton('massCulculation',Dialog)
        self.pushButton_m.setGeometry(QtCore.QRect(30, 280, 100, 23))
        self.pushButton_m.setObjectName("pushButton")  
        
        #質量集計_spreadsheet
        self.pushButton_m2 = QtGui.QPushButton('massTally_spreadsheet',Dialog)
        self.pushButton_m2.setGeometry(QtCore.QRect(130, 280, 130, 23))
        self.pushButton_m2.setObjectName("pushButton")
        
        #質量入力
        self.pushButton_m3 = QtGui.QPushButton('massImput[kg]',Dialog)
        self.pushButton_m3.setGeometry(QtCore.QRect(30, 330, 100, 23))
        self.pushButton_m3.setObjectName("pushButton")  
        self.le_mass = QtGui.QLineEdit(Dialog)
        self.le_mass.setGeometry(QtCore.QRect(130, 330, 50, 20))
        self.le_mass.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_mass.setText('10.0')
        #密度
        self.lbl_gr = QtGui.QLabel('SpecificGravity',Dialog)
        self.lbl_gr.setGeometry(QtCore.QRect(30, 355, 80, 12))
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(130, 355, 50, 20))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr.setText('7.85')


        self.comboBox_Eqp.addItems(Eqp)
        self.comboBox_Eqp.setCurrentIndex(1)
        self.comboBox_Eqp.currentIndexChanged[int].connect(self.onEqp)
        self.comboBox_Eqp.setCurrentIndex(0)

        self.comboBox_Type.setCurrentIndex(1) 
        self.comboBox_Type.currentIndexChanged[int].connect(self.onType)
        self.comboBox_Type.setCurrentIndex(0) 

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.create2)#tool
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.setParts)

        QtCore.QObject.connect(self.pushButton_m, QtCore.SIGNAL("pressed()"), self.massCulc)
        QtCore.QObject.connect(self.pushButton_m2, QtCore.SIGNAL("pressed()"), self.massTally)
        QtCore.QObject.connect(self.pushButton_m3, QtCore.SIGNAL("pressed()"), self.massImput)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'thicknerWB', None))
        pass
    def setParts(self):
        global Spreadsheet_Assy
        global rakeAssy
        global rakeTurnBackle
        doc = FreeCAD.activeDocument()
        if doc:
             group_names = []
             for obj in doc.Objects:
                 if obj.Label[:13] == "Spreadsheet_Assy":
                     Spreadsheet_Assy = obj
                 elif obj.Label=='rakeAssy':
                     rakeAssy=obj  
                 elif obj.Label=='rakeTurnBackle':
                     rakeTurnBackle=obj      
    def massImput(self):
         # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g=float(self.le_mass.text())
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g

    def massCulc(self):
        # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g0=float(self.le_gr.text())
        g=obj.Shape.Volume*g0*1000/10**9  
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g
            pass
    
    def massTally(self):#spreadsheet
        doc = App.ActiveDocument
        # 新しいスプレッドシートを作成
        spreadsheet = doc.addObject("Spreadsheet::Sheet", "Parts_List")
        spreadsheet.Label = "Parts_List"
        # ヘッダー行を記入
        headers = ['No',"Name",'Standard', 'Count','Unit[kg]','Mass[kg]']
        for header in enumerate(headers):
            spreadsheet.set(f"A{1}", headers[0])
            spreadsheet.set(f"B{1}", headers[1])
            spreadsheet.set(f"C{1}", headers[2])
            spreadsheet.set(f"D{1}", headers[3])
            spreadsheet.set(f"E{1}", headers[4])
            spreadsheet.set(f"F{1}", headers[5])
        # パーツを列挙して情報を書き込む
        row = 2
        i=1
        s=0
        for i,obj in enumerate(doc.Objects):
            if  obj.Label[:7]=='Channel' or obj.Label[:5]=='Angle' \
                or obj.Label[:5]=='Coner' or obj.Label[:7]=='Extrude' or obj.Label[:6]=='Fusion' or obj.Label[:6]=='Corner' or obj.Label[:6]=='Square' \
                    or obj.Label[:5]=='_basic' or obj.Label[:4]=='Edge' or obj.Label[:3]=='hub' or obj.Label[:7]=='_8_tube'\
                        or obj.Label[:5]=='plate' or obj.Label[:6]=='keyway' or obj.Label[:4]=='tube' or obj.Label[:5]=='color'\
                            or obj.Label[:7]=='H_Shape' or obj.Label[:6]=='HShape' or obj.Label[:4]=='mShp' or obj.Label[:4]=='hShp' or obj.Label[:4]=='LShp':
                pass        
            else:  
                try:
                    spreadsheet.set(f"E{row}", f"{obj.mass:.2f}")  # Unit
                    #s=obj.mass+s
                    #if hasattr(obj, "Shape") and obj.Shape.Volume > 0.01:
                    if hasattr(obj, "mass") and obj.mass > 0.01:
                        try:
                            spreadsheet.set(f"A{row}", str(row-1))  # No
                            spreadsheet.set(f"B{row}", obj.Label)   #Name
                            try:
                                spreadsheet.set(f"C{row}", obj.dia)
                            except:
                                pass
                            if obj.Label=='rakeAssy':
                                n=2
                            else:
                                n=1    
                            spreadsheet.set(f"D{row}", str(n))   # count
                            g=round(obj.mass*n,2)
                            spreadsheet.set(f"F{row}", str(g))   # g
                            s=g+s 
                            row += 1
                        except:
                            print('error')
                            pass   
                    else:
                        pass    
                except:
                    pass   
                spreadsheet.set(f'F{row}',str(s))
        App.ActiveDocument.recompute()
        Gui.activeDocument().activeView().viewAxometric()   

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
              joined_path = os.path.join(base, "thickner_data",mypath,pic)
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
             joined_path = os.path.join(base, "thickner_data",mypath,pic)
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
            joined_path = os.path.join(base, 'thickner_data',key2,mypath,fname) 
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
        
           