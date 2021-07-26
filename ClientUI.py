# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClientUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(900, 600))
        MainWindow.setSizeIncrement(QtCore.QSize(900, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(900, 550))
        self.centralwidget.setMaximumSize(QtCore.QSize(900, 550))
        self.centralwidget.setSizeIncrement(QtCore.QSize(900, 550))
        self.centralwidget.setBaseSize(QtCore.QSize(900, 550))
        self.centralwidget.setObjectName("centralwidget")
        self.Video_label = QtWidgets.QLabel(self.centralwidget)
        self.Video_label.setGeometry(QtCore.QRect(30, 30, 640, 480))
        self.Video_label.setAutoFillBackground(True)
        self.Video_label.setText("")
        self.Video_label.setObjectName("Video_label")
        self.PlateLabel = QtWidgets.QLabel(self.centralwidget)
        self.PlateLabel.setGeometry(QtCore.QRect(520, 50, 350, 120))
        self.PlateLabel.setAutoFillBackground(True)
        self.PlateLabel.setText("")
        self.PlateLabel.setObjectName("PlateLabel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(530, 60, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 20, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(680, 340, 81, 21))
        self.label_3.setObjectName("label_3")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setGeometry(QtCore.QRect(770, 340, 91, 22))
        self.doubleSpinBox.setDecimals(0)
        self.doubleSpinBox.setMinimum(1.0)
        self.doubleSpinBox.setMaximum(255.0)
        self.doubleSpinBox.setProperty("value", 220.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(780, 180, 101, 41))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(660, 180, 101, 41))
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(680, 370, 181, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(680, 430, 181, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Plate"))
        self.label_2.setText(_translate("MainWindow", "Car"))
        self.label_3.setText(_translate("MainWindow", "processing rate"))
        self.label_4.setText(_translate("MainWindow", "NULL"))
        self.label_5.setText(_translate("MainWindow", "Load on System:"))
        self.pushButton.setText(_translate("MainWindow", "Active Processor Unit"))
        self.pushButton_2.setText(_translate("MainWindow", "Stop Processor Unit"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionClose.setText(_translate("MainWindow", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
