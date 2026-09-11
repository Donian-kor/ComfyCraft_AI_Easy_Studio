# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'help_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, QSizePolicy,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_HelpDialog(object):
    def setupUi(self, HelpDialog):
        if not HelpDialog.objectName():
            HelpDialog.setObjectName(u"HelpDialog")
        HelpDialog.resize(750, 580)
        HelpDialog.setMinimumSize(QSize(600, 450))
        self.dialogLayout = QVBoxLayout(HelpDialog)
        self.dialogLayout.setSpacing(8)
        self.dialogLayout.setObjectName(u"dialogLayout")
        self.dlgHelpBrowser = QTextBrowser(HelpDialog)
        self.dlgHelpBrowser.setObjectName(u"dlgHelpBrowser")
        self.dlgHelpBrowser.setOpenExternalLinks(True)

        self.dialogLayout.addWidget(self.dlgHelpBrowser)

        self.dlgHelpCloseBtn = QPushButton(HelpDialog)
        self.dlgHelpCloseBtn.setObjectName(u"dlgHelpCloseBtn")

        self.dialogLayout.addWidget(self.dlgHelpCloseBtn)


        self.retranslateUi(HelpDialog)

        QMetaObject.connectSlotsByName(HelpDialog)
    # setupUi

    def retranslateUi(self, HelpDialog):
        HelpDialog.setWindowTitle(QCoreApplication.translate("HelpDialog", u"\U0001f4d6 ComfyCraft AI Easy Studio \U0000b3c4\U0000c6c0\U0000b9d0", None))
        self.dlgHelpCloseBtn.setText(QCoreApplication.translate("HelpDialog", u"\ub2eb\uae30", None))
    # retranslateUi

