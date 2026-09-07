# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QPlainTextEdit, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1500, 912)
        MainWindow.setMinimumSize(QSize(1100, 720))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        MainWindow.setFont(font)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.mainLayout = QHBoxLayout(self.centralWidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_frame = QFrame(self.centralWidget)
        self.sidebar_frame.setObjectName(u"sidebar_frame")
        self.sidebar_frame.setMinimumSize(QSize(55, 0))
        self.sidebar_frame.setMaximumSize(QSize(210, 16777215))
        self.sidebar_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.sidebarLayout = QVBoxLayout(self.sidebar_frame)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(18, 18, 18, 18)
        self.appTitle = QLabel(self.sidebar_frame)
        self.appTitle.setObjectName(u"appTitle")

        self.sidebarLayout.addWidget(self.appTitle)

        self.topSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.topSpacer)

        self.homeButton = QPushButton(self.sidebar_frame)
        self.homeButton.setObjectName(u"homeButton")

        self.sidebarLayout.addWidget(self.homeButton)

        self.pushButton = QPushButton(self.sidebar_frame)
        self.pushButton.setObjectName(u"pushButton")
        icon = QIcon()
        icon.addFile(u":/newPrefix1/network-success.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(26, 26))

        self.sidebarLayout.addWidget(self.pushButton)

        self.comfyButton = QPushButton(self.sidebar_frame)
        self.comfyButton.setObjectName(u"comfyButton")

        self.sidebarLayout.addWidget(self.comfyButton)

        self.lmstudioButton = QPushButton(self.sidebar_frame)
        self.lmstudioButton.setObjectName(u"lmstudioButton")

        self.sidebarLayout.addWidget(self.lmstudioButton)

        self.settingsButton = QPushButton(self.sidebar_frame)
        self.settingsButton.setObjectName(u"settingsButton")

        self.sidebarLayout.addWidget(self.settingsButton)

        self.bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.bottomSpacer)

        self.connectionStatus = QLabel(self.sidebar_frame)
        self.connectionStatus.setObjectName(u"connectionStatus")

        self.sidebarLayout.addWidget(self.connectionStatus)

        self.versionLabel = QLabel(self.sidebar_frame)
        self.versionLabel.setObjectName(u"versionLabel")

        self.sidebarLayout.addWidget(self.versionLabel)


        self.mainLayout.addWidget(self.sidebar_frame)

        self.contentLayout = QVBoxLayout()
        self.contentLayout.setSpacing(12)
        self.contentLayout.setObjectName(u"contentLayout")
        self.contentLayout.setContentsMargins(26, 22, 26, 22)
        self.tabWidget = QTabWidget(self.centralWidget)
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
        self.comfyTabLayout = QVBoxLayout(self.comfyTab)
        self.comfyTabLayout.setSpacing(10)
        self.comfyTabLayout.setObjectName(u"comfyTabLayout")
        self.ComfygroupBox = QGroupBox(self.comfyTab)
        self.ComfygroupBox.setObjectName(u"ComfygroupBox")
        self.ComfygroupBox.setMinimumSize(QSize(351, 301))
        self.comfyAddressLabel = QLabel(self.ComfygroupBox)
        self.comfyAddressLabel.setObjectName(u"comfyAddressLabel")
        self.comfyAddressLabel.setGeometry(QRect(10, 54, 91, 20))
        self.comfyUrlEdit = QLineEdit(self.ComfygroupBox)
        self.comfyUrlEdit.setObjectName(u"comfyUrlEdit")
        self.comfyUrlEdit.setGeometry(QRect(10, 77, 221, 41))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comfyUrlEdit.sizePolicy().hasHeightForWidth())
        self.comfyUrlEdit.setSizePolicy(sizePolicy)
        self.comfyUrlEdit.setMinimumSize(QSize(0, 32))
        self.comfyPathLabel = QLabel(self.ComfygroupBox)
        self.comfyPathLabel.setObjectName(u"comfyPathLabel")
        self.comfyPathLabel.setGeometry(QRect(10, 192, 91, 20))
        self.comfyModelPathEdit = QLineEdit(self.ComfygroupBox)
        self.comfyModelPathEdit.setObjectName(u"comfyModelPathEdit")
        self.comfyModelPathEdit.setGeometry(QRect(10, 214, 331, 41))
        sizePolicy.setHeightForWidth(self.comfyModelPathEdit.sizePolicy().hasHeightForWidth())
        self.comfyModelPathEdit.setSizePolicy(sizePolicy)
        self.comfyModelPathEdit.setMinimumSize(QSize(0, 32))
        self.comfyStatusLabel = QLabel(self.ComfygroupBox)
        self.comfyStatusLabel.setObjectName(u"comfyStatusLabel")
        self.comfyStatusLabel.setGeometry(QRect(227, 46, 121, 31))
        self.comfyTitleLabel = QLabel(self.ComfygroupBox)
        self.comfyTitleLabel.setObjectName(u"comfyTitleLabel")
        self.comfyTitleLabel.setGeometry(QRect(100, 20, 121, 31))
        font1 = QFont()
        font1.setFamilies([u"Cascadia Code"])
        font1.setBold(True)
        self.comfyTitleLabel.setFont(font1)
        self.comfyTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.comfyCheckButton = QPushButton(self.ComfygroupBox)
        self.comfyCheckButton.setObjectName(u"comfyCheckButton")
        self.comfyCheckButton.setGeometry(QRect(240, 78, 101, 41))
        self.comfyCheckButton.setMinimumSize(QSize(80, 32))
        self.modelPathStatusLabel = QLabel(self.ComfygroupBox)
        self.modelPathStatusLabel.setObjectName(u"modelPathStatusLabel")
        self.modelPathStatusLabel.setGeometry(QRect(10, 262, 100, 16))
        self.browseModelFolderButton = QPushButton(self.ComfygroupBox)
        self.browseModelFolderButton.setObjectName(u"browseModelFolderButton")
        self.browseModelFolderButton.setGeometry(QRect(253, 262, 86, 32))
        self.browseModelFolderButton.setMinimumSize(QSize(80, 32))
        self.comfyModelLabel = QLabel(self.ComfygroupBox)
        self.comfyModelLabel.setObjectName(u"comfyModelLabel")
        self.comfyModelLabel.setGeometry(QRect(10, 123, 78, 16))
        self.comfyModelCombo = QComboBox(self.ComfygroupBox)
        self.comfyModelCombo.setObjectName(u"comfyModelCombo")
        self.comfyModelCombo.setGeometry(QRect(10, 150, 104, 42))
        self.comfyModelCombo.setMinimumSize(QSize(0, 42))
        self.modelPathStatusLabel.raise_()
        self.browseModelFolderButton.raise_()
        self.comfyModelLabel.raise_()
        self.comfyModelCombo.raise_()
        self.comfyAddressLabel.raise_()
        self.comfyPathLabel.raise_()
        self.comfyModelPathEdit.raise_()
        self.comfyStatusLabel.raise_()
        self.comfyTitleLabel.raise_()
        self.comfyUrlEdit.raise_()
        self.comfyCheckButton.raise_()

        self.comfyTabLayout.addWidget(self.ComfygroupBox)

        self.generationPanel = QGroupBox(self.comfyTab)
        self.generationPanel.setObjectName(u"generationPanel")
        self.generationPanel.setMinimumSize(QSize(441, 251))
        self.layoutWidget = QWidget(self.generationPanel)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 192, 414, 51))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.preset_512x512 = QPushButton(self.layoutWidget)
        self.preset_512x512.setObjectName(u"preset_512x512")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.preset_512x512.sizePolicy().hasHeightForWidth())
        self.preset_512x512.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.preset_512x512)

        self.preset_768x768 = QPushButton(self.layoutWidget)
        self.preset_768x768.setObjectName(u"preset_768x768")
        sizePolicy1.setHeightForWidth(self.preset_768x768.sizePolicy().hasHeightForWidth())
        self.preset_768x768.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.preset_768x768)

        self.preset_1024x1024 = QPushButton(self.layoutWidget)
        self.preset_1024x1024.setObjectName(u"preset_1024x1024")
        sizePolicy1.setHeightForWidth(self.preset_1024x1024.sizePolicy().hasHeightForWidth())
        self.preset_1024x1024.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.preset_1024x1024)

        self.preset_832x1216 = QPushButton(self.layoutWidget)
        self.preset_832x1216.setObjectName(u"preset_832x1216")
        sizePolicy1.setHeightForWidth(self.preset_832x1216.sizePolicy().hasHeightForWidth())
        self.preset_832x1216.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.preset_832x1216)

        self.preset_1216x832 = QPushButton(self.layoutWidget)
        self.preset_1216x832.setObjectName(u"preset_1216x832")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.preset_1216x832.sizePolicy().hasHeightForWidth())
        self.preset_1216x832.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.preset_1216x832)

        self.layoutWidget1 = QWidget(self.generationPanel)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(9, 40, 424, 70))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widthLabel = QLabel(self.layoutWidget1)
        self.widthLabel.setObjectName(u"widthLabel")
        self.widthLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.widthLabel)

        self.widthSpinBox = QSpinBox(self.layoutWidget1)
        self.widthSpinBox.setObjectName(u"widthSpinBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widthSpinBox.sizePolicy().hasHeightForWidth())
        self.widthSpinBox.setSizePolicy(sizePolicy3)
        self.widthSpinBox.setMaximumSize(QSize(71, 40))
        self.widthSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widthSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.widthSpinBox.setMinimum(64)
        self.widthSpinBox.setMaximum(4096)
        self.widthSpinBox.setValue(1024)

        self.verticalLayout_2.addWidget(self.widthSpinBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.heightLabel = QLabel(self.layoutWidget1)
        self.heightLabel.setObjectName(u"heightLabel")
        self.heightLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.heightLabel)

        self.heightSpinBox = QSpinBox(self.layoutWidget1)
        self.heightSpinBox.setObjectName(u"heightSpinBox")
        sizePolicy3.setHeightForWidth(self.heightSpinBox.sizePolicy().hasHeightForWidth())
        self.heightSpinBox.setSizePolicy(sizePolicy3)
        self.heightSpinBox.setMaximumSize(QSize(71, 40))
        self.heightSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.heightSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.heightSpinBox.setMinimum(64)
        self.heightSpinBox.setMaximum(4096)
        self.heightSpinBox.setValue(1024)

        self.verticalLayout_4.addWidget(self.heightSpinBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.stepsLabel = QLabel(self.layoutWidget1)
        self.stepsLabel.setObjectName(u"stepsLabel")
        self.stepsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.stepsLabel)

        self.stepsSpinBox = QSpinBox(self.layoutWidget1)
        self.stepsSpinBox.setObjectName(u"stepsSpinBox")
        sizePolicy3.setHeightForWidth(self.stepsSpinBox.sizePolicy().hasHeightForWidth())
        self.stepsSpinBox.setSizePolicy(sizePolicy3)
        self.stepsSpinBox.setMaximumSize(QSize(51, 40))
        self.stepsSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stepsSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.stepsSpinBox.setMinimum(1)
        self.stepsSpinBox.setMaximum(200)
        self.stepsSpinBox.setValue(20)

        self.verticalLayout_5.addWidget(self.stepsSpinBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.cfgLabel = QLabel(self.layoutWidget1)
        self.cfgLabel.setObjectName(u"cfgLabel")
        self.cfgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.cfgLabel)

        self.cfgSpinBox = QDoubleSpinBox(self.layoutWidget1)
        self.cfgSpinBox.setObjectName(u"cfgSpinBox")
        sizePolicy3.setHeightForWidth(self.cfgSpinBox.sizePolicy().hasHeightForWidth())
        self.cfgSpinBox.setSizePolicy(sizePolicy3)
        self.cfgSpinBox.setMaximumSize(QSize(51, 40))
        self.cfgSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cfgSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.cfgSpinBox.setMinimum(0.000000000000000)
        self.cfgSpinBox.setMaximum(30.000000000000000)
        self.cfgSpinBox.setValue(7.000000000000000)

        self.verticalLayout_6.addWidget(self.cfgSpinBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.seedLabel = QLabel(self.layoutWidget1)
        self.seedLabel.setObjectName(u"seedLabel")
        self.seedLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.seedLabel)

        self.seedSpinBox = QSpinBox(self.layoutWidget1)
        self.seedSpinBox.setObjectName(u"seedSpinBox")
        sizePolicy3.setHeightForWidth(self.seedSpinBox.sizePolicy().hasHeightForWidth())
        self.seedSpinBox.setSizePolicy(sizePolicy3)
        self.seedSpinBox.setMaximumSize(QSize(81, 40))
        self.seedSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.seedSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.seedSpinBox.setMinimum(-1)
        self.seedSpinBox.setMaximum(2147483647)
        self.seedSpinBox.setValue(-1)

        self.verticalLayout_7.addWidget(self.seedSpinBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_7)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.denoiseLabel = QLabel(self.layoutWidget1)
        self.denoiseLabel.setObjectName(u"denoiseLabel")
        self.denoiseLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_8.addWidget(self.denoiseLabel)

        self.denoiseSpinBox = QDoubleSpinBox(self.layoutWidget1)
        self.denoiseSpinBox.setObjectName(u"denoiseSpinBox")
        sizePolicy3.setHeightForWidth(self.denoiseSpinBox.sizePolicy().hasHeightForWidth())
        self.denoiseSpinBox.setSizePolicy(sizePolicy3)
        self.denoiseSpinBox.setMaximumSize(QSize(51, 40))
        self.denoiseSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.denoiseSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.denoiseSpinBox.setMinimum(0.000000000000000)
        self.denoiseSpinBox.setMaximum(1.000000000000000)
        self.denoiseSpinBox.setValue(1.000000000000000)

        self.verticalLayout_8.addWidget(self.denoiseSpinBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_8)

        self.layoutWidget2 = QWidget(self.generationPanel)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(9, 114, 421, 72))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.samplerLabel = QLabel(self.layoutWidget2)
        self.samplerLabel.setObjectName(u"samplerLabel")
        self.samplerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.samplerLabel)

        self.samplerComboBox = QComboBox(self.layoutWidget2)
        self.samplerComboBox.setObjectName(u"samplerComboBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.samplerComboBox.sizePolicy().hasHeightForWidth())
        self.samplerComboBox.setSizePolicy(sizePolicy4)
        self.samplerComboBox.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_9.addWidget(self.samplerComboBox)


        self.horizontalLayout_4.addLayout(self.verticalLayout_9)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.schedulerLabel = QLabel(self.layoutWidget2)
        self.schedulerLabel.setObjectName(u"schedulerLabel")
        self.schedulerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_10.addWidget(self.schedulerLabel)

        self.schedulerComboBox = QComboBox(self.layoutWidget2)
        self.schedulerComboBox.setObjectName(u"schedulerComboBox")
        sizePolicy4.setHeightForWidth(self.schedulerComboBox.sizePolicy().hasHeightForWidth())
        self.schedulerComboBox.setSizePolicy(sizePolicy4)
        self.schedulerComboBox.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_10.addWidget(self.schedulerComboBox)


        self.horizontalLayout_4.addLayout(self.verticalLayout_10)


        self.comfyTabLayout.addWidget(self.generationPanel)

        self.executionPanel = QGroupBox(self.comfyTab)
        self.executionPanel.setObjectName(u"executionPanel")
        self.executionLayout = QVBoxLayout(self.executionPanel)
        self.executionLayout.setSpacing(0)
        self.executionLayout.setObjectName(u"executionLayout")
        self.executionLayout.setContentsMargins(0, 6, 0, 0)
        self.progressStatusLayout = QHBoxLayout()
        self.progressStatusLayout.setObjectName(u"progressStatusLayout")
        self.progressStatusLabel = QLabel(self.executionPanel)
        self.progressStatusLabel.setObjectName(u"progressStatusLabel")

        self.progressStatusLayout.addWidget(self.progressStatusLabel)

        self.progressStatusSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.progressStatusLayout.addItem(self.progressStatusSpacer)

        self.elapsedLabel = QLabel(self.executionPanel)
        self.elapsedLabel.setObjectName(u"elapsedLabel")
        self.elapsedLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.progressStatusLayout.addWidget(self.elapsedLabel)


        self.executionLayout.addLayout(self.progressStatusLayout)

        self.progressBarLayout = QHBoxLayout()
        self.progressBarLayout.setObjectName(u"progressBarLayout")
        self.progressBar = QProgressBar(self.executionPanel)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy5)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.progressBarLayout.addWidget(self.progressBar)

        self.progressPercentLabel = QLabel(self.executionPanel)
        self.progressPercentLabel.setObjectName(u"progressPercentLabel")
        self.progressPercentLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.progressBarLayout.addWidget(self.progressPercentLabel)


        self.executionLayout.addLayout(self.progressBarLayout)

        self.generateStopLayout = QHBoxLayout()
        self.generateStopLayout.setObjectName(u"generateStopLayout")
        self.generateButton = QPushButton(self.executionPanel)
        self.generateButton.setObjectName(u"generateButton")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.generateButton.sizePolicy().hasHeightForWidth())
        self.generateButton.setSizePolicy(sizePolicy6)
        icon1 = QIcon()
        icon1.addFile(u":/newPrefix1/play.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.generateButton.setIcon(icon1)
        self.generateButton.setCheckable(False)
        self.generateButton.setAutoDefault(False)

        self.generateStopLayout.addWidget(self.generateButton)

        self.stopButton = QPushButton(self.executionPanel)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.stopButton.sizePolicy().hasHeightForWidth())
        self.stopButton.setSizePolicy(sizePolicy1)
        icon2 = QIcon()
        icon2.addFile(u":/newPrefix1/stop-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.stopButton.setIcon(icon2)

        self.generateStopLayout.addWidget(self.stopButton)


        self.executionLayout.addLayout(self.generateStopLayout)

        self.executionLayout.setStretch(1, 1)
        self.executionLayout.setStretch(2, 2)

        self.comfyTabLayout.addWidget(self.executionPanel)

        self.facedetailerGroupBox = QGroupBox(self.comfyTab)
        self.facedetailerGroupBox.setObjectName(u"facedetailerGroupBox")
        self.facedetailerGroupBox.setMinimumSize(QSize(751, 181))
        self.facedetailerCheckBox = QCheckBox(self.facedetailerGroupBox)
        self.facedetailerCheckBox.setObjectName(u"facedetailerCheckBox")
        self.facedetailerCheckBox.setGeometry(QRect(190, 0, 31, 26))
        self.facedetailerCheckBox.setIconSize(QSize(33, 33))
        self.layoutWidget3 = QWidget(self.facedetailerGroupBox)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(10, 30, 764, 144))
        self.verticalLayout = QVBoxLayout(self.layoutWidget3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.facedetailerDenoiseLabel = QLabel(self.layoutWidget3)
        self.facedetailerDenoiseLabel.setObjectName(u"facedetailerDenoiseLabel")
        self.facedetailerDenoiseLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_11.addWidget(self.facedetailerDenoiseLabel)

        self.facedetailerDenoiseSpinBox = QDoubleSpinBox(self.layoutWidget3)
        self.facedetailerDenoiseSpinBox.setObjectName(u"facedetailerDenoiseSpinBox")
        self.facedetailerDenoiseSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerDenoiseSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerDenoiseSpinBox.setMinimum(0.000000000000000)
        self.facedetailerDenoiseSpinBox.setMaximum(1.000000000000000)
        self.facedetailerDenoiseSpinBox.setSingleStep(0.050000000000000)
        self.facedetailerDenoiseSpinBox.setValue(0.400000000000000)

        self.verticalLayout_11.addWidget(self.facedetailerDenoiseSpinBox)


        self.horizontalLayout_6.addLayout(self.verticalLayout_11)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.facedetailerStepsLabel = QLabel(self.layoutWidget3)
        self.facedetailerStepsLabel.setObjectName(u"facedetailerStepsLabel")
        self.facedetailerStepsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_12.addWidget(self.facedetailerStepsLabel)

        self.facedetailerStepsSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerStepsSpinBox.setObjectName(u"facedetailerStepsSpinBox")
        self.facedetailerStepsSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerStepsSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerStepsSpinBox.setMinimum(1)
        self.facedetailerStepsSpinBox.setMaximum(50)
        self.facedetailerStepsSpinBox.setValue(20)

        self.verticalLayout_12.addWidget(self.facedetailerStepsSpinBox)


        self.horizontalLayout_6.addLayout(self.verticalLayout_12)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.facedetailerCfgLabel = QLabel(self.layoutWidget3)
        self.facedetailerCfgLabel.setObjectName(u"facedetailerCfgLabel")
        self.facedetailerCfgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_13.addWidget(self.facedetailerCfgLabel)

        self.facedetailerCfgSpinBox = QDoubleSpinBox(self.layoutWidget3)
        self.facedetailerCfgSpinBox.setObjectName(u"facedetailerCfgSpinBox")
        self.facedetailerCfgSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerCfgSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerCfgSpinBox.setMinimum(0.000000000000000)
        self.facedetailerCfgSpinBox.setMaximum(20.000000000000000)
        self.facedetailerCfgSpinBox.setSingleStep(0.500000000000000)
        self.facedetailerCfgSpinBox.setValue(4.000000000000000)

        self.verticalLayout_13.addWidget(self.facedetailerCfgSpinBox)


        self.horizontalLayout_6.addLayout(self.verticalLayout_13)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.facedetailerGuideSizeLabel = QLabel(self.layoutWidget3)
        self.facedetailerGuideSizeLabel.setObjectName(u"facedetailerGuideSizeLabel")
        self.facedetailerGuideSizeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_14.addWidget(self.facedetailerGuideSizeLabel)

        self.facedetailerGuideSizeSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerGuideSizeSpinBox.setObjectName(u"facedetailerGuideSizeSpinBox")
        self.facedetailerGuideSizeSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerGuideSizeSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerGuideSizeSpinBox.setMinimum(64)
        self.facedetailerGuideSizeSpinBox.setMaximum(1024)
        self.facedetailerGuideSizeSpinBox.setValue(256)

        self.verticalLayout_14.addWidget(self.facedetailerGuideSizeSpinBox)


        self.horizontalLayout_6.addLayout(self.verticalLayout_14)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.facedetailerMaxSizeLabel = QLabel(self.layoutWidget3)
        self.facedetailerMaxSizeLabel.setObjectName(u"facedetailerMaxSizeLabel")
        self.facedetailerMaxSizeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_15.addWidget(self.facedetailerMaxSizeLabel)

        self.facedetailerMaxSizeSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerMaxSizeSpinBox.setObjectName(u"facedetailerMaxSizeSpinBox")
        self.facedetailerMaxSizeSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerMaxSizeSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerMaxSizeSpinBox.setMinimum(128)
        self.facedetailerMaxSizeSpinBox.setMaximum(2048)
        self.facedetailerMaxSizeSpinBox.setValue(768)

        self.verticalLayout_15.addWidget(self.facedetailerMaxSizeSpinBox)


        self.horizontalLayout_6.addLayout(self.verticalLayout_15)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.facedetailerFeatherLabel = QLabel(self.layoutWidget3)
        self.facedetailerFeatherLabel.setObjectName(u"facedetailerFeatherLabel")
        self.facedetailerFeatherLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_16.addWidget(self.facedetailerFeatherLabel)

        self.facedetailerFeatherSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerFeatherSpinBox.setObjectName(u"facedetailerFeatherSpinBox")
        self.facedetailerFeatherSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerFeatherSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerFeatherSpinBox.setMinimum(0)
        self.facedetailerFeatherSpinBox.setMaximum(20)
        self.facedetailerFeatherSpinBox.setValue(5)

        self.verticalLayout_16.addWidget(self.facedetailerFeatherSpinBox)


        self.horizontalLayout_6.addLayout(self.verticalLayout_16)

        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.facedetailerBboxThresholdLabel = QLabel(self.layoutWidget3)
        self.facedetailerBboxThresholdLabel.setObjectName(u"facedetailerBboxThresholdLabel")
        self.facedetailerBboxThresholdLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_17.addWidget(self.facedetailerBboxThresholdLabel)

        self.facedetailerBboxThresholdSpinBox = QDoubleSpinBox(self.layoutWidget3)
        self.facedetailerBboxThresholdSpinBox.setObjectName(u"facedetailerBboxThresholdSpinBox")
        self.facedetailerBboxThresholdSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerBboxThresholdSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerBboxThresholdSpinBox.setMinimum(0.000000000000000)
        self.facedetailerBboxThresholdSpinBox.setMaximum(1.000000000000000)
        self.facedetailerBboxThresholdSpinBox.setSingleStep(0.050000000000000)
        self.facedetailerBboxThresholdSpinBox.setValue(0.500000000000000)

        self.verticalLayout_17.addWidget(self.facedetailerBboxThresholdSpinBox)


        self.horizontalLayout_6.addLayout(self.verticalLayout_17)

        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.facedetailerBboxDilationLabel = QLabel(self.layoutWidget3)
        self.facedetailerBboxDilationLabel.setObjectName(u"facedetailerBboxDilationLabel")
        self.facedetailerBboxDilationLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_18.addWidget(self.facedetailerBboxDilationLabel)

        self.facedetailerBboxDilationSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerBboxDilationSpinBox.setObjectName(u"facedetailerBboxDilationSpinBox")
        self.facedetailerBboxDilationSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerBboxDilationSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerBboxDilationSpinBox.setMinimum(0)
        self.facedetailerBboxDilationSpinBox.setMaximum(100)
        self.facedetailerBboxDilationSpinBox.setValue(10)

        self.verticalLayout_18.addWidget(self.facedetailerBboxDilationSpinBox)


        self.horizontalLayout_6.addLayout(self.verticalLayout_18)

        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.facedetailerBboxCropFactorLabel = QLabel(self.layoutWidget3)
        self.facedetailerBboxCropFactorLabel.setObjectName(u"facedetailerBboxCropFactorLabel")
        self.facedetailerBboxCropFactorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_19.addWidget(self.facedetailerBboxCropFactorLabel)

        self.facedetailerBboxCropFactorSpinBox = QDoubleSpinBox(self.layoutWidget3)
        self.facedetailerBboxCropFactorSpinBox.setObjectName(u"facedetailerBboxCropFactorSpinBox")
        self.facedetailerBboxCropFactorSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerBboxCropFactorSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerBboxCropFactorSpinBox.setMinimum(1.000000000000000)
        self.facedetailerBboxCropFactorSpinBox.setMaximum(3.000000000000000)
        self.facedetailerBboxCropFactorSpinBox.setSingleStep(0.100000000000000)
        self.facedetailerBboxCropFactorSpinBox.setValue(1.500000000000000)

        self.verticalLayout_19.addWidget(self.facedetailerBboxCropFactorSpinBox)


        self.horizontalLayout_6.addLayout(self.verticalLayout_19)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.facedetailerSamDetectionHintLabel = QLabel(self.layoutWidget3)
        self.facedetailerSamDetectionHintLabel.setObjectName(u"facedetailerSamDetectionHintLabel")
        self.facedetailerSamDetectionHintLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_20.addWidget(self.facedetailerSamDetectionHintLabel)

        self.facedetailerSamDetectionHintComboBox = QComboBox(self.layoutWidget3)
        self.facedetailerSamDetectionHintComboBox.setObjectName(u"facedetailerSamDetectionHintComboBox")
        self.facedetailerSamDetectionHintComboBox.setMinimumSize(QSize(80, 42))

        self.verticalLayout_20.addWidget(self.facedetailerSamDetectionHintComboBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_20)

        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.facedetailerSamDilationLabel = QLabel(self.layoutWidget3)
        self.facedetailerSamDilationLabel.setObjectName(u"facedetailerSamDilationLabel")
        self.facedetailerSamDilationLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_21.addWidget(self.facedetailerSamDilationLabel)

        self.facedetailerSamDilationSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerSamDilationSpinBox.setObjectName(u"facedetailerSamDilationSpinBox")
        self.facedetailerSamDilationSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerSamDilationSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerSamDilationSpinBox.setMinimum(0)
        self.facedetailerSamDilationSpinBox.setMaximum(100)
        self.facedetailerSamDilationSpinBox.setValue(0)

        self.verticalLayout_21.addWidget(self.facedetailerSamDilationSpinBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_21)

        self.verticalLayout_22 = QVBoxLayout()
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.facedetailerSamThresholdLabel = QLabel(self.layoutWidget3)
        self.facedetailerSamThresholdLabel.setObjectName(u"facedetailerSamThresholdLabel")
        self.facedetailerSamThresholdLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_22.addWidget(self.facedetailerSamThresholdLabel)

        self.facedetailerSamThresholdSpinBox = QDoubleSpinBox(self.layoutWidget3)
        self.facedetailerSamThresholdSpinBox.setObjectName(u"facedetailerSamThresholdSpinBox")
        self.facedetailerSamThresholdSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerSamThresholdSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerSamThresholdSpinBox.setMinimum(0.000000000000000)
        self.facedetailerSamThresholdSpinBox.setMaximum(1.000000000000000)
        self.facedetailerSamThresholdSpinBox.setSingleStep(0.010000000000000)
        self.facedetailerSamThresholdSpinBox.setValue(0.930000000000000)

        self.verticalLayout_22.addWidget(self.facedetailerSamThresholdSpinBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_22)

        self.verticalLayout_23 = QVBoxLayout()
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.facedetailerSamBboxExpansionLabel = QLabel(self.layoutWidget3)
        self.facedetailerSamBboxExpansionLabel.setObjectName(u"facedetailerSamBboxExpansionLabel")
        self.facedetailerSamBboxExpansionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_23.addWidget(self.facedetailerSamBboxExpansionLabel)

        self.facedetailerSamBboxExpansionSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerSamBboxExpansionSpinBox.setObjectName(u"facedetailerSamBboxExpansionSpinBox")
        self.facedetailerSamBboxExpansionSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerSamBboxExpansionSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerSamBboxExpansionSpinBox.setMinimum(0)
        self.facedetailerSamBboxExpansionSpinBox.setMaximum(100)
        self.facedetailerSamBboxExpansionSpinBox.setValue(0)

        self.verticalLayout_23.addWidget(self.facedetailerSamBboxExpansionSpinBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_23)

        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.facedetailerSamMaskHintThresholdLabel = QLabel(self.layoutWidget3)
        self.facedetailerSamMaskHintThresholdLabel.setObjectName(u"facedetailerSamMaskHintThresholdLabel")
        self.facedetailerSamMaskHintThresholdLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_24.addWidget(self.facedetailerSamMaskHintThresholdLabel)

        self.facedetailerSamMaskHintThresholdSpinBox = QDoubleSpinBox(self.layoutWidget3)
        self.facedetailerSamMaskHintThresholdSpinBox.setObjectName(u"facedetailerSamMaskHintThresholdSpinBox")
        self.facedetailerSamMaskHintThresholdSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerSamMaskHintThresholdSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerSamMaskHintThresholdSpinBox.setMinimum(0.000000000000000)
        self.facedetailerSamMaskHintThresholdSpinBox.setMaximum(1.000000000000000)
        self.facedetailerSamMaskHintThresholdSpinBox.setSingleStep(0.050000000000000)
        self.facedetailerSamMaskHintThresholdSpinBox.setValue(0.700000000000000)

        self.verticalLayout_24.addWidget(self.facedetailerSamMaskHintThresholdSpinBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_24)

        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.facedetailerSamMaskHintUseNegativeLabel = QLabel(self.layoutWidget3)
        self.facedetailerSamMaskHintUseNegativeLabel.setObjectName(u"facedetailerSamMaskHintUseNegativeLabel")
        self.facedetailerSamMaskHintUseNegativeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_25.addWidget(self.facedetailerSamMaskHintUseNegativeLabel)

        self.facedetailerSamMaskHintUseNegativeComboBox = QComboBox(self.layoutWidget3)
        self.facedetailerSamMaskHintUseNegativeComboBox.setObjectName(u"facedetailerSamMaskHintUseNegativeComboBox")
        self.facedetailerSamMaskHintUseNegativeComboBox.setMinimumSize(QSize(80, 42))

        self.verticalLayout_25.addWidget(self.facedetailerSamMaskHintUseNegativeComboBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_25)

        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.facedetailerCycleLabel = QLabel(self.layoutWidget3)
        self.facedetailerCycleLabel.setObjectName(u"facedetailerCycleLabel")
        self.facedetailerCycleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_26.addWidget(self.facedetailerCycleLabel)

        self.facedetailerCycleSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerCycleSpinBox.setObjectName(u"facedetailerCycleSpinBox")
        self.facedetailerCycleSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerCycleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerCycleSpinBox.setMinimum(1)
        self.facedetailerCycleSpinBox.setMaximum(10)
        self.facedetailerCycleSpinBox.setValue(1)

        self.verticalLayout_26.addWidget(self.facedetailerCycleSpinBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_26)

        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.facedetailerDropSizeLabel = QLabel(self.layoutWidget3)
        self.facedetailerDropSizeLabel.setObjectName(u"facedetailerDropSizeLabel")
        self.facedetailerDropSizeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_27.addWidget(self.facedetailerDropSizeLabel)

        self.facedetailerDropSizeSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerDropSizeSpinBox.setObjectName(u"facedetailerDropSizeSpinBox")
        self.facedetailerDropSizeSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerDropSizeSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerDropSizeSpinBox.setMinimum(0)
        self.facedetailerDropSizeSpinBox.setMaximum(100)
        self.facedetailerDropSizeSpinBox.setValue(10)

        self.verticalLayout_27.addWidget(self.facedetailerDropSizeSpinBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_27)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.comfyTabLayout.addWidget(self.facedetailerGroupBox)

        self.comfyTabSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.comfyTabLayout.addItem(self.comfyTabSpacer)

        self.tabWidget.addTab(self.comfyTab, "")
        self.lmstudioTab = QWidget()
        self.lmstudioTab.setObjectName(u"lmstudioTab")
        self.lmstudioTabLayout = QVBoxLayout(self.lmstudioTab)
        self.lmstudioTabLayout.setSpacing(10)
        self.lmstudioTabLayout.setObjectName(u"lmstudioTabLayout")
        self.lmgroupBox = QGroupBox(self.lmstudioTab)
        self.lmgroupBox.setObjectName(u"lmgroupBox")
        self.lmgroupBox.setMinimumSize(QSize(351, 201))
        self.lmAddressLabel = QLabel(self.lmgroupBox)
        self.lmAddressLabel.setObjectName(u"lmAddressLabel")
        self.lmAddressLabel.setGeometry(QRect(13, 45, 91, 20))
        self.lmUrlEdit = QLineEdit(self.lmgroupBox)
        self.lmUrlEdit.setObjectName(u"lmUrlEdit")
        self.lmUrlEdit.setGeometry(QRect(13, 70, 221, 41))
        sizePolicy.setHeightForWidth(self.lmUrlEdit.sizePolicy().hasHeightForWidth())
        self.lmUrlEdit.setSizePolicy(sizePolicy)
        self.lmUrlEdit.setMinimumSize(QSize(0, 32))
        self.lmTitleLabel = QLabel(self.lmgroupBox)
        self.lmTitleLabel.setObjectName(u"lmTitleLabel")
        self.lmTitleLabel.setGeometry(QRect(109, 15, 151, 25))
        font2 = QFont()
        font2.setFamilies([u"Cascadia Code"])
        self.lmTitleLabel.setFont(font2)
        self.lmTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lmStatusLabel = QLabel(self.lmgroupBox)
        self.lmStatusLabel.setObjectName(u"lmStatusLabel")
        self.lmStatusLabel.setGeometry(QRect(230, 40, 121, 31))
        self.lmStatusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lmCheckButton = QPushButton(self.lmgroupBox)
        self.lmCheckButton.setObjectName(u"lmCheckButton")
        self.lmCheckButton.setGeometry(QRect(240, 70, 101, 41))
        self.lmCheckButton.setMinimumSize(QSize(80, 32))
        self.lmModelLabel = QLabel(self.lmgroupBox)
        self.lmModelLabel.setObjectName(u"lmModelLabel")
        self.lmModelLabel.setGeometry(QRect(11, 121, 78, 16))
        self.lmModelCombo = QComboBox(self.lmgroupBox)
        self.lmModelCombo.setObjectName(u"lmModelCombo")
        self.lmModelCombo.setGeometry(QRect(11, 149, 104, 42))
        self.lmModelCombo.setMinimumSize(QSize(0, 42))

        self.lmstudioTabLayout.addWidget(self.lmgroupBox)

        self.lmstudioTabSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.lmstudioTabLayout.addItem(self.lmstudioTabSpacer)

        self.tabWidget.addTab(self.lmstudioTab, "")
        self.promptTab = QWidget()
        self.promptTab.setObjectName(u"promptTab")
        self.promptTabLayout = QVBoxLayout(self.promptTab)
        self.promptTabLayout.setSpacing(10)
        self.promptTabLayout.setObjectName(u"promptTabLayout")
        self.promptPanel = QGroupBox(self.promptTab)
        self.promptPanel.setObjectName(u"promptPanel")
        self.gridLayout_3 = QGridLayout(self.promptPanel)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(0)
        self.gridLayout_3.setVerticalSpacing(6)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.positivePromptHeaderLayout = QHBoxLayout()
        self.positivePromptHeaderLayout.setObjectName(u"positivePromptHeaderLayout")
        self.positivePromptLabel = QLabel(self.promptPanel)
        self.positivePromptLabel.setObjectName(u"positivePromptLabel")

        self.positivePromptHeaderLayout.addWidget(self.positivePromptLabel)

        self.positivePromptHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.positivePromptHeaderLayout.addItem(self.positivePromptHeaderSpacer)

        self.positivePromptCounterLabel = QLabel(self.promptPanel)
        self.positivePromptCounterLabel.setObjectName(u"positivePromptCounterLabel")
        self.positivePromptCounterLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.positivePromptHeaderLayout.addWidget(self.positivePromptCounterLabel)


        self.gridLayout_3.addLayout(self.positivePromptHeaderLayout, 0, 0, 1, 1)

        self.positivePromptEdit = QPlainTextEdit(self.promptPanel)
        self.positivePromptEdit.setObjectName(u"positivePromptEdit")

        self.gridLayout_3.addWidget(self.positivePromptEdit, 1, 0, 1, 1)

        self.negativePromptHeaderLayout = QHBoxLayout()
        self.negativePromptHeaderLayout.setObjectName(u"negativePromptHeaderLayout")
        self.negativePromptLabel = QLabel(self.promptPanel)
        self.negativePromptLabel.setObjectName(u"negativePromptLabel")

        self.negativePromptHeaderLayout.addWidget(self.negativePromptLabel)

        self.negativePromptHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.negativePromptHeaderLayout.addItem(self.negativePromptHeaderSpacer)

        self.negativePromptCounterLabel = QLabel(self.promptPanel)
        self.negativePromptCounterLabel.setObjectName(u"negativePromptCounterLabel")
        self.negativePromptCounterLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.negativePromptHeaderLayout.addWidget(self.negativePromptCounterLabel)


        self.gridLayout_3.addLayout(self.negativePromptHeaderLayout, 2, 0, 1, 1)

        self.negativePromptEdit = QPlainTextEdit(self.promptPanel)
        self.negativePromptEdit.setObjectName(u"negativePromptEdit")
        self.negativePromptEdit.setMaximumSize(QSize(16777215, 80))

        self.gridLayout_3.addWidget(self.negativePromptEdit, 3, 0, 1, 1)

        self.enhancePromptHeaderLayout = QHBoxLayout()
        self.enhancePromptHeaderLayout.setObjectName(u"enhancePromptHeaderLayout")
        self.enhancePromptLabel = QLabel(self.promptPanel)
        self.enhancePromptLabel.setObjectName(u"enhancePromptLabel")
        self.enhancePromptLabel.setFont(font)

        self.enhancePromptHeaderLayout.addWidget(self.enhancePromptLabel)

        self.enhancePromptHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.enhancePromptHeaderLayout.addItem(self.enhancePromptHeaderSpacer)

        self.enhancePromptButton = QPushButton(self.promptPanel)
        self.enhancePromptButton.setObjectName(u"enhancePromptButton")
        self.enhancePromptButton.setMinimumSize(QSize(0, 28))
        self.enhancePromptButton.setMaximumSize(QSize(16777215, 28))
        icon3 = QIcon()
        icon3.addFile(u":/newPrefix1/sparkel.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.enhancePromptButton.setIcon(icon3)

        self.enhancePromptHeaderLayout.addWidget(self.enhancePromptButton)

        self.enhancePromptCounterLabel = QLabel(self.promptPanel)
        self.enhancePromptCounterLabel.setObjectName(u"enhancePromptCounterLabel")
        self.enhancePromptCounterLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.enhancePromptHeaderLayout.addWidget(self.enhancePromptCounterLabel)


        self.gridLayout_3.addLayout(self.enhancePromptHeaderLayout, 4, 0, 1, 1)

        self.enhancePromptEdit = QPlainTextEdit(self.promptPanel)
        self.enhancePromptEdit.setObjectName(u"enhancePromptEdit")
        sizePolicy4.setHeightForWidth(self.enhancePromptEdit.sizePolicy().hasHeightForWidth())
        self.enhancePromptEdit.setSizePolicy(sizePolicy4)
        self.enhancePromptEdit.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_3.addWidget(self.enhancePromptEdit, 5, 0, 1, 1)

        self.gridLayout_3.setRowStretch(1, 1)

        self.promptTabLayout.addWidget(self.promptPanel)

        self.promptTabSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.promptTabLayout.addItem(self.promptTabSpacer)

        self.tabWidget.addTab(self.promptTab, "")
        self.resultTab = QWidget()
        self.resultTab.setObjectName(u"resultTab")
        self.resultTabLayout = QVBoxLayout(self.resultTab)
        self.resultTabLayout.setSpacing(10)
        self.resultTabLayout.setObjectName(u"resultTabLayout")
        self.resultPanel = QGroupBox(self.resultTab)
        self.resultPanel.setObjectName(u"resultPanel")
        self.resultPanel.setMinimumSize(QSize(250, 0))
        self.gridLayout = QGridLayout(self.resultPanel)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(2, -1, 2, 2)
        self.previewLabel = QLabel(self.resultPanel)
        self.previewLabel.setObjectName(u"previewLabel")
        self.previewLabel.setMinimumSize(QSize(200, 288))
        self.previewLabel.setFont(font)
        self.previewLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.previewLabel.setWordWrap(True)

        self.gridLayout.addWidget(self.previewLabel, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.openOutputFolderButton = QPushButton(self.resultPanel)
        self.openOutputFolderButton.setObjectName(u"openOutputFolderButton")
        self.openOutputFolderButton.setMinimumSize(QSize(100, 32))

        self.horizontalLayout.addWidget(self.openOutputFolderButton)

        self.saveImageButton = QPushButton(self.resultPanel)
        self.saveImageButton.setObjectName(u"saveImageButton")
        self.saveImageButton.setMinimumSize(QSize(100, 32))

        self.horizontalLayout.addWidget(self.saveImageButton)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 2)

        self.resultTabLayout.addWidget(self.resultPanel)

        self.resultTabSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.resultTabLayout.addItem(self.resultTabSpacer)

        self.tabWidget.addTab(self.resultTab, "")
        self.logTab = QWidget()
        self.logTab.setObjectName(u"logTab")
        self.logLayout = QVBoxLayout(self.logTab)
        self.logLayout.setSpacing(10)
        self.logLayout.setObjectName(u"logLayout")
        self.logHeaderRow = QHBoxLayout()
        self.logHeaderRow.setSpacing(10)
        self.logHeaderRow.setObjectName(u"logHeaderRow")
        self.toggleLogButton = QPushButton(self.logTab)
        self.toggleLogButton.setObjectName(u"toggleLogButton")
        icon4 = QIcon()
        icon4.addFile(u":/newPrefix1/toggle-off.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toggleLogButton.setIcon(icon4)
        self.toggleLogButton.setIconSize(QSize(55, 55))

        self.logHeaderRow.addWidget(self.toggleLogButton)

        self.logHeaderRowSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.logHeaderRow.addItem(self.logHeaderRowSpacer)


        self.logLayout.addLayout(self.logHeaderRow)

        self.logGroupBox = QGroupBox(self.logTab)
        self.logGroupBox.setObjectName(u"logGroupBox")
        sizePolicy6.setHeightForWidth(self.logGroupBox.sizePolicy().hasHeightForWidth())
        self.logGroupBox.setSizePolicy(sizePolicy6)
        self.logGroupBox.setMinimumSize(QSize(381, 100))
        self.logGroupBox.setMaximumSize(QSize(16777215, 16777215))
        self.logGroupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logTextEdit = QPlainTextEdit(self.logGroupBox)
        self.logTextEdit.setObjectName(u"logTextEdit")
        self.logTextEdit.setGeometry(QRect(11, 25, 1121, 551))
        self.logTextEdit.setReadOnly(True)
        self.resetButton = QPushButton(self.logGroupBox)
        self.resetButton.setObjectName(u"resetButton")
        self.resetButton.setGeometry(QRect(282, 25, 91, 32))
        sizePolicy6.setHeightForWidth(self.resetButton.sizePolicy().hasHeightForWidth())
        self.resetButton.setSizePolicy(sizePolicy6)
        self.resetButton.setMinimumSize(QSize(80, 32))

        self.logLayout.addWidget(self.logGroupBox)

        self.tabWidget.addTab(self.logTab, "")
        self.settingsTab = QWidget()
        self.settingsTab.setObjectName(u"settingsTab")
        self.settingsLayout = QVBoxLayout(self.settingsTab)
        self.settingsLayout.setSpacing(12)
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.actionButtonLayout = QHBoxLayout()
        self.actionButtonLayout.setObjectName(u"actionButtonLayout")
        self.restoreDefaultsButton = QPushButton(self.settingsTab)
        self.restoreDefaultsButton.setObjectName(u"restoreDefaultsButton")
        self.restoreDefaultsButton.setMinimumSize(QSize(100, 32))

        self.actionButtonLayout.addWidget(self.restoreDefaultsButton)

        self.loadConfigButton = QPushButton(self.settingsTab)
        self.loadConfigButton.setObjectName(u"loadConfigButton")
        self.loadConfigButton.setMinimumSize(QSize(100, 32))

        self.actionButtonLayout.addWidget(self.loadConfigButton)

        self.saveConfigButton = QPushButton(self.settingsTab)
        self.saveConfigButton.setObjectName(u"saveConfigButton")
        self.saveConfigButton.setMinimumSize(QSize(100, 32))

        self.actionButtonLayout.addWidget(self.saveConfigButton)


        self.settingsLayout.addLayout(self.actionButtonLayout)

        self.exitRow = QHBoxLayout()
        self.exitRow.setSpacing(10)
        self.exitRow.setObjectName(u"exitRow")
        self.exitButton = QPushButton(self.settingsTab)
        self.exitButton.setObjectName(u"exitButton")
        sizePolicy6.setHeightForWidth(self.exitButton.sizePolicy().hasHeightForWidth())
        self.exitButton.setSizePolicy(sizePolicy6)
        self.exitButton.setMinimumSize(QSize(120, 32))
        icon5 = QIcon()
        icon5.addFile(u":/newPrefix1/off-2.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exitButton.setIcon(icon5)

        self.exitRow.addWidget(self.exitButton)

        self.exitRowSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.exitRow.addItem(self.exitRowSpacer)


        self.settingsLayout.addLayout(self.exitRow)

        self.settingsSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.settingsLayout.addItem(self.settingsSpacer)

        self.tabWidget.addTab(self.settingsTab, "")
        self.helpTab = QWidget()
        self.helpTab.setObjectName(u"helpTab")
        self.helpTabLayout = QVBoxLayout(self.helpTab)
        self.helpTabLayout.setSpacing(10)
        self.helpTabLayout.setObjectName(u"helpTabLayout")
        self.helpBrowser = QTextBrowser(self.helpTab)
        self.helpBrowser.setObjectName(u"helpBrowser")
        sizePolicy6.setHeightForWidth(self.helpBrowser.sizePolicy().hasHeightForWidth())
        self.helpBrowser.setSizePolicy(sizePolicy6)
        self.helpBrowser.setOpenExternalLinks(True)

        self.helpTabLayout.addWidget(self.helpBrowser)

        self.helpTabSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.helpTabLayout.addItem(self.helpTabSpacer)

        self.tabWidget.addTab(self.helpTab, "")

        self.contentLayout.addWidget(self.tabWidget)


        self.mainLayout.addLayout(self.contentLayout)

        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(5)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ComfyUI + LMStudio Generator v0.3", None))
        self.appTitle.setText(QCoreApplication.translate("MainWindow", u"\u2726  ComfyUI + LMStudio", None))
        self.homeButton.setText(QCoreApplication.translate("MainWindow", u"\u2302   \ud648", None))
        self.pushButton.setText("")
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
        self.ComfygroupBox.setTitle("")
        self.comfyAddressLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f4e1 \U0000c11c\U0000bc84 \U0000c8fc\U0000c18c", None))
        self.comfyUrlEdit.setText(QCoreApplication.translate("MainWindow", u"http://127.0.0.1:8188", None))
        self.comfyPathLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c1 \U0000baa8\U0000b378 \U0000d3f4\U0000b354", None))
        self.comfyModelPathEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"ComfyUI \ubaa8\ub378 \ud3f4\ub354 \uacbd\ub85c", None))
        self.comfyStatusLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f4e1\U0000c5f0\U0000acb0 \U0000d655\U0000c778 \U0000c911...", None))
        self.comfyTitleLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f3a8 ComfyUI", None))
        self.comfyCheckButton.setText(QCoreApplication.translate("MainWindow", u"\uc5f0\uacb0 \ud655\uc778", None))
        self.modelPathStatusLabel.setText(QCoreApplication.translate("MainWindow", u"\u2713 \ubaa8\ub378 \ud3f4\ub354 \ud655\uc778", None))
        self.browseModelFolderButton.setText(QCoreApplication.translate("MainWindow", u"\ucc3e\uc544\ubcf4\uae30", None))
        self.comfyModelLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f4e6 \U0000baa8\U0000b378 \U0000c120\U0000d0dd", None))
        self.generationPanel.setTitle(QCoreApplication.translate("MainWindow", u"\u2699\ufe0f Generation options", None))
        self.preset_512x512.setText(QCoreApplication.translate("MainWindow", u"512\u00d7512", None))
        self.preset_768x768.setText(QCoreApplication.translate("MainWindow", u"768\u00d7768", None))
        self.preset_1024x1024.setText(QCoreApplication.translate("MainWindow", u"1024\u00d71024", None))
        self.preset_832x1216.setText(QCoreApplication.translate("MainWindow", u"832\u00d71216", None))
        self.preset_1216x832.setText(QCoreApplication.translate("MainWindow", u"1216\u00d7832", None))
        self.widthLabel.setText(QCoreApplication.translate("MainWindow", u"\uac00\ub85c", None))
        self.heightLabel.setText(QCoreApplication.translate("MainWindow", u"\uc138\ub85c", None))
        self.stepsLabel.setText(QCoreApplication.translate("MainWindow", u"Steps", None))
        self.cfgLabel.setText(QCoreApplication.translate("MainWindow", u"CFG", None))
        self.seedLabel.setText(QCoreApplication.translate("MainWindow", u"Seed", None))
        self.denoiseLabel.setText(QCoreApplication.translate("MainWindow", u"Denoise", None))
        self.samplerLabel.setText(QCoreApplication.translate("MainWindow", u"Sampler", None))
#if QT_CONFIG(tooltip)
        self.samplerComboBox.setToolTip(QCoreApplication.translate("MainWindow", u"SAMPLER_OPTIONS(\"dpmpp_2m_sde\", \"SDE \uae30\ubc18\uc73c\ub85c \ub514\ud14c\uc77c\uc774 \ub6f0\uc5b4\ub098\uba70, \ubd80\ub4dc\ub7ec\uc6b4 \uacb0\uacfc\ubb3c\uc744 \uc0dd\uc131\ud569\ub2c8\ub2e4.\"),(\"dpmpp_2m\", \"\uac00\uc7a5 \ubcf4\ud3b8\uc801\uc73c\ub85c \uc0ac\uc6a9\ub418\uba70 \uc18d\ub3c4\uc640 \ud488\uc9c8\uc758 \uade0\ud615\uc774 \ud6cc\ub96d\ud569\ub2c8\ub2e4.\"),(\"euler\", \"\ube60\ub974\uace0 \uc548\uc815\uc801\uc774\uba70 \uae54\ub054\ud55c \uacb0\uacfc\ubb3c\uc744 \uc6d0\ud560 \ub54c \uc801\ud569\ud569\ub2c8\ub2e4.\"),(\"euler_ancestral\", \"\ub9e4 \uc2a4\ud15d\ub9c8\ub2e4 \ub178\uc774\uc988\ub97c \ucd94\uac00\ud558\uc5ec \ub2e4\uc591\ud55c \ubcc0\ud615\uc744 \uc2dc\ub3c4\ud569\ub2c8\ub2e4.\"),(\"lcm\", \"\uc801\uc740 \uc2a4\ud15d(4~8)\uc73c\ub85c\ub3c4 \ube60\ub974\uac8c \uc0dd\uc131\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.\"),(\"ddim\", \"\uc77c\uad00\uc131\uc774 \ub192\uace0 \uc548\uc815\uc801\uc778 \uc0dd\uc131\uc744 \ubcf4\uc7a5\ud569\ub2c8\ub2e4.\"),", None))
#endif // QT_CONFIG(tooltip)
        self.schedulerLabel.setText(QCoreApplication.translate("MainWindow", u"Scheduler", None))
#if QT_CONFIG(tooltip)
        self.schedulerComboBox.setToolTip(QCoreApplication.translate("MainWindow", u"SCHEDULER_OPTIONS (\"normal\", \"\uac00\uc7a5 \ubb34\ub09c\ud558\uace0 \uae30\ubcf8\uc801\uc778 \ub178\uc774\uc988 \uc2a4\ucf00\uc904\uc785\ub2c8\ub2e4.\"), (\"karras\", \"\uace0\ud654\uc9c8 \uc774\ubbf8\uc9c0 \uc0dd\uc131\uc5d0 \uac15\ud558\uba70 \ub514\ud14c\uc77c\uc744 \uc0b4\ub9ac\ub294 \ub370 \ud6a8\uacfc\uc801\uc785\ub2c8\ub2e4.\"), (\"exponential\", \"\uc9c0\uc218\uc801\uc73c\ub85c \ubcc0\ud654\ud558\uba70 \ubd80\ub4dc\ub7ec\uc6b4 \uac10\uc1e0\ub97c \uc81c\uacf5\ud569\ub2c8\ub2e4.\"), (\"sgm_uniform\", \"SGM \ub178\uc774\uc988 \uc2a4\ucf00\uc904\uc744 \uc0ac\uc6a9\ud558\uba70 \uc77c\uc815\ud55c \uac04\uaca9\uc744 \uac00\uc9d1\ub2c8\ub2e4.\"), (\"simple\", \"\ubcf5\uc7a1\ud55c \uacc4\uc0b0 \uc5c6\uc774 \ub2e8\uc21c\ud55c \uc120\ud615 \uc2a4\ucf00\uc904\uc785\ub2c8\ub2e4.\"), (\"ddim_uniform\", \"DDIM\uc758 \uade0\uc77c\ud55c \ub178\uc774\uc988 \uc2a4\ucf00\uc904\uc744 \ub530\ub985\ub2c8\ub2e4.\"), (\"beta\", \"\ubca0\ud0c0 \ubd84\ud3ec\ub97c \ub530\ub974\ub294 \ub178\uc774\uc988 \uc2a4\ucf00\uc904\uc785\ub2c8"
                        "\ub2e4.\"), (\"linear_quadratic\", \"\uc120\ud615\uacfc \uc774\ucc28 \ud568\uc218\uac00 \ud63c\ud569\ub41c \ub3c5\ud2b9\ud55c \uc2a4\ucf00\uc904\uc785\ub2c8\ub2e4.\"), (\"kl_optimal\", \"KL \ubc1c\uc0b0\uc744 \ucd5c\uc801\ud654\ud558\uc5ec \uc218\ub834 \uc18d\ub3c4\ub97c \ub192\uc785\ub2c8\ub2e4.\"),", None))
#endif // QT_CONFIG(tooltip)
        self.executionPanel.setTitle(QCoreApplication.translate("MainWindow", u"\u25b6\ufe0f Launch", None))
        self.progressStatusLabel.setText(QCoreApplication.translate("MainWindow", u"\uc900\ube44 \uc644\ub8cc", None))
        self.elapsedLabel.setText(QCoreApplication.translate("MainWindow", u"0\ucd08", None))
        self.progressPercentLabel.setText(QCoreApplication.translate("MainWindow", u"0%", None))
        self.generateButton.setText(QCoreApplication.translate("MainWindow", u"\uc774\ubbf8\uc9c0 \uc0dd\uc131 \uc2dc\uc791", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc9c0", None))
#if QT_CONFIG(tooltip)
        self.facedetailerGroupBox.setToolTip(QCoreApplication.translate("MainWindow", u"FaceDetailer\ub294 ComfyUI Impact Pack\uc758 \ub178\ub4dc\ub85c, \uc0dd\uc131\ub41c \uc774\ubbf8\uc9c0\uc5d0\uc11c \uc5bc\uad74\uc744 \uac10\uc9c0\ud558\uc5ec \ubcc4\ub3c4\uc758 \ud30c\ub77c\ubbf8\ud130\ub85c\uc5bc\uad74 \uc601\uc5ed\ub9cc \uc7ac\uc0dd\uc131\ud558\uc5ec \ub514\ud14c\uc77c\uc744 \ubcf4\uc815\ud569\ub2c8\ub2e4.\uae30\uc874 \uc0dd\uc131 \uc635\uc158(CFG, Steps \ub4f1)\uacfc \ubcc4\ub3c4\ub85c \ub3d9\uc791\ud558\uba70, \uc5bc\uad74 \uc601\uc5ed\ub9cc \ub354 \uc12c\uc138\ud558\uac8c/\uac15\ud558\uac8c \ubcf4\uc815\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.\ud544\uc218 \uc870\uac74: ComfyUI\uc5d0 Impact Pack \uc124\uce58 \ud544\uc694 (FaceDetailer, UltralyticsDetectorProvider \ub178\ub4dc \ud3ec\ud568)", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\U0001f464 FaceDetailer (\U0000c5bc\U0000ad74 \U0000bcf4\U0000c815)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerCheckBox.setToolTip(QCoreApplication.translate("MainWindow", u"FaceDetailer \uc5bc\uad74 \ubcf4\uc815 \uae30\ub2a5 \ucf1c\uae30/\ub044\uae30 \uccb4\ud06c \uc2dc: \uc804\uccb4 \uc774\ubbf8\uc9c0\uc0dd\uc131 \ud6c4 \uc5bc\uad74 \uc601\uc5ed\ub9cc \ubcc4\ub3c4\ub85c \ubcf4\uc815 \ud574\uc81c \uc2dc: \ubcf4\uc815 \uc5c6\uc774, \uc77c\ubc18 \uc774\ubbf8\uc9c0\uc0dd\uc131\ub9cc \uc218\ud589 \ud544\uc218: ComfyUI Impact Pack \uc124\uce58 \ud544\uc694", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerCheckBox.setText("")
#if QT_CONFIG(tooltip)
        self.facedetailerDenoiseLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc7ac\uc0dd\uc131 \uc2dc \uc6d0\ubcf8 \uc720\uc9c0 \uac15\ub3c4 (0.0~1.0) \ub0ae\uc744\uc218\ub85d \uc6d0\ubcf8 \uc5bc\uad74 \ud615\ud0dc \uc720\uc9c0, \ub192\uc744\uc218\ub85d \ud504\ub86c\ud504\ud2b8 \ubc18\uc601 \uac15\ud568 \uae30\ubcf8 0.4: \uc6d0\ubcf8 \uc5bc\uad74 \uc720\uc9c0\ud558\uba74\uc11c \ub514\ud14c\uc77c \ubcf4\uac15 \u203b \uc804\uccb4 \uc0dd\uc131\uc758 Denoise\uc640 \ubcc4\ub3c4 \ub3d9\uc791", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerDenoiseLabel.setText(QCoreApplication.translate("MainWindow", u"Denoise", None))
#if QT_CONFIG(tooltip)
        self.facedetailerDenoiseSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc7ac\uc0dd\uc131 \uc2dc \uc6d0\ubcf8 \uc720\uc9c0 \uac15\ub3c4 (0.0~1.0) \ub0ae\uc744\uc218\ub85d \uc6d0\ubcf8 \uc5bc\uad74 \ud615\ud0dc \uc720\uc9c0, \ub192\uc744\uc218\ub85d \ud504\ub86c\ud504\ud2b8 \ubc18\uc601 \uac15\ud568 \uae30\ubcf8 0.4: \uc6d0\ubcf8 \uc5bc\uad74 \uc720\uc9c0\ud558\uba74\uc11c \ub514\ud14c\uc77c \ubcf4\uac15 \u203b \uc804\uccb4 \uc0dd\uc131\uc758 Denoise\uc640 \ubcc4\ub3c4 \ub3d9\uc791", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerStepsLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc7ac\uc0dd\uc131 \ubc18\ubcf5 \ud69f\uc218 (1~50) \ub192\uc744\uc218\ub85d \ub514\ud14c\uc77c \ud5a5\uc0c1, \uc0dd\uc131 \uc2dc\uac04 \uc99d\uac00 \uae30\ubcf8 20: \uc801\uc808\ud55c \ud488\uc9c8/\uc18d\ub3c4 \uade0\ud615 \u203b \uc804\uccb4 \uc0dd\uc131\uc758 Steps\uc640 \ubcc4\ub3c4 \ub3d9\uc791", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerStepsLabel.setText(QCoreApplication.translate("MainWindow", u"Steps", None))
#if QT_CONFIG(tooltip)
        self.facedetailerStepsSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc7ac\uc0dd\uc131 \ubc18\ubcf5 \ud69f\uc218 (1~50) \ub192\uc744\uc218\ub85d \ub514\ud14c\uc77c \ud5a5\uc0c1, \uc0dd\uc131 \uc2dc\uac04 \uc99d\uac00 \uae30\ubcf8 20: \uc801\uc808\ud55c \ud488\uc9c8/\uc18d\ub3c4 \uade0\ud615 \u203b \uc804\uccb4 \uc0dd\uc131\uc758 Steps\uc640 \ubcc4\ub3c4 \ub3d9\uc791", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerCfgLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc7ac\uc0dd\uc131 \uc2dc \ud504\ub86c\ud504\ud2b8 \uc900\uc218\ub3c4 (0~20) \ub192\uc744\uc218\ub85d \ud504\ub86c\ud504\ud2b8 \uac15\ub825 \ubc18\uc601, \ub0ae\uc744\uc218\ub85d \uc790\uc720\ub85c\uc6b4 \uc0dd\uc131 \uae30\ubcf8 4.0: \uc790\uc5f0\uc2a4\ub7ec\uc6b4 \uc5bc\uad74 \ubcf4\uc815 \u203b \uc804\uccb4 \uc0dd\uc131\uc758 CFG\uc640 \ubcc4\ub3c4 \ub3d9\uc791", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerCfgLabel.setText(QCoreApplication.translate("MainWindow", u"CFG", None))
#if QT_CONFIG(tooltip)
        self.facedetailerCfgSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc7ac\uc0dd\uc131 \uc2dc \ud504\ub86c\ud504\ud2b8 \uc900\uc218\ub3c4 (0~20) \ub192\uc744\uc218\ub85d \ud504\ub86c\ud504\ud2b8 \uac15\ub825 \ubc18\uc601, \ub0ae\uc744\uc218\ub85d \uc790\uc720\ub85c\uc6b4 \uc0dd\uc131 \uae30\ubcf8 4.0: \uc790\uc5f0\uc2a4\ub7ec\uc6b4 \uc5bc\uad74 \ubcf4\uc815 \u203b \uc804\uccb4 \uc0dd\uc131\uc758 CFG\uc640 \ubcc4\ub3c4 \ub3d9\uc791", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerGuideSizeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"FaceDetailer \uc804\uc6a9: \uc5bc\uad74 \ud06c\ub86d\uc744 \uc5c5\uc2a4\ucf00\uc77c\ud560 \ud0c0\uac9f \ud574\uc0c1\ub3c4 \uc5bc\uad74 \uc601\uc5ed\uc744 \uc774 \ud06c\uae30\ub85c \ud0a4\uc6cc\uc11c \ub514\ud14c\uc77c\ud558\uac8c \uc7ac\uc0dd\uc131 \ud6c4 \uc6d0\ubcf8\uc5d0 \ud569\uc131 \uae30\ubcf8 256: 256x256\uc73c\ub85c \uc5c5\uc2a4\ucf00\uc77c\ud558\uc5ec \uc138\ubc00 \ubcf4\uc815 \u203b \uc804\uccb4 \uc774\ubbf8\uc9c0 \ud574\uc0c1\ub3c4(\uac00\ub85c/\uc138\ub85c)\uc640 \ubb34\uad00", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerGuideSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Guide Size", None))
#if QT_CONFIG(tooltip)
        self.facedetailerGuideSizeSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"FaceDetailer \uc804\uc6a9: \uc5bc\uad74 \ud06c\ub86d\uc744 \uc5c5\uc2a4\ucf00\uc77c\ud560 \ud0c0\uac9f \ud574\uc0c1\ub3c4 \uc5bc\uad74 \uc601\uc5ed\uc744 \uc774 \ud06c\uae30\ub85c \ud0a4\uc6cc\uc11c \ub514\ud14c\uc77c\ud558\uac8c \uc7ac\uc0dd\uc131 \ud6c4 \uc6d0\ubcf8\uc5d0 \ud569\uc131 \uae30\ubcf8 256: 256x256\uc73c\ub85c \uc5c5\uc2a4\ucf00\uc77c\ud558\uc5ec \uc138\ubc00 \ubcf4\uc815 \u203b \uc804\uccb4 \uc774\ubbf8\uc9c0 \ud574\uc0c1\ub3c4(\uac00\ub85c/\uc138\ub85c)\uc640 \ubb34\uad00", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerMaxSizeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"FaceDetailer \uc804\uc6a9: \uc5bc\uad74 \ud06c\ub86d \ucd5c\ub300 \ud06c\uae30 \uc81c\ud55c (VRAM \uc808\uc57d) \ub108\ubb34 \ud070 \uc5bc\uad74 \ud06c\ub86d \ubc29\uc9c0\ub85c \uba54\ubaa8\ub9ac \ubd80\uc871 \ubc29\uc9c0 \uae30\ubcf8 768: 768px \ucd08\uacfc \uc5bc\uad74\uc740 \ub2e4\uc6b4\uc2a4\ucf00\uc77c \ud6c4 \ucc98\ub9ac \u203b \uc804\uccb4 \uc774\ubbf8\uc9c0 \ud574\uc0c1\ub3c4\uc640 \ubb34\uad00", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerMaxSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Max Size", None))
#if QT_CONFIG(tooltip)
        self.facedetailerFeatherLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ud569\uc131 \uacbd\uacc4\uc120 \ube14\ub7ec \ucc98\ub9ac (0~20) \ub192\uc744\uc218\ub85d \uacbd\uacc4 \uc790\uc5f0\uc2a4\ub7ec\uc6c0, \ub0ae\uc744\uc218\ub85d \uc120\uba85 \uae30\ubcf8 5: \uc790\uc5f0\uc2a4\ub7ec\uc6b4 \ud569\uc131 \u203b \uc5bc\uad74 \ub9c8\uc2a4\ud06c \uacbd\uacc4 \ubd80\ub4dc\ub7fd\uac8c \ucc98\ub9ac", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerFeatherLabel.setText(QCoreApplication.translate("MainWindow", u"Feather", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxThresholdLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uac10\uc9c0 \uc2e0\ub8b0\ub3c4 \uc784\uacc4\uac12 (0.0~1.0) \ub0ae\uc744\uc218\ub85d \ub354 \ub9ce\uc740 \uc5bc\uad74 \uac10\uc9c0, \ub192\uc744\uc218\ub85d \ud655\uc2e4\ud55c \uc5bc\uad74\ub9cc \uac10\uc9c0 \uae30\ubcf8 0.5", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerBboxThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"BBox Thresh", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxThresholdSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uac10\uc9c0 \uc2e0\ub8b0\ub3c4 \uc784\uacc4\uac12 (0.0~1.0) \ub0ae\uc744\uc218\ub85d \ub354 \ub9ce\uc740 \uc5bc\uad74 \uac10\uc9c0, \ub192\uc744\uc218\ub85d \ud655\uc2e4\ud55c \uc5bc\uad74\ub9cc \uac10\uc9c0 \uae30\ubcf8 0.5", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerBboxDilationLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uac10\uc9c0\ub41c \uc5bc\uad74 \ubc14\uc6b4\ub529 \ubc15\uc2a4 \ud655\uc7a5 \ud53d\uc140 (0~100) \ub192\uc744\uc218\ub85d \uc5bc\uad74 \uc8fc\ubcc0 \uc601\uc5ed \ud3ec\ud568 \uae30\ubcf8 10", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerBboxDilationLabel.setText(QCoreApplication.translate("MainWindow", u"BBox Dilate", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxDilationSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uac10\uc9c0\ub41c \uc5bc\uad74 \ubc14\uc6b4\ub529 \ubc15\uc2a4 \ud655\uc7a5 \ud53d\uc140 (0~100) \ub192\uc744\uc218\ub85d \uc5bc\uad74 \uc8fc\ubcc0 \uc601\uc5ed \ud3ec\ud568 \uae30\ubcf8 10", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerBboxCropFactorLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ud06c\ub86d \uc601\uc5ed \ube44\uc728 (1.0~3.0) \ub192\uc744\uc218\ub85d \ub354 \ub113\uc740 \uc5bc\uad74 \uc601\uc5ed \ud06c\ub86d \uae30\ubcf8 1.5", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerBboxCropFactorLabel.setText(QCoreApplication.translate("MainWindow", u"Crop Factor", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxCropFactorSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ud06c\ub86d \uc601\uc5ed \ube44\uc728 (1.0~3.0) \ub192\uc744\uc218\ub85d \ub354 \ub113\uc740 \uc5bc\uad74 \uc601\uc5ed \ud06c\ub86d \uae30\ubcf8 1.5", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerSamDetectionHintLabel.setToolTip(QCoreApplication.translate("MainWindow", u"SAM \uc5bc\uad74 \uac10\uc9c0 \ud78c\ud2b8 \ubaa8\ub4dc center-1: \uc911\uc559 \ub2e8\uc77c \uc5bc\uad74 center-2: \uc911\uc559 \ub450 \uc5bc\uad74 center-3: \uc911\uc559 \uc138 \uc5bc\uad74 center-4: \uc911\uc559 \ub124 \uc5bc\uad74 all: \ubaa8\ub4e0 \uc5bc\uad74 \uae30\ubcf8 center-1", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamDetectionHintLabel.setText(QCoreApplication.translate("MainWindow", u"SAM Hint", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamDetectionHintComboBox.setToolTip(QCoreApplication.translate("MainWindow", u"SAM \uc5bc\uad74 \uac10\uc9c0 \ud78c\ud2b8 \ubaa8\ub4dc center-1: \uc911\uc559 \ub2e8\uc77c \uc5bc\uad74 center-2: \uc911\uc559 \ub450 \uc5bc\uad74 center-3: \uc911\uc559 \uc138 \uc5bc\uad74 center-4: \uc911\uc559 \ub124 \uc5bc\uad74 all: \ubaa8\ub4e0 \uc5bc\uad74 \uae30\ubcf8 center-1", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerSamDilationLabel.setToolTip(QCoreApplication.translate("MainWindow", u"SAM \ub9c8\uc2a4\ud06c \ud655\uc7a5/\ucd95\uc18c \ud53d\uc140 (0~100) \uc591\uc218: \ub9c8\uc2a4\ud06c \ud655\uc7a5, \uc74c\uc218: \ub9c8\uc2a4\ud06c \ucd95\uc18c \uae30\ubcf8 0", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamDilationLabel.setText(QCoreApplication.translate("MainWindow", u"SAM Dilate", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamDilationSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"SAM \ub9c8\uc2a4\ud06c \ud655\uc7a5/\ucd95\uc18c \ud53d\uc140 (0~100) \uc591\uc218: \ub9c8\uc2a4\ud06c \ud655\uc7a5, \uc74c\uc218: \ub9c8\uc2a4\ud06c \ucd95\uc18c \uae30\ubcf8 0", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerSamThresholdLabel.setToolTip(QCoreApplication.translate("MainWindow", u"SAM \ub9c8\uc2a4\ud06c \uc2e0\ub8b0\ub3c4 \uc784\uacc4\uac12 (0.0~1.0) \ub192\uc744\uc218\ub85d \uc5c4\uaca9\ud55c \ub9c8\uc2a4\ud06c \uae30\ubcf8 0.93", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"SAM Thresh", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamThresholdSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"SAM \ub9c8\uc2a4\ud06c \uc2e0\ub8b0\ub3c4 \uc784\uacc4\uac12 (0.0~1.0) \ub192\uc744\uc218\ub85d \uc5c4\uaca9\ud55c \ub9c8\uc2a4\ud06c \uae30\ubcf8 0.93", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerSamBboxExpansionLabel.setToolTip(QCoreApplication.translate("MainWindow", u"SAM \ubc14\uc6b4\ub529 \ubc15\uc2a4 \ud655\uc7a5 \ud53d\uc140 (0~100) \uae30\ubcf8 0", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamBboxExpansionLabel.setText(QCoreApplication.translate("MainWindow", u"SAM BBox Exp", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamBboxExpansionSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"SAM \ubc14\uc6b4\ub529 \ubc15\uc2a4 \ud655\uc7a5 \ud53d\uc140 (0~100) \uae30\ubcf8 0", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintThresholdLabel.setToolTip(QCoreApplication.translate("MainWindow", u"SAM \ub9c8\uc2a4\ud06c \ud78c\ud2b8 \uc784\uacc4\uac12 (0.0~1.0) \uae30\ubcf8 0.7", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"Mask Hint Thresh", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintThresholdSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"SAM \ub9c8\uc2a4\ud06c \ud78c\ud2b8 \uc784\uacc4\uac12 (0.0~1.0) \uae30\ubcf8 0.7", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintUseNegativeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"SAM \ub9c8\uc2a4\ud06c \ud78c\ud2b8 \ub124\uac70\ud2f0\ube0c \uc0ac\uc6a9 False: \uc0ac\uc6a9 \uc548\ud568, Small: \uc791\uc740 \uc601\uc5ed, Outter: \ubc14\uae65 \uc601\uc5ed \uae30\ubcf8 False", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintUseNegativeLabel.setText(QCoreApplication.translate("MainWindow", u"Mask Hint Neg", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintUseNegativeComboBox.setToolTip(QCoreApplication.translate("MainWindow", u"SAM \ub9c8\uc2a4\ud06c \ud78c\ud2b8 \ub124\uac70\ud2f0\ube0c \uc0ac\uc6a9 False: \uc0ac\uc6a9 \uc548\ud568, Small: \uc791\uc740 \uc601\uc5ed, Outter: \ubc14\uae65 \uc601\uc5ed \uae30\ubcf8 False", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerCycleLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ubcf4\uc815 \ubc18\ubcf5 \ud69f\uc218 (1~10) \ub192\uc744\uc218\ub85d \ub354 \uc815\uad50\ud55c \ubcf4\uc815, \uc2dc\uac04 \uc99d\uac00 \uae30\ubcf8 1", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerCycleLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle", None))
#if QT_CONFIG(tooltip)
        self.facedetailerCycleSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ubcf4\uc815 \ubc18\ubcf5 \ud69f\uc218 (1~10) \ub192\uc744\uc218\ub85d \ub354 \uc815\uad50\ud55c \ubcf4\uc815, \uc2dc\uac04 \uc99d\uac00 \uae30\ubcf8 1", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerDropSizeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc791\uc740 \uc5bc\uad74 \ud544\ud130\ub9c1 \ud06c\uae30 (0~100) \uc774 \ud06c\uae30 \ubbf8\ub9cc \uc5bc\uad74\uc740 \ubcf4\uc815 \uc81c\uc678 \uae30\ubcf8 10", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerDropSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Drop Size", None))
#if QT_CONFIG(tooltip)
        self.facedetailerDropSizeSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uc791\uc740 \uc5bc\uad74 \ud544\ud130\ub9c1 \ud06c\uae30 (0~100) \uc774 \ud06c\uae30 \ubbf8\ub9cc \uc5bc\uad74\uc740 \ubcf4\uc815 \uc81c\uc678 \uae30\ubcf8 10", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.comfyTab), QCoreApplication.translate("MainWindow", u"\u25c8   ComfyUI", None))
        self.lmgroupBox.setTitle("")
        self.lmAddressLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f4e1 \U0000c11c\U0000bc84 \U0000c8fc\U0000c18c", None))
        self.lmUrlEdit.setText(QCoreApplication.translate("MainWindow", u"http://127.0.0.1:1729", None))
        self.lmTitleLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f9e0 LM Studio", None))
        self.lmStatusLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f4e1\U0000c5f0\U0000acb0 \U0000d655\U0000c778 \U0000c911...", None))
        self.lmCheckButton.setText(QCoreApplication.translate("MainWindow", u"\uc5f0\uacb0 \ud655\uc778", None))
        self.lmModelLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f4e6 \U0000baa8\U0000b378 \U0000c120\U0000d0dd", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.lmstudioTab), QCoreApplication.translate("MainWindow", u"\u25c6   LMStudio", None))
        self.promptPanel.setTitle(QCoreApplication.translate("MainWindow", u"\u270d\ufe0f Prompt", None))
        self.positivePromptLabel.setText(QCoreApplication.translate("MainWindow", u"Positive Prompt", None))
        self.positivePromptCounterLabel.setText(QCoreApplication.translate("MainWindow", u"0 / 2000", None))
        self.positivePromptEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\uc0dd\uc131\ud558\uace0 \uc2f6\uc740 \uc774\ubbf8\uc9c0\uc5d0 \ub300\ud55c \uc124\uba85\uc744 \uc785\ub825\ud558\uc138\uc694.", None))
        self.negativePromptLabel.setText(QCoreApplication.translate("MainWindow", u"Negative Prompt", None))
        self.negativePromptCounterLabel.setText(QCoreApplication.translate("MainWindow", u"0 / 2000", None))
        self.negativePromptEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\uc0dd\uc131\ud558\uc9c0 \uc54a\uc744 \uc694\uc18c\ub97c \uc785\ub825\ud558\uc138\uc694.", None))
        self.enhancePromptLabel.setText(QCoreApplication.translate("MainWindow", u"AI enhancePrompt", None))
#if QT_CONFIG(tooltip)
        self.enhancePromptButton.setToolTip(QCoreApplication.translate("MainWindow", u"LM Studio\ub97c \uc0ac\uc6a9\ud558\uc5ec \ud504\ub86c\ud504\ud2b8\ub97c \ud5a5\uc0c1\uc2dc\ud0b5\ub2c8\ub2e4", None))
#endif // QT_CONFIG(tooltip)
        self.enhancePromptButton.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub86c\ud504\ud2b8 \ud5a5\uc0c1", None))
        self.enhancePromptCounterLabel.setText(QCoreApplication.translate("MainWindow", u"0 / 2000", None))
        self.enhancePromptEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\ud504\ub86c\ud504\ud2b8 \ud5a5\uc0c1 \ubc84\ud2bc\uc744 \ub204\ub974\uace0 \uc7a0\uc2dc \uae30\ub2e4\ub9ac\uba74 ai\uac00 \ud5a5\uc0c1\ub41c \ud504\ub86c\ud504\ud2b8\ub97c \uc785\ub825\ud574\uc90d\ub2c8\ub2e4.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.promptTab), QCoreApplication.translate("MainWindow", u"\u270d\ufe0f   Prompt", None))
        self.resultPanel.setTitle(QCoreApplication.translate("MainWindow", u"\U0001f5bc\U0000fe0f Image preview", None))
        self.previewLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f5bc\U0000fe0f", None))
        self.openOutputFolderButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c2 Open", None))
        self.saveImageButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4be Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.resultTab), QCoreApplication.translate("MainWindow", u"\U0001f5bc\U0000fe0f   Result", None))
        self.toggleLogButton.setText("")
        self.logGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\U0001f4cb View live logs", None))
        self.logTextEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\ub85c\uadf8\uac00 \uc5ec\uae30\uc5d0 \ud45c\uc2dc\ub429\ub2c8\ub2e4...", None))
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f5d1\U0000fe0f Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logTab), QCoreApplication.translate("MainWindow", u"\U0001f4cb   Log", None))
        self.restoreDefaultsButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f504\U0000ae30\U0000bcf8\U0000ac12 \U0000bcf5\U0000c6d0", None))
        self.loadConfigButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c2 \U0000c124\U0000c815 \U0000bd88\U0000b7ec\U0000c624\U0000ae30", None))
        self.saveConfigButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4be \U0000c124\U0000c815 \U0000c800\U0000c7a5", None))
        self.exitButton.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), QCoreApplication.translate("MainWindow", u"\u2699\ufe0f   Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.helpTab), QCoreApplication.translate("MainWindow", u"\u2753   Help", None))
    # retranslateUi

