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
        MainWindow.resize(800, 541)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(800, 541))
        MainWindow.setSizeIncrement(QtCore.QSize(800, 500))
        MainWindow.setBaseSize(QtCore.QSize(800, 500))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(800, 500))
        self.centralwidget.setMaximumSize(QtCore.QSize(800, 500))
        self.centralwidget.setSizeIncrement(QtCore.QSize(800, 500))
        self.centralwidget.setBaseSize(QtCore.QSize(800, 500))
        self.centralwidget.setObjectName("centralwidget")
        self.Video_label = QtWidgets.QLabel(self.centralwidget)
        self.Video_label.setGeometry(QtCore.QRect(10, 10, 640, 480))
        self.Video_label.setAutoFillBackground(True)
        self.Video_label.setText("")
        self.Video_label.setObjectName("Video_label")
        self.PlateLabel = QtWidgets.QLabel(self.centralwidget)
        self.PlateLabel.setGeometry(QtCore.QRect(510, 30, 251, 81))
        self.PlateLabel.setAutoFillBackground(True)
        self.PlateLabel.setText("")
        self.PlateLabel.setObjectName("PlateLabel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(720, 10, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(660, 170, 47, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(660, 230, 81, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(670, 190, 91, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(670, 250, 91, 16))
        self.label_6.setObjectName("label_6")
        self.disconButton = QtWidgets.QPushButton(self.centralwidget)
        self.disconButton.setGeometry(QtCore.QRect(650, 370, 131, 31))
        self.disconButton.setObjectName("disconButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
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
        self.label_3.setText(_translate("MainWindow", "Car Type:"))
        self.label_4.setText(_translate("MainWindow", "Plate content:"))
        self.label_5.setText(_translate("MainWindow", "XXXXXXXXXXXXXXX"))
        self.label_6.setText(_translate("MainWindow", "XXXXXXXXXXXXXXX"))
        self.disconButton.setText(_translate("MainWindow", "Disconnect from server"))
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
