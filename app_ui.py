'''
Project PZYP

Created by: Ana Graça, Nuno Guerra, Sónia Jardim

Data Entrega: 07/03/2022
'''

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pzyp_app.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QRadioButton, QSizePolicy, QSlider, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(651, 464)
        self.widget = QWidget(MainWindow)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 10, 631, 441))
        self.lblTitulo = QLabel(self.widget)
        self.lblTitulo.setObjectName(u"lblTitulo")
        self.lblTitulo.setGeometry(QRect(270, 10, 61, 51))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(18)
        font.setBold(True)
        self.lblTitulo.setFont(font)
        self.lblTitulo.setFrameShape(QFrame.NoFrame)
        self.rBtnCompressao = QRadioButton(self.widget)
        self.rBtnCompressao.setObjectName(u"rBtnCompressao")
        self.rBtnCompressao.setGeometry(QRect(90, 80, 161, 41))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(12)
        self.rBtnCompressao.setFont(font1)
        self.rBtnDescompressao = QRadioButton(self.widget)
        self.rBtnDescompressao.setObjectName(u"rBtnDescompressao")
        self.rBtnDescompressao.setGeometry(QRect(390, 80, 141, 41))
        self.rBtnDescompressao.setFont(font1)
        self.lblNivel = QLabel(self.widget)
        self.lblNivel.setObjectName(u"lblNivel")
        self.lblNivel.setGeometry(QRect(30, 140, 201, 31))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(10)
        self.lblNivel.setFont(font2)
        self.horizontalSlider = QSlider(self.widget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(30, 180, 571, 22))
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(4)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.lblPass = QLabel(self.widget)
        self.lblPass.setObjectName(u"lblPass")
        self.lblPass.setGeometry(QRect(30, 240, 81, 31))
        self.lblPass.setFont(font2)
        self.txtPass = QLineEdit(self.widget)
        self.txtPass.setObjectName(u"txtPass")
        self.txtPass.setEnabled(False)
        self.txtPass.setGeometry(QRect(150, 240, 261, 31))
        self.txtPass.setReadOnly(False)
        self.lblConf_Pass = QLabel(self.widget)
        self.lblConf_Pass.setObjectName(u"lblConf_Pass")
        self.lblConf_Pass.setGeometry(QRect(30, 290, 101, 31))
        self.lblConf_Pass.setFont(font2)
        self.txtConf_Pass = QLineEdit(self.widget)
        self.txtConf_Pass.setObjectName(u"txtConf_Pass")
        self.txtConf_Pass.setEnabled(False)
        self.txtConf_Pass.setGeometry(QRect(150, 290, 261, 31))
        self.txtConf_Pass.setReadOnly(False)
        self.btnStart = QPushButton(self.widget)
        self.btnStart.setObjectName(u"btnStart")
        self.btnStart.setGeometry(QRect(450, 360, 141, 31))
        self.btnStart.setFont(font2)
        self.progressBar = QProgressBar(self.widget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(450, 400, 171, 16))
        self.progressBar.setValue(0)
        self.lbllvl = QLabel(self.widget)
        self.lbllvl.setObjectName(u"lbllvl")
        self.lbllvl.setGeometry(QRect(230, 140, 49, 31))
        font3 = QFont()
        font3.setPointSize(12)
        self.lbllvl.setFont(font3)
        self.checkPw = QCheckBox(self.widget)
        self.checkPw.setObjectName(u"checkPw")
        self.checkPw.setGeometry(QRect(460, 240, 81, 20))
        self.checkSummary = QCheckBox(self.widget)
        self.checkSummary.setObjectName(u"checkSummary")
        self.checkSummary.setGeometry(QRect(460, 270, 81, 20))
        self.btnfile = QPushButton(self.widget)
        self.btnfile.setObjectName(u"btnfile")
        self.btnfile.setGeometry(QRect(150, 360, 131, 31))
        self.lblfile = QLabel(self.widget)
        self.lblfile.setObjectName(u"lblfile")
        self.lblfile.setGeometry(QRect(30, 425, 580, 16))

        self.retranslateUi(MainWindow)



        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Dialog", None))
        self.lblTitulo.setText(QCoreApplication.translate("MainWindow", u"PZYP", None))
        self.rBtnCompressao.setText(QCoreApplication.translate("MainWindow", u"Compress\u00e3o", None))
        self.rBtnDescompressao.setText(QCoreApplication.translate("MainWindow", u"Descompress\u00e3o", None))
        self.lblNivel.setText(QCoreApplication.translate("MainWindow", u"Escolha o N\u00edvel de Compress\u00e3o:", None))
        self.lblPass.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.txtPass.setPlaceholderText("")
        self.lblConf_Pass.setText(QCoreApplication.translate("MainWindow", u"Confirma\u00e7\u00e3o:", None))
        self.btnStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.lbllvl.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.checkPw.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.checkSummary.setText(QCoreApplication.translate("MainWindow", u"Summary", None))
        self.btnfile.setText(QCoreApplication.translate("MainWindow", u"Selecionar Ficheiro...", None))
        self.lblfile.setText(QCoreApplication.translate("MainWindow", u"...", None))
    # retranslateUi

