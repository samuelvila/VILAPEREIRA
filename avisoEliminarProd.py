# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'avisoEliminarProd.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_avisoEliminarProd(object):
    def setupUi(self, avisoEliminarProd):
        avisoEliminarProd.setObjectName("avisoEliminarProd")
        avisoEliminarProd.resize(400, 300)
        self.btnConfirmElimProd = QtWidgets.QDialogButtonBox(avisoEliminarProd)
        self.btnConfirmElimProd.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.btnConfirmElimProd.setOrientation(QtCore.Qt.Horizontal)
        self.btnConfirmElimProd.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.btnConfirmElimProd.setCenterButtons(True)
        self.btnConfirmElimProd.setObjectName("btnConfirmElimProd")
        self.label = QtWidgets.QLabel(avisoEliminarProd)
        self.label.setGeometry(QtCore.QRect(70, 50, 261, 81))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(avisoEliminarProd)
        self.label_2.setGeometry(QtCore.QRect(160, 140, 61, 61))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(avisoEliminarProd)
        self.btnConfirmElimProd.accepted.connect(avisoEliminarProd.accept)
        self.btnConfirmElimProd.rejected.connect(avisoEliminarProd.reject)
        QtCore.QMetaObject.connectSlotsByName(avisoEliminarProd)

    def retranslateUi(self, avisoEliminarProd):
        _translate = QtCore.QCoreApplication.translate
        avisoEliminarProd.setWindowTitle(_translate("avisoEliminarProd", "Dialog"))
        self.label.setText(_translate("avisoEliminarProd", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">¿ ESTÁ SEGURO DE ELIMINAR</span></p><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\"> EL PRODUCTO ?</span></p></body></html>"))
        self.label_2.setText(_translate("avisoEliminarProd", "<html><head/><body><p><img src=\":/avisomod/avisos1.jpg\"/></p></body></html>"))
import avisomod_rc