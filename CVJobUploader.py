# Form implementation generated from reading ui file 'CVJobUploader.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(688, 328)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(320, 30, 341, 241))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.frame.setLineWidth(3)
        self.frame.setObjectName("frame")
        self.jobLabel = QtWidgets.QLabel(parent=self.frame)
        self.jobLabel.setGeometry(QtCore.QRect(10, 10, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.jobLabel.setFont(font)
        self.jobLabel.setObjectName("jobLabel")
        self.phaseLabel = QtWidgets.QLabel(parent=self.frame)
        self.phaseLabel.setGeometry(QtCore.QRect(10, 40, 321, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.phaseLabel.setFont(font)
        self.phaseLabel.setObjectName("phaseLabel")
        self.label_4 = QtWidgets.QLabel(parent=self.frame)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 47, 13))
        self.label_4.setObjectName("label_4")
        self.submitCVJ = QtWidgets.QPushButton(parent=self.frame)
        self.submitCVJ.setGeometry(QtCore.QRect(10, 190, 321, 23))
        self.submitCVJ.setObjectName("submitCVJ")
        self.otherCheckBox = QtWidgets.QCheckBox(parent=self.frame)
        self.otherCheckBox.setGeometry(QtCore.QRect(130, 120, 51, 17))
        self.otherCheckBox.setChecked(True)
        self.otherCheckBox.setObjectName("otherCheckBox")
        self.standardCheckBox = QtWidgets.QCheckBox(parent=self.frame)
        self.standardCheckBox.setGeometry(QtCore.QRect(10, 120, 71, 17))
        self.standardCheckBox.setObjectName("standardCheckBox")
        self.draftCheckBox = QtWidgets.QCheckBox(parent=self.frame)
        self.draftCheckBox.setGeometry(QtCore.QRect(80, 120, 51, 17))
        self.draftCheckBox.setObjectName("draftCheckBox")
        self.errorTag = QtWidgets.QLabel(parent=self.frame)
        self.errorTag.setGeometry(QtCore.QRect(10, 170, 141, 16))
        self.errorTag.setObjectName("errorTag")
        self.lotDropDown = QtWidgets.QComboBox(parent=self.frame)
        self.lotDropDown.setGeometry(QtCore.QRect(10, 90, 251, 20))
        self.lotDropDown.setObjectName("lotDropDown")
        self.cvjStatusLabel = QtWidgets.QLabel(parent=self.frame)
        self.cvjStatusLabel.setGeometry(QtCore.QRect(269, 91, 60, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.cvjStatusLabel.setFont(font)
        self.cvjStatusLabel.setAutoFillBackground(False)
        self.cvjStatusLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cvjStatusLabel.setObjectName("cvjStatusLabel")
        self.jobIDSubmit = QtWidgets.QPushButton(parent=self.centralwidget)
        self.jobIDSubmit.setGeometry(QtCore.QRect(220, 120, 61, 23))
        self.jobIDSubmit.setObjectName("jobIDSubmit")
        self.jobIDInput = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.jobIDInput.setGeometry(QtCore.QRect(30, 120, 181, 20))
        self.jobIDInput.setObjectName("jobIDInput")
        self.label_5 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 100, 171, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 688, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CV Job Upload Tool"))
        self.label.setText(_translate("MainWindow", "CV Job Uploader"))
        self.jobLabel.setText(_translate("MainWindow", "K Hov - Aguila at Terra Lago"))
        self.phaseLabel.setText(_translate("MainWindow", "Phase: 2"))
        self.label_4.setText(_translate("MainWindow", "Lots"))
        self.submitCVJ.setText(_translate("MainWindow", "Submit CVJ"))
        self.otherCheckBox.setText(_translate("MainWindow", "Other"))
        self.standardCheckBox.setText(_translate("MainWindow", "Standard"))
        self.draftCheckBox.setText(_translate("MainWindow", "Draft"))
        self.errorTag.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">Plan Number is invalid</span></p></body></html>"))
        self.cvjStatusLabel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#d9a03e;\">CVJ Exists</span></p></body></html>"))
        self.jobIDSubmit.setText(_translate("MainWindow", "Submit"))
        self.label_5.setText(_translate("MainWindow", "Enter Job ID"))
