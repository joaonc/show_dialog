# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'show_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QWidget)
from . import resources_rc

class Ui_ShowDialog(object):
    def setupUi(self, ShowDialog):
        if not ShowDialog.objectName():
            ShowDialog.setObjectName(u"ShowDialog")
        ShowDialog.resize(677, 584)
        font = QFont()
        font.setPointSize(50)
        ShowDialog.setFont(font)
        icon = QIcon()
        icon.addFile(u":/images/window_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ShowDialog.setWindowIcon(icon)
        self.title_label = QLabel(ShowDialog)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(120, 50, 431, 121))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.details_label = QLabel(ShowDialog)
        self.details_label.setObjectName(u"details_label")
        self.details_label.setGeometry(QRect(300, 260, 261, 101))
        font1 = QFont()
        font1.setPointSize(20)
        self.details_label.setFont(font1)
        self.pass_button = QPushButton(ShowDialog)
        self.pass_button.setObjectName(u"pass_button")
        self.pass_button.setGeometry(QRect(330, 430, 331, 121))
        icon1 = QIcon()
        icon1.addFile(u":/images/pass_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pass_button.setIcon(icon1)
        self.fail_button = QPushButton(ShowDialog)
        self.fail_button.setObjectName(u"fail_button")
        self.fail_button.setGeometry(QRect(30, 430, 271, 121))
        icon2 = QIcon()
        icon2.addFile(u":/images/fail_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fail_button.setIcon(icon2)

        self.retranslateUi(ShowDialog)

        QMetaObject.connectSlotsByName(ShowDialog)
    # setupUi

    def retranslateUi(self, ShowDialog):
        ShowDialog.setWindowTitle(QCoreApplication.translate("ShowDialog", u"Show Dialog", None))
        self.title_label.setText(QCoreApplication.translate("ShowDialog", u"Title", None))
        self.details_label.setText(QCoreApplication.translate("ShowDialog", u"Details", None))
        self.pass_button.setText(QCoreApplication.translate("ShowDialog", u"Pass", None))
        self.fail_button.setText(QCoreApplication.translate("ShowDialog", u"Fail", None))
    # retranslateUi

