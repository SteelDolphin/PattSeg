# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(885, 605)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 861, 531))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 859, 529))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.button.setGeometry(QtCore.QRect(10, 10, 211, 31))
        self.button.setObjectName("button")
        self.plotWidget = QtWidgets.QGraphicsView(self.scrollAreaWidgetContents)
        self.plotWidget.setGeometry(QtCore.QRect(10, 50, 831, 461))
        self.plotWidget.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.plotWidget.setObjectName("plotWidget")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 885, 23))
        self.menubar.setStyleSheet("")
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setStyleSheet("")
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpenFile = QtWidgets.QAction(MainWindow)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionS = QtWidgets.QAction(MainWindow)
        self.actionS.setObjectName("actionS")
        self.menu.addAction(self.actionOpenFile)
        self.menu.addSeparator()
        self.menu_2.addAction(self.actionS)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button.setText(_translate("MainWindow", "Load and Process Image"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "关于"))
        self.actionOpenFile.setText(_translate("MainWindow", "打开文件"))
        self.actionS.setText(_translate("MainWindow", "help"))
