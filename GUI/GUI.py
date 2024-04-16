# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TEST-GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.com_combo = QComboBox(self.centralwidget)
        self.com_combo.addItem("")
        self.com_combo.addItem("")
        self.com_combo.addItem("")
        self.com_combo.addItem("")
        self.com_combo.addItem("")
        self.com_combo.addItem("")
        self.com_combo.setObjectName(u"com_combo")
        self.com_combo.setGeometry(QRect(30, 90, 141, 31))
        font = QFont()
        font.setPointSize(16)
        self.com_combo.setFont(font)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 20, 201, 81))
        font1 = QFont()
        font1.setPointSize(26)
        self.label.setFont(font1)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(260, 20, 181, 71))
        self.label_2.setFont(font1)
        self.Baudrate_combo = QComboBox(self.centralwidget)
        self.Baudrate_combo.addItem("")
        self.Baudrate_combo.addItem("")
        self.Baudrate_combo.addItem("")
        self.Baudrate_combo.addItem("")
        self.Baudrate_combo.setObjectName(u"Baudrate_combo")
        self.Baudrate_combo.setGeometry(QRect(260, 90, 121, 31))
        self.Baudrate_combo.setFont(font)
        self.connect_button = QPushButton(self.centralwidget)
        self.connect_button.setObjectName(u"connect_button")
        self.connect_button.setGeometry(QRect(480, 70, 211, 81))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 210, 261, 41))
        self.label_3.setFont(font1)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 290, 271, 41))
        self.label_4.setFont(font1)
        self.command_combo = QComboBox(self.centralwidget)
        self.command_combo.addItem("")
        self.command_combo.addItem("")
        self.command_combo.addItem("")
        self.command_combo.addItem("")
        self.command_combo.addItem("")
        self.command_combo.addItem("")
        self.command_combo.addItem("")
        self.command_combo.setObjectName(u"command_combo")
        self.command_combo.setGeometry(QRect(320, 220, 211, 31))
        self.command_combo.setFont(font)
        self.rx_field = QTextEdit(self.centralwidget)
        self.rx_field.setObjectName(u"rx_field")
        self.rx_field.setGeometry(QRect(310, 290, 321, 41))
        self.send_button = QPushButton(self.centralwidget)
        self.send_button.setObjectName(u"send_button")
        self.send_button.setGeometry(QRect(550, 223, 131, 31))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.com_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.com_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.com_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.com_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.com_combo.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))
        self.com_combo.setItemText(5, QCoreApplication.translate("MainWindow", u"COM6", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"COM - PORT", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"BAUD RATE", None))
        self.Baudrate_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"9600", None))
        self.Baudrate_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"14400", None))
        self.Baudrate_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"38400", None))
        self.Baudrate_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"115200", None))

        self.connect_button.setText(QCoreApplication.translate("MainWindow", u"CONNECT", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TX - COMMAND", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"RX - COMMAND", None))
        self.command_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"CMD_RANDOM", None))
        self.command_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"CMD_GET_FWVERSION", None))
        self.command_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"CMD_HELLO ", None))
        self.command_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"CMD_GET_TARGET_TYPE", None))
        self.command_combo.setItemText(4, QCoreApplication.translate("MainWindow", u"CMD_READ_HR", None))
        self.command_combo.setItemText(5, QCoreApplication.translate("MainWindow", u"CMD_WRITE_HR", None))
        self.command_combo.setItemText(6, QCoreApplication.translate("MainWindow", u"CMD_ASCII_CONSOLE", None))

        self.send_button.setText(QCoreApplication.translate("MainWindow", u"send", None))
    # retranslateUi

