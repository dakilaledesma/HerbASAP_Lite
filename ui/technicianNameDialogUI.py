# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/technicianNamesUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_technicianNameDialog(object):
    def setupUi(self, technicianNameDialog):
        technicianNameDialog.setObjectName("technicianNameDialog")
        technicianNameDialog.setWindowModality(QtCore.Qt.NonModal)
        technicianNameDialog.resize(302, 305)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        technicianNameDialog.setFont(font)
        technicianNameDialog.setStyleSheet("font: 12pt \"Cantarell\";")
        self.verticalLayout = QtWidgets.QVBoxLayout(technicianNameDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget_technicianNames = QtWidgets.QListWidget(technicianNameDialog)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.listWidget_technicianNames.setFont(font)
        self.listWidget_technicianNames.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.listWidget_technicianNames.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget_technicianNames.setProperty("showDropIndicator", False)
        self.listWidget_technicianNames.setAlternatingRowColors(True)
        self.listWidget_technicianNames.setResizeMode(QtWidgets.QListView.Adjust)
        self.listWidget_technicianNames.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget_technicianNames.setModelColumn(0)
        self.listWidget_technicianNames.setObjectName("listWidget_technicianNames")
        self.verticalLayout.addWidget(self.listWidget_technicianNames)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_remove = QtWidgets.QPushButton(technicianNameDialog)
        self.pushButton_remove.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_remove.setFont(font)
        self.pushButton_remove.setObjectName("pushButton_remove")
        self.horizontalLayout.addWidget(self.pushButton_remove)
        self.pushButton_add = QtWidgets.QPushButton(technicianNameDialog)
        self.pushButton_add.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_add.setFont(font)
        self.pushButton_add.setFocusPolicy(QtCore.Qt.TabFocus)
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout.addWidget(self.pushButton_add)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_newTechnician = QtWidgets.QLineEdit(technicianNameDialog)
        self.lineEdit_newTechnician.setObjectName("lineEdit_newTechnician")
        self.horizontalLayout_2.addWidget(self.lineEdit_newTechnician)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(technicianNameDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(technicianNameDialog)
        self.pushButton_add.clicked.connect(technicianNameDialog.add_item)
        self.pushButton_remove.clicked.connect(technicianNameDialog.remove_item)
        self.buttonBox.accepted.connect(technicianNameDialog.accept)
        self.buttonBox.rejected.connect(technicianNameDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(technicianNameDialog)
        technicianNameDialog.setTabOrder(self.lineEdit_newTechnician, self.pushButton_add)
        technicianNameDialog.setTabOrder(self.pushButton_add, self.pushButton_remove)

    def retranslateUi(self, technicianNameDialog):
        _translate = QtCore.QCoreApplication.translate
        technicianNameDialog.setWindowTitle(_translate("technicianNameDialog", "Technicians"))
        self.listWidget_technicianNames.setSortingEnabled(False)
        self.pushButton_remove.setText(_translate("technicianNameDialog", "Remove Selected"))
        self.pushButton_add.setToolTip(_translate("technicianNameDialog", "Add to list"))
        self.pushButton_add.setText(_translate("technicianNameDialog", "Add New Name"))
