# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NEW.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QFrame(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(210, 0))
        self.sidebar.setMaximumSize(QSize(210, 16777215))
        self.sidebar.setFrameShape(QFrame.Shape.NoFrame)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(18, 18, 18, 18)
        self.appTitle = QLabel(self.sidebar)
        self.appTitle.setObjectName(u"appTitle")

        self.sidebarLayout.addWidget(self.appTitle)

        self.topSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.topSpacer)

        self.homeButton = QPushButton(self.sidebar)
        self.homeButton.setObjectName(u"homeButton")

        self.sidebarLayout.addWidget(self.homeButton)

        self.comfyButton = QPushButton(self.sidebar)
        self.comfyButton.setObjectName(u"comfyButton")

        self.sidebarLayout.addWidget(self.comfyButton)

        self.lmstudioButton = QPushButton(self.sidebar)
        self.lmstudioButton.setObjectName(u"lmstudioButton")

        self.sidebarLayout.addWidget(self.lmstudioButton)

        self.settingsButton = QPushButton(self.sidebar)
        self.settingsButton.setObjectName(u"settingsButton")

        self.sidebarLayout.addWidget(self.settingsButton)

        self.bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.bottomSpacer)

        self.connectionStatus = QLabel(self.sidebar)
        self.connectionStatus.setObjectName(u"connectionStatus")

        self.sidebarLayout.addWidget(self.connectionStatus)

        self.versionLabel = QLabel(self.sidebar)
        self.versionLabel.setObjectName(u"versionLabel")

        self.sidebarLayout.addWidget(self.versionLabel)


        self.mainLayout.addWidget(self.sidebar)

        self.contentLayout = QVBoxLayout()
        self.contentLayout.setObjectName(u"contentLayout")
        self.contentLayout.setContentsMargins(26, 22, 26, 22)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.homeTab = QWidget()
        self.homeTab.setObjectName(u"homeTab")
        self.homeLayout = QVBoxLayout(self.homeTab)
        self.homeLayout.setSpacing(18)
        self.homeLayout.setObjectName(u"homeLayout")
        self.heroCard = QFrame(self.homeTab)
        self.heroCard.setObjectName(u"heroCard")
        self.heroCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.heroLayout = QVBoxLayout(self.heroCard)
        self.heroLayout.setObjectName(u"heroLayout")
        self.heroTitle = QLabel(self.heroCard)
        self.heroTitle.setObjectName(u"heroTitle")

        self.heroLayout.addWidget(self.heroTitle)

        self.heroDescription = QLabel(self.heroCard)
        self.heroDescription.setObjectName(u"heroDescription")

        self.heroLayout.addWidget(self.heroDescription)

        self.startButton = QPushButton(self.heroCard)
        self.startButton.setObjectName(u"startButton")

        self.heroLayout.addWidget(self.startButton)


        self.homeLayout.addWidget(self.heroCard)

        self.cardsLayout = QHBoxLayout()
        self.cardsLayout.setObjectName(u"cardsLayout")
        self.comfyCard = QFrame(self.homeTab)
        self.comfyCard.setObjectName(u"comfyCard")
        self.comfyCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.comfyCardLayout = QVBoxLayout(self.comfyCard)
        self.comfyCardLayout.setObjectName(u"comfyCardLayout")
        self.comfyCardTitle = QLabel(self.comfyCard)
        self.comfyCardTitle.setObjectName(u"comfyCardTitle")

        self.comfyCardLayout.addWidget(self.comfyCardTitle)

        self.comfyCardText = QLabel(self.comfyCard)
        self.comfyCardText.setObjectName(u"comfyCardText")

        self.comfyCardLayout.addWidget(self.comfyCardText)

        self.comfyCardButton = QPushButton(self.comfyCard)
        self.comfyCardButton.setObjectName(u"comfyCardButton")

        self.comfyCardLayout.addWidget(self.comfyCardButton)


        self.cardsLayout.addWidget(self.comfyCard)

        self.lmCard = QFrame(self.homeTab)
        self.lmCard.setObjectName(u"lmCard")
        self.lmCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.lmCardLayout = QVBoxLayout(self.lmCard)
        self.lmCardLayout.setObjectName(u"lmCardLayout")
        self.lmCardTitle = QLabel(self.lmCard)
        self.lmCardTitle.setObjectName(u"lmCardTitle")

        self.lmCardLayout.addWidget(self.lmCardTitle)

        self.lmCardText = QLabel(self.lmCard)
        self.lmCardText.setObjectName(u"lmCardText")

        self.lmCardLayout.addWidget(self.lmCardText)

        self.lmCardButton = QPushButton(self.lmCard)
        self.lmCardButton.setObjectName(u"lmCardButton")

        self.lmCardLayout.addWidget(self.lmCardButton)


        self.cardsLayout.addWidget(self.lmCard)


        self.homeLayout.addLayout(self.cardsLayout)

        self.recentTitle = QLabel(self.homeTab)
        self.recentTitle.setObjectName(u"recentTitle")

        self.homeLayout.addWidget(self.recentTitle)

        self.recentList = QListWidget(self.homeTab)
        self.recentList.setObjectName(u"recentList")

        self.homeLayout.addWidget(self.recentList)

        self.systemCard = QFrame(self.homeTab)
        self.systemCard.setObjectName(u"systemCard")
        self.systemCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.systemLayout = QHBoxLayout(self.systemCard)
        self.systemLayout.setObjectName(u"systemLayout")
        self.gpuStatus = QLabel(self.systemCard)
        self.gpuStatus.setObjectName(u"gpuStatus")

        self.systemLayout.addWidget(self.gpuStatus)

        self.lmStatus = QLabel(self.systemCard)
        self.lmStatus.setObjectName(u"lmStatus")

        self.systemLayout.addWidget(self.lmStatus)

        self.comfyStatus = QLabel(self.systemCard)
        self.comfyStatus.setObjectName(u"comfyStatus")

        self.systemLayout.addWidget(self.comfyStatus)


        self.homeLayout.addWidget(self.systemCard)

        self.tabWidget.addTab(self.homeTab, "")
        self.comfyTab = QWidget()
        self.comfyTab.setObjectName(u"comfyTab")
        self.comfyLayout = QVBoxLayout(self.comfyTab)
        self.comfyLayout.setObjectName(u"comfyLayout")
        self.comfyTitle = QLabel(self.comfyTab)
        self.comfyTitle.setObjectName(u"comfyTitle")

        self.comfyLayout.addWidget(self.comfyTitle)

        self.workflowEditor = QTextEdit(self.comfyTab)
        self.workflowEditor.setObjectName(u"workflowEditor")

        self.comfyLayout.addWidget(self.workflowEditor)

        self.progressBar = QProgressBar(self.comfyTab)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(45)

        self.comfyLayout.addWidget(self.progressBar)

        self.generateButton = QPushButton(self.comfyTab)
        self.generateButton.setObjectName(u"generateButton")

        self.comfyLayout.addWidget(self.generateButton)

        self.tabWidget.addTab(self.comfyTab, "")
        self.lmstudioTab = QWidget()
        self.lmstudioTab.setObjectName(u"lmstudioTab")
        self.lmstudioLayout = QVBoxLayout(self.lmstudioTab)
        self.lmstudioLayout.setObjectName(u"lmstudioLayout")
        self.lmstudioTitle = QLabel(self.lmstudioTab)
        self.lmstudioTitle.setObjectName(u"lmstudioTitle")

        self.lmstudioLayout.addWidget(self.lmstudioTitle)

        self.modelList = QListWidget(self.lmstudioTab)
        self.modelList.setObjectName(u"modelList")

        self.lmstudioLayout.addWidget(self.modelList)

        self.modelInfo = QLabel(self.lmstudioTab)
        self.modelInfo.setObjectName(u"modelInfo")

        self.lmstudioLayout.addWidget(self.modelInfo)

        self.tabWidget.addTab(self.lmstudioTab, "")
        self.settingsTab = QWidget()
        self.settingsTab.setObjectName(u"settingsTab")
        self.settingsLayout = QFormLayout(self.settingsTab)
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.comfyUrlLabel = QLabel(self.settingsTab)
        self.comfyUrlLabel.setObjectName(u"comfyUrlLabel")

        self.settingsLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.comfyUrlLabel)

        self.comfyUrl = QLineEdit(self.settingsTab)
        self.comfyUrl.setObjectName(u"comfyUrl")

        self.settingsLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comfyUrl)

        self.lmstudioUrlLabel = QLabel(self.settingsTab)
        self.lmstudioUrlLabel.setObjectName(u"lmstudioUrlLabel")

        self.settingsLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lmstudioUrlLabel)

        self.lmstudioUrl = QLineEdit(self.settingsTab)
        self.lmstudioUrl.setObjectName(u"lmstudioUrl")

        self.settingsLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lmstudioUrl)

        self.themeLabel = QLabel(self.settingsTab)
        self.themeLabel.setObjectName(u"themeLabel")

        self.settingsLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.themeLabel)

        self.themeCombo = QComboBox(self.settingsTab)
        self.themeCombo.addItem("")
        self.themeCombo.addItem("")
        self.themeCombo.setObjectName(u"themeCombo")

        self.settingsLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.themeCombo)

        self.saveSettingsButton = QPushButton(self.settingsTab)
        self.saveSettingsButton.setObjectName(u"saveSettingsButton")

        self.settingsLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.saveSettingsButton)

        self.tabWidget.addTab(self.settingsTab, "")

        self.contentLayout.addWidget(self.tabWidget)


        self.mainLayout.addLayout(self.contentLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ComfyUI + LMStudio", None))
        self.appTitle.setText(QCoreApplication.translate("MainWindow", u"\u2726  ComfyUI + LMStudio", None))
        self.homeButton.setText(QCoreApplication.translate("MainWindow", u"\u2302   \ud648", None))
        self.comfyButton.setText(QCoreApplication.translate("MainWindow", u"\u25c8   ComfyUI", None))
        self.lmstudioButton.setText(QCoreApplication.translate("MainWindow", u"\u25c6   LMStudio", None))
        self.settingsButton.setText(QCoreApplication.translate("MainWindow", u"\u2699   \uc124\uc815", None))
        self.connectionStatus.setText(QCoreApplication.translate("MainWindow", u"\u25cf  \uc5f0\uacb0 \uc0c1\ud0dc  \uc815\uc0c1", None))
        self.versionLabel.setText(QCoreApplication.translate("MainWindow", u"v1.0.0  \u2022  Windows", None))
        self.heroTitle.setText(QCoreApplication.translate("MainWindow", u"AI \uc774\ubbf8\uc9c0 \uc0dd\uc131\uc758\\n\uc0c8\ub85c\uc6b4 \uc791\uc5c5 \uacf5\uac04", None))
        self.heroDescription.setText(QCoreApplication.translate("MainWindow", u"ComfyUI\uc640 LMStudio\ub97c \ud558\ub098\uc758 \uc571\uc5d0\uc11c \ud3b8\ub9ac\ud558\uac8c \uc0ac\uc6a9\ud558\uc138\uc694.", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"\uc0c8 \ud504\ub85c\uc81d\ud2b8 \uc2dc\uc791  \u2192", None))
        self.comfyCardTitle.setText(QCoreApplication.translate("MainWindow", u"\u25c8  ComfyUI", None))
        self.comfyCardText.setText(QCoreApplication.translate("MainWindow", u"\uc774\ubbf8\uc9c0 \uc0dd\uc131 \uc6cc\ud06c\ud50c\ub85c\uc6b0", None))
        self.comfyCardButton.setText(QCoreApplication.translate("MainWindow", u"\ubc14\ub85c\uac00\uae30  \u2192", None))
        self.lmCardTitle.setText(QCoreApplication.translate("MainWindow", u"\u25c6  LMStudio", None))
        self.lmCardText.setText(QCoreApplication.translate("MainWindow", u"\ub85c\uceec AI \ubaa8\ub378 \uad00\ub9ac", None))
        self.lmCardButton.setText(QCoreApplication.translate("MainWindow", u"\ubc14\ub85c\uac00\uae30  \u2192", None))
        self.recentTitle.setText(QCoreApplication.translate("MainWindow", u"\ucd5c\uadfc \ud504\ub85c\uc81d\ud2b8", None))
        self.gpuStatus.setText(QCoreApplication.translate("MainWindow", u"GPU   \u25cf \uc815\uc0c1", None))
        self.lmStatus.setText(QCoreApplication.translate("MainWindow", u"LMStudio   \u25cf \uc2e4\ud589 \uc911", None))
        self.comfyStatus.setText(QCoreApplication.translate("MainWindow", u"ComfyUI   \u25cf \uc900\ube44\ub428", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.homeTab), QCoreApplication.translate("MainWindow", u"\ud648", None))
        self.comfyTitle.setText(QCoreApplication.translate("MainWindow", u"ComfyUI \uc6cc\ud06c\ud50c\ub85c\uc6b0", None))
        self.workflowEditor.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\uc6cc\ud06c\ud50c\ub85c\uc6b0 JSON \ub610\ub294 \uc791\uc5c5 \uc815\ubcf4\ub97c \uc785\ub825\ud558\uc138\uc694.", None))
        self.generateButton.setText(QCoreApplication.translate("MainWindow", u"\uc0dd\uc131 \uc2dc\uc791", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.comfyTab), QCoreApplication.translate("MainWindow", u"ComfyUI", None))
        self.lmstudioTitle.setText(QCoreApplication.translate("MainWindow", u"LMStudio \ubaa8\ub378", None))
        self.modelInfo.setText(QCoreApplication.translate("MainWindow", u"\ubaa8\ub378\uc744 \uc120\ud0dd\ud558\uba74 \uc0c1\uc138 \uc815\ubcf4\uac00 \ud45c\uc2dc\ub429\ub2c8\ub2e4.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.lmstudioTab), QCoreApplication.translate("MainWindow", u"LMStudio", None))
        self.comfyUrlLabel.setText(QCoreApplication.translate("MainWindow", u"ComfyUI \uc8fc\uc18c", None))
        self.comfyUrl.setText(QCoreApplication.translate("MainWindow", u"http://127.0.0.1:8188", None))
        self.lmstudioUrlLabel.setText(QCoreApplication.translate("MainWindow", u"LMStudio \uc8fc\uc18c", None))
        self.lmstudioUrl.setText(QCoreApplication.translate("MainWindow", u"http://127.0.0.1:1234", None))
        self.themeLabel.setText(QCoreApplication.translate("MainWindow", u"\ud14c\ub9c8", None))
        self.themeCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"Modern Dark", None))
        self.themeCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"Professional Dark", None))

        self.saveSettingsButton.setText(QCoreApplication.translate("MainWindow", u"\uc124\uc815 \uc800\uc7a5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
    # retranslateUi

