# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(420, 620)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainTabs = QTabWidget(self.centralwidget)
        self.mainTabs.setObjectName(u"mainTabs")
        self.homeTab = QWidget()
        self.homeTab.setObjectName(u"homeTab")
        self.homeLayout = QVBoxLayout(self.homeTab)
        self.homeLayout.setObjectName(u"homeLayout")
        self.label = QLabel(self.homeTab)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.homeLayout.addWidget(self.label)

        self.button = QPushButton(self.homeTab)
        self.button.setObjectName(u"button")

        self.homeLayout.addWidget(self.button)

        self.mainTabs.addTab(self.homeTab, "")
        self.calculatorTab = QWidget()
        self.calculatorTab.setObjectName(u"calculatorTab")
        self.calculatorLayout = QVBoxLayout(self.calculatorTab)
        self.calculatorLayout.setObjectName(u"calculatorLayout")
        self.mainTabs.addTab(self.calculatorTab, "")

        self.verticalLayout.addWidget(self.mainTabs)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.mainTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u7b2c\u4e00\u4e2a\u9879\u76ee", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u70b9\u4e00\u4e0b\u6309\u94ae\u8bd5\u8bd5", None))
        self.button.setText(QCoreApplication.translate("MainWindow", u"\u70b9\u51fb", None))
        self.mainTabs.setTabText(self.mainTabs.indexOf(self.homeTab), QCoreApplication.translate("MainWindow", u"\u9996\u9875", None))
        self.mainTabs.setTabText(self.mainTabs.indexOf(self.calculatorTab), QCoreApplication.translate("MainWindow", u"\u8ba1\u7b97\u5668", None))
    # retranslateUi

