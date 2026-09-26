# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'help_dialog_v2.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_HelpDialog(object):
    def setupUi(self, HelpDialog):
        if not HelpDialog.objectName():
            HelpDialog.setObjectName(u"HelpDialog")
        HelpDialog.resize(900, 650)
        HelpDialog.setMinimumSize(QSize(700, 500))
        self.dialogLayout = QVBoxLayout(HelpDialog)
        self.dialogLayout.setSpacing(0)
        self.dialogLayout.setObjectName(u"dialogLayout")
        self.dialogLayout.setContentsMargins(0, 0, 0, 0)
        self.headerFrame = QFrame(HelpDialog)
        self.headerFrame.setObjectName(u"headerFrame")
        self.headerFrame.setMinimumSize(QSize(0, 48))
        self.headerFrame.setMaximumSize(QSize(16777215, 48))
        self.headerFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.headerFrame.setStyleSheet(u"QFrame#headerFrame {\n"
"    border-bottom: 1px solid palette(mid);\n"
"    background-color: palette(window);\n"
"}")
        self.headerLayout = QHBoxLayout(self.headerFrame)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(16, 4, 16, 4)
        self.helpTitleLabel = QLabel(self.headerFrame)
        self.helpTitleLabel.setObjectName(u"helpTitleLabel")
        self.helpTitleLabel.setStyleSheet(u"font-size: 16px; font-weight: 600;")

        self.headerLayout.addWidget(self.helpTitleLabel)

        self.headerSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)

        self.helpCloseBtn = QPushButton(self.headerFrame)
        self.helpCloseBtn.setObjectName(u"helpCloseBtn")
        self.helpCloseBtn.setMinimumSize(QSize(36, 36))
        self.helpCloseBtn.setMaximumSize(QSize(36, 36))
        self.helpCloseBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.helpCloseBtn.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    border-radius: 18px;\n"
"    background-color: transparent;\n"
"    font-size: 16px;\n"
"    font-weight: 600;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: palette(midlight);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: palette(mid);\n"
"}")

        self.headerLayout.addWidget(self.helpCloseBtn)


        self.dialogLayout.addWidget(self.headerFrame)

        self.contentFrame = QFrame(HelpDialog)
        self.contentFrame.setObjectName(u"contentFrame")
        self.contentFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.contentLayout = QHBoxLayout(self.contentFrame)
        self.contentLayout.setSpacing(0)
        self.contentLayout.setObjectName(u"contentLayout")
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.leftPanel = QFrame(self.contentFrame)
        self.leftPanel.setObjectName(u"leftPanel")
        self.leftPanel.setMinimumSize(QSize(180, 0))
        self.leftPanel.setMaximumSize(QSize(280, 16777215))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftPanel.sizePolicy().hasHeightForWidth())
        self.leftPanel.setSizePolicy(sizePolicy)
        self.leftPanel.setFrameShape(QFrame.Shape.StyledPanel)
        self.leftPanel.setStyleSheet(u"QFrame#leftPanel {\n"
"    border-right: 1px solid palette(mid);\n"
"    background-color: palette(window);\n"
"}")
        self.leftPanelLayout = QVBoxLayout(self.leftPanel)
        self.leftPanelLayout.setSpacing(0)
        self.leftPanelLayout.setObjectName(u"leftPanelLayout")
        self.leftPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.sectionListWidget = QListWidget(self.leftPanel)
        self.sectionListWidget.setObjectName(u"sectionListWidget")
        self.sectionListWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.sectionListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.sectionListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sectionListWidget.setSpacing(2)
        self.sectionListWidget.setStyleSheet(u"QListWidget {\n"
"    border: none;\n"
"    outline: none;\n"
"    background-color: transparent;\n"
"}\n"
"QListWidget::item {\n"
"    padding: 10px 14px;\n"
"    border: none;\n"
"    border-radius: 0;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"QListWidget::item:selected {\n"
"    background-color: palette(highlight);\n"
"    color: palette(highlighted-text);\n"
"}\n"
"QListWidget::item:selected:!active {\n"
"    background-color: palette(highlight);\n"
"    color: palette(highlighted-text);\n"
"}")

        self.leftPanelLayout.addWidget(self.sectionListWidget)


        self.contentLayout.addWidget(self.leftPanel)

        self.rightPanel = QFrame(self.contentFrame)
        self.rightPanel.setObjectName(u"rightPanel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.rightPanel.sizePolicy().hasHeightForWidth())
        self.rightPanel.setSizePolicy(sizePolicy1)
        self.rightPanel.setFrameShape(QFrame.Shape.NoFrame)
        self.rightPanelLayout = QVBoxLayout(self.rightPanel)
        self.rightPanelLayout.setSpacing(0)
        self.rightPanelLayout.setObjectName(u"rightPanelLayout")
        self.rightPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.helpContentBrowser = QTextBrowser(self.rightPanel)
        self.helpContentBrowser.setObjectName(u"helpContentBrowser")
        self.helpContentBrowser.setOpenExternalLinks(True)
        self.helpContentBrowser.setFrameShape(QFrame.Shape.NoFrame)
        self.helpContentBrowser.setStyleSheet(u"QTextBrowser {\n"
"    border: none;\n"
"    background-color: palette(base);\n"
"    padding: 24px;\n"
"    font-family: 'Pretendard', 'Noto Sans KR', system-ui;\n"
"    font-size: 14px;\n"
"    line-height: 1.6;\n"
"}\n"
"QTextBrowser:focus {\n"
"    border: none;\n"
"    outline: none;\n"
"}")

        self.rightPanelLayout.addWidget(self.helpContentBrowser)


        self.contentLayout.addWidget(self.rightPanel)


        self.dialogLayout.addWidget(self.contentFrame)


        self.retranslateUi(HelpDialog)

        QMetaObject.connectSlotsByName(HelpDialog)
    # setupUi

    def retranslateUi(self, HelpDialog):
        HelpDialog.setWindowTitle(QCoreApplication.translate("HelpDialog", u"\U0001f4d6 ComfyCraft AI Easy Studio \U0000b3c4\U0000c6c0\U0000b9d0 v0.3", None))
        self.helpTitleLabel.setText(QCoreApplication.translate("HelpDialog", u"\U0001f4d6 ComfyCraft AI Easy Studio \U0000b3c4\U0000c6c0\U0000b9d0", None))
#if QT_CONFIG(tooltip)
        self.helpCloseBtn.setToolTip(QCoreApplication.translate("HelpDialog", u"\ub2eb\uae30 (Esc)", None))
#endif // QT_CONFIG(tooltip)
        self.helpCloseBtn.setText(QCoreApplication.translate("HelpDialog", u"\u2715", None))
    # retranslateUi

