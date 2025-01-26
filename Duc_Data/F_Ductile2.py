# -*- coding: utf-8 -*-
import os
from sys import exit, argv
from PySide2.QtWidgets import QApplication, QLabel, QComboBox, QLineEdit, QPushButton
from FreeCAD import Base
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft


doc=App.ActiveDocument
class Main():
    def __init__(self):
        super().__init__()
        self.tile='F形鋳鉄管'
        self.left=10
        self.top=10
        self.width=300
        self.height=300
        """
        self.label = QtWidgets.QLabel(qdialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 61, 16))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(qdialog)
        self.comboBox.setGeometry(QtCore.QRect(110, 20, 271, 22))
        self.comboBox.setObjectName("comboBox")
        self.label_2 = QtWidgets.QLabel(qdialog)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 61, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(qdialog)
        self.label_3.setGeometry(QtCore.QRect(210, 50, 171, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(qdialog)
        self.label_4.setGeometry(QtCore.QRect(30, 80, 61, 16))
        self.label_4.setObjectName("label_4")
        self.comboBox_2 = QtWidgets.QComboBox(qdialog)
        self.comboBox_2.setGeometry(QtCore.QRect(110, 80, 69, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_5 = QtWidgets.QLabel(qdialog)
        self.label_5.setGeometry(QtCore.QRect(210, 80, 171, 16))
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAutoFillBackground(False)
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_5.setMidLineWidth(2)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(qdialog)
        self.label_6.setGeometry(QtCore.QRect(30, 120, 71, 16))
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtWidgets.QLineEdit(qdialog)
        self.lineEdit.setGeometry(QtCore.QRect(110, 120, 71, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(qdialog)
        self.pushButton.setGeometry(QtCore.QRect(210, 120, 171, 23))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_2 = QtWidgets.QLineEdit(qdialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 50, 71, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        #self.label_7 = QtWidgets.QLabel(qdialog)
        #self.label_7.setGeometry(QtCore.QRect(39, 161, 341, 111))
        #self.label_7.setText("")
        #self.label_7.setPixmap(QtGui.QPixmap("img_f01.png"))
        #self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        #self.label_7.setObjectName("label_7")


        """

        self.initUI()
    def initUI(self):

        self.setWindowTitle(self.tile)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.show


if __name__ == '__main__':
	app = QApplication(sys.argv)
    Main()
    sys.exit(app.exec_())
