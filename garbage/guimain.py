# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'example/src/gui/main.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 575)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.text_list = QtWidgets.QListWidget(self.centralwidget)
        self.text_list.setGeometry(QtCore.QRect(10, 10, 601, 431))
        self.text_list.setObjectName("text_list")
        self.text_list.setSpacing(2)
        self.text_list.setWordWrap(True)

        self.user_list = QtWidgets.QListWidget(self.centralwidget)
        self.user_list.setGeometry(QtCore.QRect(620, 10, 171, 431))
        self.user_list.setObjectName("user_list")

        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(620, 450, 171, 31))
        self.send_button.setObjectName("send_button")

        self.file_button = QtWidgets.QPushButton(self.centralwidget)
        self.file_button.setGeometry(QtCore.QRect(620, 490, 171, 31))
        self.file_button.setObjectName("file_button")

        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(620, 530, 171, 31))
        self.exit_button.setObjectName("exit_button")

        self.message_text = QtWidgets.QTextEdit(self.centralwidget)
        self.message_text.setGeometry(QtCore.QRect(10, 450, 601, 111))
        self.message_text.setObjectName("message_text")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.send_button.setText(_translate("MainWindow", "Отправить"))
        self.file_button.setText(_translate("MainWindow", "Прикрепить файл"))
        self.exit_button.setText(_translate("MainWindow", "Выход"))
