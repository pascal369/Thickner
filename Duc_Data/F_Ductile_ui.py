# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F_Ductile.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PySide import QtCore, QtGui, QtWidgets


class Ui_qdialog(object):
    def setupUi(self, qdialog):
        qdialog.setObjectName("qdialog")
        qdialog.resize(402, 289)
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
        self.label_7 = QtWidgets.QLabel(qdialog)
        self.label_7.setGeometry(QtCore.QRect(39, 161, 341, 111))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("img_f01.png"))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")

        self.retranslateUi(qdialog)
        QtCore.QMetaObject.connectSlotsByName(qdialog)

    def retranslateUi(self, qdialog):
        _translate = QtCore.QCoreApplication.translate
        qdialog.setWindowTitle(_translate("qdialog", "F_type JDPA A300 v1.0"))
        self.label.setText(_translate("qdialog", "F形異形管"))
        self.label_2.setText(_translate("qdialog", "切管長[mm]"))
        self.label_3.setText(_translate("qdialog", "Label3"))
        self.label_4.setText(_translate("qdialog", "呼び径"))
        self.label_5.setText(_translate("qdialog", "Create"))
        self.label_6.setText(_translate("qdialog", "License Key"))
        self.pushButton.setText(_translate("qdialog", "ライセンスキーを記憶する。"))
