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
from PySide6.QtWidgets import (QApplication, QDialog, QSizePolicy, QWidget)
from . import resources_rc

class Ui_ShowDialog(object):
    def setupUi(self, ShowDialog):
        if not ShowDialog.objectName():
            ShowDialog.setObjectName(u"ShowDialog")
        ShowDialog.resize(400, 300)
        icon = QIcon()
        icon.addFile(u":/images/window_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ShowDialog.setWindowIcon(icon)

        self.retranslateUi(ShowDialog)

        QMetaObject.connectSlotsByName(ShowDialog)
    # setupUi

    def retranslateUi(self, ShowDialog):
        ShowDialog.setWindowTitle(QCoreApplication.translate("ShowDialog", u"Show Dialog", None))
    # retranslateUi

