# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/window.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(902, 714)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("gui/icon/chat.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(32, 32))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 901, 641))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.textList = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.textList.setObjectName("textList")
        self.verticalLayout.addWidget(self.textList)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.message = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHeightForWidth(self.message.sizePolicy().hasHeightForWidth())
        self.message.setSizePolicy(sizePolicy)
        self.message.setObjectName("message")
        self.horizontalLayout.addWidget(self.message)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.bSend = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bSend.sizePolicy().hasHeightForWidth())
        self.bSend.setSizePolicy(sizePolicy)
        self.bSend.setMinimumSize(QtCore.QSize(150, 40))
        self.bSend.setObjectName("bSend")
        self.verticalLayout_2.addWidget(self.bSend)

        self.bSendFile = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.bSendFile.setMinimumSize(QtCore.QSize(150, 40))
        self.bSendFile.setObjectName("bSendFile")
        self.verticalLayout_2.addWidget(self.bSendFile)

        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.mConnect = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("gui/icon/connect.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.mConnect.setIcon(icon1)
        self.mConnect.setObjectName("mConnect")

        self.mExit = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("gui/icon/exit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.mExit.setIcon(icon2)
        self.mExit.setObjectName("mExit")

        self.mInfo = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("gui/icon/info.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mInfo.setIcon(icon3)
        self.mInfo.setObjectName("mInfo")

        self.toolBar.addAction(self.mConnect)
        self.toolBar.addAction(self.mExit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.mInfo)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Главное окно"))
        self.bSend.setText(_translate("MainWindow", "Отправить"))
        self.bSendFile.setText(_translate("MainWindow", "Прикрепить файл"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.mConnect.setText(_translate("MainWindow", "Подключиться"))
        self.mExit.setText(_translate("MainWindow", "Выход"))
        self.mInfo.setText(_translate("MainWindow", "Информация"))
