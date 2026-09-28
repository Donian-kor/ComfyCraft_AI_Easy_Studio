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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QPlainTextEdit, QPushButton, QScrollArea,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1100, 700)
        MainWindow.setMinimumSize(QSize(1100, 700))
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.gridLayout_3 = QGridLayout(self.centralWidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.headerFrame = QFrame(self.centralWidget)
        self.headerFrame.setObjectName(u"headerFrame")
        self.headerFrame.setMinimumSize(QSize(0, 60))
        self.headerFrame.setMaximumSize(QSize(16777215, 60))
        self.headerFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.headerLayout = QHBoxLayout(self.headerFrame)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(12, 4, 12, 4)
        self.appTitle = QLabel(self.headerFrame)
        self.appTitle.setObjectName(u"appTitle")

        self.headerLayout.addWidget(self.appTitle)

        self.newChatBtn = QPushButton(self.headerFrame)
        self.newChatBtn.setObjectName(u"newChatBtn")
        self.newChatBtn.setMinimumSize(QSize(120, 30))
        self.newChatBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.headerLayout.addWidget(self.newChatBtn)

        self.headerSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)

        self.comfyStatusBtn = QPushButton(self.headerFrame)
        self.comfyStatusBtn.setObjectName(u"comfyStatusBtn")
        self.comfyStatusBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.headerLayout.addWidget(self.comfyStatusBtn)

        self.lmStatusBtn = QPushButton(self.headerFrame)
        self.lmStatusBtn.setObjectName(u"lmStatusBtn")
        self.lmStatusBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.headerLayout.addWidget(self.lmStatusBtn)

        self.themeComboBox = QComboBox(self.headerFrame)
        self.themeComboBox.setObjectName(u"themeComboBox")
        self.themeComboBox.setMinimumSize(QSize(170, 30))

        self.headerLayout.addWidget(self.themeComboBox)


        self.gridLayout_3.addWidget(self.headerFrame, 0, 0, 1, 1)

        self.studioContainer = QFrame(self.centralWidget)
        self.studioContainer.setObjectName(u"studioContainer")
        self.studioContainer.setFrameShape(QFrame.Shape.NoFrame)
        self.studioLayout = QHBoxLayout(self.studioContainer)
        self.studioLayout.setSpacing(0)
        self.studioLayout.setObjectName(u"studioLayout")
        self.studioLayout.setContentsMargins(0, 0, 0, 0)
        self.railFrame = QFrame(self.studioContainer)
        self.railFrame.setObjectName(u"railFrame")
        self.railFrame.setMinimumSize(QSize(76, 0))
        self.railFrame.setMaximumSize(QSize(76, 16777215))
        self.railFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.railLayout = QVBoxLayout(self.railFrame)
        self.railLayout.setSpacing(6)
        self.railLayout.setObjectName(u"railLayout")
        self.railLayout.setContentsMargins(8, 8, 8, 8)
        self.railHomeBtn = QPushButton(self.railFrame)
        self.railHomeBtn.setObjectName(u"railHomeBtn")
        self.railHomeBtn.setMinimumSize(QSize(60, 55))
        self.railHomeBtn.setMaximumSize(QSize(60, 55))
        self.railHomeBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.railLayout.addWidget(self.railHomeBtn)

        self.railOptionsBtn = QPushButton(self.railFrame)
        self.railOptionsBtn.setObjectName(u"railOptionsBtn")
        self.railOptionsBtn.setMinimumSize(QSize(60, 55))
        self.railOptionsBtn.setMaximumSize(QSize(60, 55))
        self.railOptionsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.railLayout.addWidget(self.railOptionsBtn)

        self.railHistoryBtn = QPushButton(self.railFrame)
        self.railHistoryBtn.setObjectName(u"railHistoryBtn")
        self.railHistoryBtn.setMinimumSize(QSize(60, 55))
        self.railHistoryBtn.setMaximumSize(QSize(60, 55))
        self.railHistoryBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.railLayout.addWidget(self.railHistoryBtn)

        self.railSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.railLayout.addItem(self.railSpacer)

        self.railHelpBtn = QPushButton(self.railFrame)
        self.railHelpBtn.setObjectName(u"railHelpBtn")
        self.railHelpBtn.setMinimumSize(QSize(60, 55))
        self.railHelpBtn.setMaximumSize(QSize(60, 55))
        self.railHelpBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.railLayout.addWidget(self.railHelpBtn)

        self.railSettingsBtn = QPushButton(self.railFrame)
        self.railSettingsBtn.setObjectName(u"railSettingsBtn")
        self.railSettingsBtn.setMinimumSize(QSize(60, 55))
        self.railSettingsBtn.setMaximumSize(QSize(60, 55))
        self.railSettingsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.railLayout.addWidget(self.railSettingsBtn)


        self.studioLayout.addWidget(self.railFrame)

        self.leftScrollArea = QScrollArea(self.studioContainer)
        self.leftScrollArea.setObjectName(u"leftScrollArea")
        self.leftScrollArea.setMaximumSize(QSize(420, 16777215))
        self.leftScrollArea.setVisible(False)
        self.leftScrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.leftScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.leftScrollArea.setWidgetResizable(True)
        self.leftContentWidget = QWidget()
        self.leftContentWidget.setObjectName(u"leftContentWidget")
        self.optionsLayout = QVBoxLayout(self.leftContentWidget)
        self.optionsLayout.setSpacing(8)
        self.optionsLayout.setObjectName(u"optionsLayout")
        self.optionsLayout.setContentsMargins(12, -1, 12, -1)
        self.capModel = QLabel(self.leftContentWidget)
        self.capModel.setObjectName(u"capModel")

        self.optionsLayout.addWidget(self.capModel)

        self.modelCurrentLabel = QLabel(self.leftContentWidget)
        self.modelCurrentLabel.setObjectName(u"modelCurrentLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modelCurrentLabel.sizePolicy().hasHeightForWidth())
        self.modelCurrentLabel.setSizePolicy(sizePolicy)

        self.optionsLayout.addWidget(self.modelCurrentLabel)

        self.lmModelSelectLayout = QVBoxLayout()
        self.lmModelSelectLayout.setSpacing(4)
        self.lmModelSelectLayout.setObjectName(u"lmModelSelectLayout")
        self.lmModelSelectLabel = QLabel(self.leftContentWidget)
        self.lmModelSelectLabel.setObjectName(u"lmModelSelectLabel")

        self.lmModelSelectLayout.addWidget(self.lmModelSelectLabel)

        self.lmModelCombo = QComboBox(self.leftContentWidget)
        self.lmModelCombo.setObjectName(u"lmModelCombo")
        self.lmModelCombo.setMinimumSize(QSize(0, 34))

        self.lmModelSelectLayout.addWidget(self.lmModelCombo)


        self.optionsLayout.addLayout(self.lmModelSelectLayout)

        self.capResolution = QLabel(self.leftContentWidget)
        self.capResolution.setObjectName(u"capResolution")

        self.optionsLayout.addWidget(self.capResolution)

        self.presetsButtonLayout = QHBoxLayout()
        self.presetsButtonLayout.setSpacing(8)
        self.presetsButtonLayout.setObjectName(u"presetsButtonLayout")
        self.preset_1024x1024 = QPushButton(self.leftContentWidget)
        self.preset_1024x1024.setObjectName(u"preset_1024x1024")
        self.preset_1024x1024.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.preset_1024x1024.setMinimumSize(QSize(0, 60))
        self.preset_1024x1024.setMaximumSize(QSize(220, 16777215))

        self.presetsButtonLayout.addWidget(self.preset_1024x1024)

        self.preset_896x1152 = QPushButton(self.leftContentWidget)
        self.preset_896x1152.setObjectName(u"preset_896x1152")
        self.preset_896x1152.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.preset_896x1152.setMinimumSize(QSize(0, 60))
        self.preset_896x1152.setMaximumSize(QSize(220, 16777215))

        self.presetsButtonLayout.addWidget(self.preset_896x1152)

        self.preset_1152x896 = QPushButton(self.leftContentWidget)
        self.preset_1152x896.setObjectName(u"preset_1152x896")
        self.preset_1152x896.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.preset_1152x896.setMinimumSize(QSize(0, 60))
        self.preset_1152x896.setMaximumSize(QSize(220, 16777215))

        self.presetsButtonLayout.addWidget(self.preset_1152x896)


        self.optionsLayout.addLayout(self.presetsButtonLayout)

        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.setSpacing(8)
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.widthLabel = QLabel(self.leftContentWidget)
        self.widthLabel.setObjectName(u"widthLabel")
        self.widthLabel.setMinimumSize(QSize(64, 0))

        self.hboxLayout.addWidget(self.widthLabel)

        self.widthSpinBox = QSpinBox(self.leftContentWidget)
        self.widthSpinBox.setObjectName(u"widthSpinBox")
        self.widthSpinBox.setMinimumSize(QSize(72, 0))

        self.hboxLayout.addWidget(self.widthSpinBox)

        self.heightLabel = QLabel(self.leftContentWidget)
        self.heightLabel.setObjectName(u"heightLabel")
        self.heightLabel.setMinimumSize(QSize(64, 0))

        self.hboxLayout.addWidget(self.heightLabel)

        self.heightSpinBox = QSpinBox(self.leftContentWidget)
        self.heightSpinBox.setObjectName(u"heightSpinBox")
        self.heightSpinBox.setMinimumSize(QSize(72, 0))

        self.hboxLayout.addWidget(self.heightSpinBox)


        self.optionsLayout.addLayout(self.hboxLayout)

        self.capSampling = QLabel(self.leftContentWidget)
        self.capSampling.setObjectName(u"capSampling")

        self.optionsLayout.addWidget(self.capSampling)

        self.hboxLayout1 = QHBoxLayout()
        self.hboxLayout1.setSpacing(8)
        self.hboxLayout1.setObjectName(u"hboxLayout1")
        self.stepsLabelTitle = QLabel(self.leftContentWidget)
        self.stepsLabelTitle.setObjectName(u"stepsLabelTitle")
        self.stepsLabelTitle.setMinimumSize(QSize(64, 0))

        self.hboxLayout1.addWidget(self.stepsLabelTitle)

        self.stepsSlider = QSlider(self.leftContentWidget)
        self.stepsSlider.setObjectName(u"stepsSlider")
        self.stepsSlider.setMinimum(1)
        self.stepsSlider.setMaximum(50)
        self.stepsSlider.setValue(24)
        self.stepsSlider.setOrientation(Qt.Orientation.Horizontal)

        self.hboxLayout1.addWidget(self.stepsSlider)

        self.stepsValueLabel = QLabel(self.leftContentWidget)
        self.stepsValueLabel.setObjectName(u"stepsValueLabel")

        self.hboxLayout1.addWidget(self.stepsValueLabel)


        self.optionsLayout.addLayout(self.hboxLayout1)

        self.hboxLayout2 = QHBoxLayout()
        self.hboxLayout2.setSpacing(8)
        self.hboxLayout2.setObjectName(u"hboxLayout2")
        self.cfgLabelTitle = QLabel(self.leftContentWidget)
        self.cfgLabelTitle.setObjectName(u"cfgLabelTitle")
        self.cfgLabelTitle.setMinimumSize(QSize(64, 0))

        self.hboxLayout2.addWidget(self.cfgLabelTitle)

        self.cfgSlider = QSlider(self.leftContentWidget)
        self.cfgSlider.setObjectName(u"cfgSlider")
        self.cfgSlider.setMinimum(10)
        self.cfgSlider.setMaximum(150)
        self.cfgSlider.setValue(35)
        self.cfgSlider.setOrientation(Qt.Orientation.Horizontal)

        self.hboxLayout2.addWidget(self.cfgSlider)

        self.cfgValueLabel = QLabel(self.leftContentWidget)
        self.cfgValueLabel.setObjectName(u"cfgValueLabel")

        self.hboxLayout2.addWidget(self.cfgValueLabel)


        self.optionsLayout.addLayout(self.hboxLayout2)

        self.hboxLayout3 = QHBoxLayout()
        self.hboxLayout3.setSpacing(8)
        self.hboxLayout3.setObjectName(u"hboxLayout3")
        self.seedTitleLabel = QLabel(self.leftContentWidget)
        self.seedTitleLabel.setObjectName(u"seedTitleLabel")
        self.seedTitleLabel.setMinimumSize(QSize(64, 0))

        self.hboxLayout3.addWidget(self.seedTitleLabel)

        self.seedSpinBox = QSpinBox(self.leftContentWidget)
        self.seedSpinBox.setObjectName(u"seedSpinBox")
        self.seedSpinBox.setMinimumSize(QSize(120, 28))
        self.seedSpinBox.setMaximumSize(QSize(110, 16777215))

        self.hboxLayout3.addWidget(self.seedSpinBox)

        self.randomSeedButton = QPushButton(self.leftContentWidget)
        self.randomSeedButton.setObjectName(u"randomSeedButton")
        self.randomSeedButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.hboxLayout3.addWidget(self.randomSeedButton)

        self.lockSeedButton = QPushButton(self.leftContentWidget)
        self.lockSeedButton.setObjectName(u"lockSeedButton")
        self.lockSeedButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.lockSeedButton.setCheckable(True)

        self.hboxLayout3.addWidget(self.lockSeedButton)


        self.optionsLayout.addLayout(self.hboxLayout3)

        self.hboxLayout4 = QHBoxLayout()
        self.hboxLayout4.setSpacing(8)
        self.hboxLayout4.setObjectName(u"hboxLayout4")
        self.samplerLabel = QLabel(self.leftContentWidget)
        self.samplerLabel.setObjectName(u"samplerLabel")
        self.samplerLabel.setMinimumSize(QSize(64, 0))

        self.hboxLayout4.addWidget(self.samplerLabel)

        self.samplerComboBox = QComboBox(self.leftContentWidget)
        self.samplerComboBox.setObjectName(u"samplerComboBox")

        self.hboxLayout4.addWidget(self.samplerComboBox)


        self.optionsLayout.addLayout(self.hboxLayout4)

        self.hboxLayout5 = QHBoxLayout()
        self.hboxLayout5.setSpacing(8)
        self.hboxLayout5.setObjectName(u"hboxLayout5")
        self.schedulerLabel = QLabel(self.leftContentWidget)
        self.schedulerLabel.setObjectName(u"schedulerLabel")
        self.schedulerLabel.setMinimumSize(QSize(64, 0))

        self.hboxLayout5.addWidget(self.schedulerLabel)

        self.schedulerComboBox = QComboBox(self.leftContentWidget)
        self.schedulerComboBox.setObjectName(u"schedulerComboBox")

        self.hboxLayout5.addWidget(self.schedulerComboBox)


        self.optionsLayout.addLayout(self.hboxLayout5)

        self.hboxLayout6 = QHBoxLayout()
        self.hboxLayout6.setSpacing(8)
        self.hboxLayout6.setObjectName(u"hboxLayout6")
        self.denoiseLabel = QLabel(self.leftContentWidget)
        self.denoiseLabel.setObjectName(u"denoiseLabel")
        self.denoiseLabel.setMinimumSize(QSize(64, 0))

        self.hboxLayout6.addWidget(self.denoiseLabel)

        self.denoiseSpinBox = QDoubleSpinBox(self.leftContentWidget)
        self.denoiseSpinBox.setObjectName(u"denoiseSpinBox")

        self.hboxLayout6.addWidget(self.denoiseSpinBox)


        self.optionsLayout.addLayout(self.hboxLayout6)

        self.capPrompt = QLabel(self.leftContentWidget)
        self.capPrompt.setObjectName(u"capPrompt")

        self.optionsLayout.addWidget(self.capPrompt)

        self.negativePromptFrame = QFrame(self.leftContentWidget)
        self.negativePromptFrame.setObjectName(u"negativePromptFrame")
        self.negativePromptFrame.setVisible(False)
        sizePolicy.setHeightForWidth(self.negativePromptFrame.sizePolicy().hasHeightForWidth())
        self.negativePromptFrame.setSizePolicy(sizePolicy)
        self.negLayout = QVBoxLayout(self.negativePromptFrame)
        self.negLayout.setSpacing(4)
        self.negLayout.setObjectName(u"negLayout")
        self.negLayout.setContentsMargins(0, 4, 0, 0)
        self.negativePromptEdit = QPlainTextEdit(self.negativePromptFrame)
        self.negativePromptEdit.setObjectName(u"negativePromptEdit")
        self.negativePromptEdit.setMinimumSize(QSize(0, 54))

        self.negLayout.addWidget(self.negativePromptEdit)


        self.optionsLayout.addWidget(self.negativePromptFrame)

        self.enhancePromptButton = QPushButton(self.leftContentWidget)
        self.enhancePromptButton.setObjectName(u"enhancePromptButton")
        self.enhancePromptButton.setMinimumSize(QSize(0, 38))
        self.enhancePromptButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.optionsLayout.addWidget(self.enhancePromptButton)

        self.enhancePromptEdit = QPlainTextEdit(self.leftContentWidget)
        self.enhancePromptEdit.setObjectName(u"enhancePromptEdit")
        self.enhancePromptEdit.setMinimumSize(QSize(0, 68))
        self.enhancePromptEdit.setVisible(False)
        sizePolicy.setHeightForWidth(self.enhancePromptEdit.sizePolicy().hasHeightForWidth())
        self.enhancePromptEdit.setSizePolicy(sizePolicy)

        self.optionsLayout.addWidget(self.enhancePromptEdit)

        self.positivePromptEdit = QPlainTextEdit(self.leftContentWidget)
        self.positivePromptEdit.setObjectName(u"positivePromptEdit")
        self.positivePromptEdit.setMinimumSize(QSize(0, 76))
        self.positivePromptEdit.setVisible(False)
        sizePolicy.setHeightForWidth(self.positivePromptEdit.sizePolicy().hasHeightForWidth())
        self.positivePromptEdit.setSizePolicy(sizePolicy)

        self.optionsLayout.addWidget(self.positivePromptEdit)

        self.capFace = QLabel(self.leftContentWidget)
        self.capFace.setObjectName(u"capFace")

        self.optionsLayout.addWidget(self.capFace)

        self.hboxLayout7 = QHBoxLayout()
        self.hboxLayout7.setSpacing(8)
        self.hboxLayout7.setObjectName(u"hboxLayout7")
        self.facedetailerCheckBox = QCheckBox(self.leftContentWidget)
        self.facedetailerCheckBox.setObjectName(u"facedetailerCheckBox")
        self.facedetailerCheckBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.hboxLayout7.addWidget(self.facedetailerCheckBox)

        self.facedetailerHelpBtn = QPushButton(self.leftContentWidget)
        self.facedetailerHelpBtn.setObjectName(u"facedetailerHelpBtn")
        self.facedetailerHelpBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.facedetailerHelpBtn.setAutoDefault(False)

        self.hboxLayout7.addWidget(self.facedetailerHelpBtn)


        self.optionsLayout.addLayout(self.hboxLayout7)

        self.facedetailerPanel = QFrame(self.leftContentWidget)
        self.facedetailerPanel.setObjectName(u"facedetailerPanel")
        self.facedetailerPanel.setVisible(False)
        sizePolicy.setHeightForWidth(self.facedetailerPanel.sizePolicy().hasHeightForWidth())
        self.facedetailerPanel.setSizePolicy(sizePolicy)
        self.facedetailerPanelVBox = QVBoxLayout(self.facedetailerPanel)
        self.facedetailerPanelVBox.setSpacing(2)
        self.facedetailerPanelVBox.setObjectName(u"facedetailerPanelVBox")
        self.facedetailerPanelVBox.setContentsMargins(4, 4, 4, 4)
        self.fdOptRow = QHBoxLayout()
        self.fdOptRow.setSpacing(6)
        self.fdOptRow.setObjectName(u"fdOptRow")
        self.facedetailerDenoiseLabel = QLabel(self.facedetailerPanel)
        self.facedetailerDenoiseLabel.setObjectName(u"facedetailerDenoiseLabel")
        self.facedetailerDenoiseLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow.addWidget(self.facedetailerDenoiseLabel)

        self.facedetailerDenoiseSlider = QSlider(self.facedetailerPanel)
        self.facedetailerDenoiseSlider.setObjectName(u"facedetailerDenoiseSlider")
        self.facedetailerDenoiseSlider.setMinimum(0)
        self.facedetailerDenoiseSlider.setMaximum(100)
        self.facedetailerDenoiseSlider.setValue(40)
        self.facedetailerDenoiseSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow.addWidget(self.facedetailerDenoiseSlider)

        self.facedetailerDenoiseValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerDenoiseValueLabel.setObjectName(u"facedetailerDenoiseValueLabel")
        self.facedetailerDenoiseValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow.addWidget(self.facedetailerDenoiseValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow)

        self.fdOptRow1 = QHBoxLayout()
        self.fdOptRow1.setSpacing(6)
        self.fdOptRow1.setObjectName(u"fdOptRow1")
        self.facedetailerStepsLabel = QLabel(self.facedetailerPanel)
        self.facedetailerStepsLabel.setObjectName(u"facedetailerStepsLabel")
        self.facedetailerStepsLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow1.addWidget(self.facedetailerStepsLabel)

        self.facedetailerStepsSlider = QSlider(self.facedetailerPanel)
        self.facedetailerStepsSlider.setObjectName(u"facedetailerStepsSlider")
        self.facedetailerStepsSlider.setMinimum(1)
        self.facedetailerStepsSlider.setMaximum(50)
        self.facedetailerStepsSlider.setValue(20)
        self.facedetailerStepsSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow1.addWidget(self.facedetailerStepsSlider)

        self.facedetailerStepsValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerStepsValueLabel.setObjectName(u"facedetailerStepsValueLabel")
        self.facedetailerStepsValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow1.addWidget(self.facedetailerStepsValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow1)

        self.fdOptRow2 = QHBoxLayout()
        self.fdOptRow2.setSpacing(6)
        self.fdOptRow2.setObjectName(u"fdOptRow2")
        self.facedetailerCfgLabel = QLabel(self.facedetailerPanel)
        self.facedetailerCfgLabel.setObjectName(u"facedetailerCfgLabel")
        self.facedetailerCfgLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow2.addWidget(self.facedetailerCfgLabel)

        self.facedetailerCfgSlider = QSlider(self.facedetailerPanel)
        self.facedetailerCfgSlider.setObjectName(u"facedetailerCfgSlider")
        self.facedetailerCfgSlider.setMinimum(0)
        self.facedetailerCfgSlider.setMaximum(200)
        self.facedetailerCfgSlider.setValue(40)
        self.facedetailerCfgSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow2.addWidget(self.facedetailerCfgSlider)

        self.facedetailerCfgValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerCfgValueLabel.setObjectName(u"facedetailerCfgValueLabel")
        self.facedetailerCfgValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow2.addWidget(self.facedetailerCfgValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow2)

        self.fdOptRow3 = QHBoxLayout()
        self.fdOptRow3.setSpacing(6)
        self.fdOptRow3.setObjectName(u"fdOptRow3")
        self.facedetailerFeatherLabel = QLabel(self.facedetailerPanel)
        self.facedetailerFeatherLabel.setObjectName(u"facedetailerFeatherLabel")
        self.facedetailerFeatherLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow3.addWidget(self.facedetailerFeatherLabel)

        self.facedetailerFeatherSlider = QSlider(self.facedetailerPanel)
        self.facedetailerFeatherSlider.setObjectName(u"facedetailerFeatherSlider")
        self.facedetailerFeatherSlider.setMinimum(0)
        self.facedetailerFeatherSlider.setMaximum(20)
        self.facedetailerFeatherSlider.setValue(5)
        self.facedetailerFeatherSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow3.addWidget(self.facedetailerFeatherSlider)

        self.facedetailerFeatherValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerFeatherValueLabel.setObjectName(u"facedetailerFeatherValueLabel")
        self.facedetailerFeatherValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow3.addWidget(self.facedetailerFeatherValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow3)

        self.fdOptRow4 = QHBoxLayout()
        self.fdOptRow4.setSpacing(6)
        self.fdOptRow4.setObjectName(u"fdOptRow4")
        self.facedetailerDropSizeLabel = QLabel(self.facedetailerPanel)
        self.facedetailerDropSizeLabel.setObjectName(u"facedetailerDropSizeLabel")
        self.facedetailerDropSizeLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow4.addWidget(self.facedetailerDropSizeLabel)

        self.facedetailerDropSizeSlider = QSlider(self.facedetailerPanel)
        self.facedetailerDropSizeSlider.setObjectName(u"facedetailerDropSizeSlider")
        self.facedetailerDropSizeSlider.setMinimum(1)
        self.facedetailerDropSizeSlider.setMaximum(100)
        self.facedetailerDropSizeSlider.setValue(10)
        self.facedetailerDropSizeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow4.addWidget(self.facedetailerDropSizeSlider)

        self.facedetailerDropSizeValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerDropSizeValueLabel.setObjectName(u"facedetailerDropSizeValueLabel")
        self.facedetailerDropSizeValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow4.addWidget(self.facedetailerDropSizeValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow4)

        self.fdOptRow5 = QHBoxLayout()
        self.fdOptRow5.setSpacing(6)
        self.fdOptRow5.setObjectName(u"fdOptRow5")
        self.facedetailerGuideSizeLabel = QLabel(self.facedetailerPanel)
        self.facedetailerGuideSizeLabel.setObjectName(u"facedetailerGuideSizeLabel")
        self.facedetailerGuideSizeLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow5.addWidget(self.facedetailerGuideSizeLabel)

        self.facedetailerGuideSizeSlider = QSlider(self.facedetailerPanel)
        self.facedetailerGuideSizeSlider.setObjectName(u"facedetailerGuideSizeSlider")
        self.facedetailerGuideSizeSlider.setMinimum(1)
        self.facedetailerGuideSizeSlider.setMaximum(16)
        self.facedetailerGuideSizeSlider.setValue(4)
        self.facedetailerGuideSizeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow5.addWidget(self.facedetailerGuideSizeSlider)

        self.facedetailerGuideSizeValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerGuideSizeValueLabel.setObjectName(u"facedetailerGuideSizeValueLabel")
        self.facedetailerGuideSizeValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow5.addWidget(self.facedetailerGuideSizeValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow5)

        self.fdOptRow6 = QHBoxLayout()
        self.fdOptRow6.setSpacing(6)
        self.fdOptRow6.setObjectName(u"fdOptRow6")
        self.facedetailerMaxSizeLabel = QLabel(self.facedetailerPanel)
        self.facedetailerMaxSizeLabel.setObjectName(u"facedetailerMaxSizeLabel")
        self.facedetailerMaxSizeLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow6.addWidget(self.facedetailerMaxSizeLabel)

        self.facedetailerMaxSizeSlider = QSlider(self.facedetailerPanel)
        self.facedetailerMaxSizeSlider.setObjectName(u"facedetailerMaxSizeSlider")
        self.facedetailerMaxSizeSlider.setMinimum(2)
        self.facedetailerMaxSizeSlider.setMaximum(32)
        self.facedetailerMaxSizeSlider.setValue(12)
        self.facedetailerMaxSizeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow6.addWidget(self.facedetailerMaxSizeSlider)

        self.facedetailerMaxSizeValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerMaxSizeValueLabel.setObjectName(u"facedetailerMaxSizeValueLabel")
        self.facedetailerMaxSizeValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow6.addWidget(self.facedetailerMaxSizeValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow6)

        self.fdOptRow7 = QHBoxLayout()
        self.fdOptRow7.setSpacing(6)
        self.fdOptRow7.setObjectName(u"fdOptRow7")
        self.facedetailerCycleLabel = QLabel(self.facedetailerPanel)
        self.facedetailerCycleLabel.setObjectName(u"facedetailerCycleLabel")
        self.facedetailerCycleLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow7.addWidget(self.facedetailerCycleLabel)

        self.facedetailerCycleSlider = QSlider(self.facedetailerPanel)
        self.facedetailerCycleSlider.setObjectName(u"facedetailerCycleSlider")
        self.facedetailerCycleSlider.setMinimum(1)
        self.facedetailerCycleSlider.setMaximum(10)
        self.facedetailerCycleSlider.setValue(1)
        self.facedetailerCycleSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow7.addWidget(self.facedetailerCycleSlider)

        self.facedetailerCycleValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerCycleValueLabel.setObjectName(u"facedetailerCycleValueLabel")
        self.facedetailerCycleValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow7.addWidget(self.facedetailerCycleValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow7)

        self.fdOptRow8 = QHBoxLayout()
        self.fdOptRow8.setSpacing(6)
        self.fdOptRow8.setObjectName(u"fdOptRow8")
        self.facedetailerBboxThresholdLabel = QLabel(self.facedetailerPanel)
        self.facedetailerBboxThresholdLabel.setObjectName(u"facedetailerBboxThresholdLabel")
        self.facedetailerBboxThresholdLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow8.addWidget(self.facedetailerBboxThresholdLabel)

        self.facedetailerBboxThresholdSlider = QSlider(self.facedetailerPanel)
        self.facedetailerBboxThresholdSlider.setObjectName(u"facedetailerBboxThresholdSlider")
        self.facedetailerBboxThresholdSlider.setMinimum(10)
        self.facedetailerBboxThresholdSlider.setMaximum(100)
        self.facedetailerBboxThresholdSlider.setValue(50)
        self.facedetailerBboxThresholdSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow8.addWidget(self.facedetailerBboxThresholdSlider)

        self.facedetailerBboxThresholdValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerBboxThresholdValueLabel.setObjectName(u"facedetailerBboxThresholdValueLabel")
        self.facedetailerBboxThresholdValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow8.addWidget(self.facedetailerBboxThresholdValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow8)

        self.fdOptRow9 = QHBoxLayout()
        self.fdOptRow9.setSpacing(6)
        self.fdOptRow9.setObjectName(u"fdOptRow9")
        self.facedetailerBboxDilationLabel = QLabel(self.facedetailerPanel)
        self.facedetailerBboxDilationLabel.setObjectName(u"facedetailerBboxDilationLabel")
        self.facedetailerBboxDilationLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow9.addWidget(self.facedetailerBboxDilationLabel)

        self.facedetailerBboxDilationSlider = QSlider(self.facedetailerPanel)
        self.facedetailerBboxDilationSlider.setObjectName(u"facedetailerBboxDilationSlider")
        self.facedetailerBboxDilationSlider.setMinimum(-20)
        self.facedetailerBboxDilationSlider.setMaximum(100)
        self.facedetailerBboxDilationSlider.setValue(10)
        self.facedetailerBboxDilationSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow9.addWidget(self.facedetailerBboxDilationSlider)

        self.facedetailerBboxDilationValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerBboxDilationValueLabel.setObjectName(u"facedetailerBboxDilationValueLabel")
        self.facedetailerBboxDilationValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow9.addWidget(self.facedetailerBboxDilationValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow9)

        self.fdOptRow10 = QHBoxLayout()
        self.fdOptRow10.setSpacing(6)
        self.fdOptRow10.setObjectName(u"fdOptRow10")
        self.facedetailerBboxCropFactorLabel = QLabel(self.facedetailerPanel)
        self.facedetailerBboxCropFactorLabel.setObjectName(u"facedetailerBboxCropFactorLabel")
        self.facedetailerBboxCropFactorLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow10.addWidget(self.facedetailerBboxCropFactorLabel)

        self.facedetailerBboxCropFactorSlider = QSlider(self.facedetailerPanel)
        self.facedetailerBboxCropFactorSlider.setObjectName(u"facedetailerBboxCropFactorSlider")
        self.facedetailerBboxCropFactorSlider.setMinimum(100)
        self.facedetailerBboxCropFactorSlider.setMaximum(500)
        self.facedetailerBboxCropFactorSlider.setValue(150)
        self.facedetailerBboxCropFactorSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow10.addWidget(self.facedetailerBboxCropFactorSlider)

        self.facedetailerBboxCropFactorValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerBboxCropFactorValueLabel.setObjectName(u"facedetailerBboxCropFactorValueLabel")
        self.facedetailerBboxCropFactorValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow10.addWidget(self.facedetailerBboxCropFactorValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow10)

        self.fdOptRow11 = QHBoxLayout()
        self.fdOptRow11.setSpacing(6)
        self.fdOptRow11.setObjectName(u"fdOptRow11")
        self.facedetailerSamThresholdLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamThresholdLabel.setObjectName(u"facedetailerSamThresholdLabel")
        self.facedetailerSamThresholdLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow11.addWidget(self.facedetailerSamThresholdLabel)

        self.facedetailerSamThresholdSlider = QSlider(self.facedetailerPanel)
        self.facedetailerSamThresholdSlider.setObjectName(u"facedetailerSamThresholdSlider")
        self.facedetailerSamThresholdSlider.setMinimum(10)
        self.facedetailerSamThresholdSlider.setMaximum(100)
        self.facedetailerSamThresholdSlider.setValue(93)
        self.facedetailerSamThresholdSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow11.addWidget(self.facedetailerSamThresholdSlider)

        self.facedetailerSamThresholdValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamThresholdValueLabel.setObjectName(u"facedetailerSamThresholdValueLabel")
        self.facedetailerSamThresholdValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow11.addWidget(self.facedetailerSamThresholdValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow11)

        self.fdOptRow12 = QHBoxLayout()
        self.fdOptRow12.setSpacing(6)
        self.fdOptRow12.setObjectName(u"fdOptRow12")
        self.facedetailerSamDilationLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamDilationLabel.setObjectName(u"facedetailerSamDilationLabel")
        self.facedetailerSamDilationLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow12.addWidget(self.facedetailerSamDilationLabel)

        self.facedetailerSamDilationSlider = QSlider(self.facedetailerPanel)
        self.facedetailerSamDilationSlider.setObjectName(u"facedetailerSamDilationSlider")
        self.facedetailerSamDilationSlider.setMinimum(0)
        self.facedetailerSamDilationSlider.setMaximum(100)
        self.facedetailerSamDilationSlider.setValue(0)
        self.facedetailerSamDilationSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow12.addWidget(self.facedetailerSamDilationSlider)

        self.facedetailerSamDilationValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamDilationValueLabel.setObjectName(u"facedetailerSamDilationValueLabel")
        self.facedetailerSamDilationValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow12.addWidget(self.facedetailerSamDilationValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow12)

        self.fdOptRow13 = QHBoxLayout()
        self.fdOptRow13.setSpacing(6)
        self.fdOptRow13.setObjectName(u"fdOptRow13")
        self.facedetailerSamBboxExpansionLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamBboxExpansionLabel.setObjectName(u"facedetailerSamBboxExpansionLabel")
        self.facedetailerSamBboxExpansionLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow13.addWidget(self.facedetailerSamBboxExpansionLabel)

        self.facedetailerSamBboxExpansionSlider = QSlider(self.facedetailerPanel)
        self.facedetailerSamBboxExpansionSlider.setObjectName(u"facedetailerSamBboxExpansionSlider")
        self.facedetailerSamBboxExpansionSlider.setMinimum(0)
        self.facedetailerSamBboxExpansionSlider.setMaximum(100)
        self.facedetailerSamBboxExpansionSlider.setValue(0)
        self.facedetailerSamBboxExpansionSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow13.addWidget(self.facedetailerSamBboxExpansionSlider)

        self.facedetailerSamBboxExpansionValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamBboxExpansionValueLabel.setObjectName(u"facedetailerSamBboxExpansionValueLabel")
        self.facedetailerSamBboxExpansionValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow13.addWidget(self.facedetailerSamBboxExpansionValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow13)

        self.fdOptRow14 = QHBoxLayout()
        self.fdOptRow14.setSpacing(6)
        self.fdOptRow14.setObjectName(u"fdOptRow14")
        self.facedetailerSamMaskHintThresholdLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamMaskHintThresholdLabel.setObjectName(u"facedetailerSamMaskHintThresholdLabel")
        self.facedetailerSamMaskHintThresholdLabel.setMinimumSize(QSize(64, 0))

        self.fdOptRow14.addWidget(self.facedetailerSamMaskHintThresholdLabel)

        self.facedetailerSamMaskHintThresholdSlider = QSlider(self.facedetailerPanel)
        self.facedetailerSamMaskHintThresholdSlider.setObjectName(u"facedetailerSamMaskHintThresholdSlider")
        self.facedetailerSamMaskHintThresholdSlider.setMinimum(10)
        self.facedetailerSamMaskHintThresholdSlider.setMaximum(100)
        self.facedetailerSamMaskHintThresholdSlider.setValue(70)
        self.facedetailerSamMaskHintThresholdSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fdOptRow14.addWidget(self.facedetailerSamMaskHintThresholdSlider)

        self.facedetailerSamMaskHintThresholdValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamMaskHintThresholdValueLabel.setObjectName(u"facedetailerSamMaskHintThresholdValueLabel")
        self.facedetailerSamMaskHintThresholdValueLabel.setMinimumSize(QSize(46, 0))

        self.fdOptRow14.addWidget(self.facedetailerSamMaskHintThresholdValueLabel)


        self.facedetailerPanelVBox.addLayout(self.fdOptRow14)


        self.optionsLayout.addWidget(self.facedetailerPanel)

        self.openOutputFolderButton = QPushButton(self.leftContentWidget)
        self.openOutputFolderButton.setObjectName(u"openOutputFolderButton")
        self.openOutputFolderButton.setVisible(False)
        self.openOutputFolderButton.setMinimumSize(QSize(0, 34))
        self.openOutputFolderButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.optionsLayout.addWidget(self.openOutputFolderButton)

        self.leftScrollArea.setWidget(self.leftContentWidget)

        self.studioLayout.addWidget(self.leftScrollArea)

        self.chatFrame = QFrame(self.studioContainer)
        self.chatFrame.setObjectName(u"chatFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.chatFrame.sizePolicy().hasHeightForWidth())
        self.chatFrame.setSizePolicy(sizePolicy1)
        self.chatFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.chatMainLayout = QVBoxLayout(self.chatFrame)
        self.chatMainLayout.setSpacing(8)
        self.chatMainLayout.setObjectName(u"chatMainLayout")
        self.chatScrollArea = QScrollArea(self.chatFrame)
        self.chatScrollArea.setObjectName(u"chatScrollArea")
        self.chatScrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.chatScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.chatScrollArea.setWidgetResizable(True)
        self.chatContentWidget = QWidget()
        self.chatContentWidget.setObjectName(u"chatContentWidget")
        self.chatContentWidget.setGeometry(QRect(0, 0, 994, 534))
        self.chatLayout = QVBoxLayout(self.chatContentWidget)
        self.chatLayout.setSpacing(16)
        self.chatLayout.setObjectName(u"chatLayout")
        self.chatLayout.setContentsMargins(18, 18, 18, 18)
        self.chatSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.chatLayout.addItem(self.chatSpacer)

        self.chatScrollArea.setWidget(self.chatContentWidget)

        self.chatMainLayout.addWidget(self.chatScrollArea)


        self.studioLayout.addWidget(self.chatFrame)


        self.gridLayout_3.addWidget(self.studioContainer, 1, 0, 1, 1)

        self.inputFrame = QFrame(self.centralWidget)
        self.inputFrame.setObjectName(u"inputFrame")
        self.inputFrame.setMinimumSize(QSize(0, 58))
        self.inputFrame.setMaximumSize(QSize(16777215, 58))
        self.inputFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.inputRowLayout = QHBoxLayout(self.inputFrame)
        self.inputRowLayout.setSpacing(10)
        self.inputRowLayout.setObjectName(u"inputRowLayout")
        self.inputRowLayout.setContentsMargins(10, 10, 10, 10)
        self.comfyModelCombo = QComboBox(self.inputFrame)
        self.comfyModelCombo.setObjectName(u"comfyModelCombo")
        self.comfyModelCombo.setMinimumSize(QSize(0, 34))

        self.inputRowLayout.addWidget(self.comfyModelCombo)

        self.chatInputEdit = QPlainTextEdit(self.inputFrame)
        self.chatInputEdit.setObjectName(u"chatInputEdit")
        self.chatInputEdit.setMinimumSize(QSize(0, 34))
        self.chatInputEdit.setMaximumSize(QSize(16777215, 34))

        self.inputRowLayout.addWidget(self.chatInputEdit)

        self.sendBtn = QPushButton(self.inputFrame)
        self.sendBtn.setObjectName(u"sendBtn")
        self.sendBtn.setMinimumSize(QSize(34, 34))
        self.sendBtn.setMaximumSize(QSize(34, 34))
        self.sendBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.inputRowLayout.addWidget(self.sendBtn)

        self.inputRowLayout.setStretch(0, 1)
        self.inputRowLayout.setStretch(1, 3)

        self.gridLayout_3.addWidget(self.inputFrame, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ComfyCraft AI Easy Studio", None))
        self.appTitle.setText(QCoreApplication.translate("MainWindow", u"\u2728 ComfyCraft AI", None))
#if QT_CONFIG(tooltip)
        self.newChatBtn.setToolTip(QCoreApplication.translate("MainWindow", u"\uc0c8 \ub300\ud654\ub97c \uc2dc\uc791\ud569\ub2c8\ub2e4", None))
#endif // QT_CONFIG(tooltip)
        self.newChatBtn.setText(QCoreApplication.translate("MainWindow", u"\uff0b \uc0c8 \ub300\ud654", None))
#if QT_CONFIG(tooltip)
        self.comfyStatusBtn.setToolTip(QCoreApplication.translate("MainWindow", u"\ud074\ub9ad\ud558\uc5ec ComfyUI \uc11c\ubc84 \uc8fc\uc18c \ubc0f \ubaa8\ub378 \ud3f4\ub354\ub97c \uc124\uc815\ud569\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.comfyStatusBtn.setText(QCoreApplication.translate("MainWindow", u"\U0001f3a8 ComfyUI \U000025cf \U0000d655\U0000c778 \U0000c911...", None))
#if QT_CONFIG(tooltip)
        self.lmStatusBtn.setToolTip(QCoreApplication.translate("MainWindow", u"\ud074\ub9ad\ud558\uc5ec LM Studio \uc11c\ubc84 \uc8fc\uc18c\ub97c \uc124\uc815\ud569\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.lmStatusBtn.setText(QCoreApplication.translate("MainWindow", u"\U0001f4ac LM Studio \U000025cf \U0000d655\U0000c778 \U0000c911...", None))
#if QT_CONFIG(tooltip)
        self.themeComboBox.setToolTip(QCoreApplication.translate("MainWindow", u"UI \ud14c\ub9c8\ub97c \ubcc0\uacbd\ud569\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.railHomeBtn.setToolTip(QCoreApplication.translate("MainWindow", u"\uba54\uc778 \ucc44\ud305 \ud654\uba74\uc73c\ub85c", None))
#endif // QT_CONFIG(tooltip)
        self.railHomeBtn.setText(QCoreApplication.translate("MainWindow", u"\ud648", None))
#if QT_CONFIG(accessibility)
        self.railHomeBtn.setAccessibleName(QCoreApplication.translate("MainWindow", u"\ud648 \u2014 \uba54\uc778 \ucc44\ud305 \ud654\uba74\uc73c\ub85c", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(tooltip)
        self.railOptionsBtn.setToolTip(QCoreApplication.translate("MainWindow", u"\uc0dd\uc131 \uc635\uc158 \ud328\ub110", None))
#endif // QT_CONFIG(tooltip)
        self.railOptionsBtn.setText(QCoreApplication.translate("MainWindow", u"\uc635\uc158", None))
#if QT_CONFIG(accessibility)
        self.railOptionsBtn.setAccessibleName(QCoreApplication.translate("MainWindow", u"\uc0dd\uc131 \uc635\uc158 \u2014 \uc635\uc158 \ud328\ub110 \ud3bc\uce68/\uc811\ud798", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(tooltip)
        self.railHistoryBtn.setToolTip(QCoreApplication.translate("MainWindow", u"\ub300\ud654 \uc774\ub825", None))
#endif // QT_CONFIG(tooltip)
        self.railHistoryBtn.setText(QCoreApplication.translate("MainWindow", u"\uc774\ub825", None))
#if QT_CONFIG(tooltip)
        self.railHelpBtn.setToolTip(QCoreApplication.translate("MainWindow", u"\ub3c4\uc6c0\ub9d0", None))
#endif // QT_CONFIG(tooltip)
        self.railHelpBtn.setText(QCoreApplication.translate("MainWindow", u"?", None))
#if QT_CONFIG(tooltip)
        self.railSettingsBtn.setToolTip(QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
#endif // QT_CONFIG(tooltip)
        self.railSettingsBtn.setText(QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
        self.capModel.setText(QCoreApplication.translate("MainWindow", u"\ubaa8\ub378", None))
        self.modelCurrentLabel.setText(QCoreApplication.translate("MainWindow", u"\ud604\uc7ac \ubaa8\ub378: -", None))
        self.lmModelSelectLabel.setText(QCoreApplication.translate("MainWindow", u"\uc5b8\uc5b4 \ubaa8\ub378 (LM Studio AI)", None))
#if QT_CONFIG(tooltip)
        self.lmModelCombo.setToolTip(QCoreApplication.translate("MainWindow", u"\ud504\ub86c\ud504\ud2b8 \ubc88\uc5ed \ubc0f \ud655\uc7a5\uc5d0 \uc0ac\uc6a9\ud560 LM Studio \uc5b8\uc5b4 \ubaa8\ub378\uc744 \uc120\ud0dd\ud569\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.capResolution.setText(QCoreApplication.translate("MainWindow", u"\ud574\uc0c1\ub3c4", None))
        self.preset_1024x1024.setText(QCoreApplication.translate("MainWindow", u"\u25a1 \uc815\uc0ac\uac01 (1:1)\n"
"1024\u00d71024", None))
        self.preset_896x1152.setText(QCoreApplication.translate("MainWindow", u"\u25af \uc138\ub85c\ud615 (9:16) \u2605\n"
"896\u00d71152", None))
        self.preset_1152x896.setText(QCoreApplication.translate("MainWindow", u"\u25ad \uc640\uc774\ub4dc (16:9)\n"
"1152\u00d7896", None))
        self.widthLabel.setText(QCoreApplication.translate("MainWindow", u"\uac00\ub85c \ud3ed:", None))
        self.heightLabel.setText(QCoreApplication.translate("MainWindow", u"\uc138\ub85c \ub192\uc774:", None))
        self.capSampling.setText(QCoreApplication.translate("MainWindow", u"\uc0d8\ud50c\ub9c1", None))
        self.stepsLabelTitle.setText(QCoreApplication.translate("MainWindow", u"\uc0d8\ud50c\ub9c1 \uc2a4\ud15d (Steps)", None))
        self.stepsValueLabel.setText(QCoreApplication.translate("MainWindow", u"24", None))
        self.cfgLabelTitle.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub86c\ud504\ud2b8 \ucda9\uc2e4\ub3c4 (CFG)", None))
        self.cfgValueLabel.setText(QCoreApplication.translate("MainWindow", u"3.5", None))
        self.seedTitleLabel.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\ub4dc \ubc88\ud638:", None))
        self.randomSeedButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f3b2 \U0000b79c\U0000b364", None))
        self.lockSeedButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f513 \U0000ace0\U0000c815 \U0000c548\U0000d568", None))
        self.samplerLabel.setText(QCoreApplication.translate("MainWindow", u"\uc0d8\ud50c\ub7ec", None))
        self.schedulerLabel.setText(QCoreApplication.translate("MainWindow", u"\uc2a4\ucf00\uc904\ub7ec", None))
        self.denoiseLabel.setText(QCoreApplication.translate("MainWindow", u"\ub514\ub178\uc774\uc988", None))
        self.capPrompt.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub86c\ud504\ud2b8", None))
        self.negativePromptEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\ud488\uc9c8 \uc800\ud558 \ubc29\uc9c0\uc6a9 \ubd80\uc815\uc5b4 (SDXL \ub4f1 \uc804\uc6a9)", None))
        self.enhancePromptButton.setText(QCoreApplication.translate("MainWindow", u"\u2728 AI \ud504\ub86c\ud504\ud2b8 \ub9c8\ubc95\uc0ac\ub85c \uc601\ubb38 \ud655\uc7a5 \uc0dd\uc131", None))
        self.enhancePromptEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"AI \ub9c8\ubc95\uc0ac\ub97c \uc2e4\ud589\ud558\uba74 \uc601\ubb38 \ucd5c\uc801\ud654 \ud504\ub86c\ud504\ud2b8\uac00 \uc0dd\uc131\ub418\uba70, \ud544\uc694\uc2dc \uc5ec\uae30\uc11c \uc9c1\uc811 \uc218\uc815\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.", None))
        self.positivePromptEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\ub9cc\ub4e4\uace0 \uc2f6\uc740 \uc774\ubbf8\uc9c0\ub97c \uc790\uc5f0\uc2a4\ub7ec\uc6b4 \ud55c\uad6d\uc5b4\ub85c \uc801\uc5b4\ubcf4\uc138\uc694. (\uc608: \ube44 \ub0b4\ub9ac\ub294 \ub124\uc628\uc0ac\uc778 \ub3c4\uc2dc\uc758 \uc740\ubc1c \uc548\ub4dc\ub85c\uc774\ub4dc \uc18c\ub140, \uc601\ud654 \uac19\uc740 \uc870\uba85)", None))
        self.capFace.setText(QCoreApplication.translate("MainWindow", u"FaceDetailer", None))
#if QT_CONFIG(tooltip)
        self.facedetailerCheckBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ubcf4\uc815(FaceDetailer)\uc744 \ucf1c\uace0 \ub055\ub2c8\ub2e4. \uc5bc\uad74\uc774 \ubb49\uac1c\uc9c8 \ub54c \ucf1c\uba74 \uc5bc\uad74\ub9cc \ub2e4\uc2dc \uadf8\ub824\uc90d\ub2c8\ub2e4. \ucc98\uc74c\uc5d0\ub294 \uaebc \ub450\ub294 \uac83\uc744 \ucd94\ucc9c\ud569\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerCheckBox.setText(QCoreApplication.translate("MainWindow", u"\U0001f464 FaceDetailer (\U0000c5bc\U0000ad74 \U0000bcf4\U0000c815 \U0000cf1c\U0000ae30)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerHelpBtn.setToolTip(QCoreApplication.translate("MainWindow", u"\ub20c\ub7ec\uc11c \uc5bc\uad74 \ubcf4\uc815 \uc635\uc158\uc744 \ucd08\ubcf4\uc790\ub3c4 \uc27d\uac8c \uc124\uba85\ud55c \uc804\uccb4 \uac00\uc774\ub4dc\ub97c \ubd05\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerHelpBtn.setText(QCoreApplication.translate("MainWindow", u"\u2753 \ub3c4\uc6c0\ub9d0", None))
#if QT_CONFIG(tooltip)
        self.facedetailerDenoiseLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74\uc744 \uc5bc\ub9c8\ub098 \uc0c8\ub85c \uadf8\ub9b4\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8\uac12 0.40 \ucd94\ucc9c. \ub192\uc73c\uba74 \uc5bc\uad74\uc774 \uc644\uc804\ud788 \ubc14\ub014 \uc218 \uc788\uc2b5\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerDenoiseLabel.setText(QCoreApplication.translate("MainWindow", u"Denoise (\uc5bc\uad74 \ub2e4\uc2dc\uadf8\ub9ac\uae30 \uc815\ub3c4)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerDenoiseSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74\uc744 \uc5bc\ub9c8\ub098 \uc0c8\ub85c \uadf8\ub9b4\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8\uac12 0.40 \ucd94\ucc9c. \uc5bc\uad74\uc774 \uacfc\ud558\uac8c \ubc14\ub00c\uba74 \uc774 \uac12\uc744 \ub0ae\ucd94\uc138\uc694.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerDenoiseValueLabel.setText(QCoreApplication.translate("MainWindow", u"0.40", None))
#if QT_CONFIG(tooltip)
        self.facedetailerStepsLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74\uc744 \uace0\uce58\ub294 \uacc4\uc0b0 \ud69f\uc218\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 20 \ucd94\ucc9c. \uc62c\ub9ac\uba74 \uc815\ubc00\ud574\uc9c0\uc9c0\ub9cc \ub290\ub824\uc9d1\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerStepsLabel.setText(QCoreApplication.translate("MainWindow", u"Steps (\ubcf4\uc815 \uc815\ubc00\ub3c4)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerStepsSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74\uc744 \uace0\uce58\ub294 \uacc4\uc0b0 \ud69f\uc218\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 20 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerStepsValueLabel.setText(QCoreApplication.translate("MainWindow", u"20", None))
#if QT_CONFIG(tooltip)
        self.facedetailerCfgLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\ud504\ub86c\ud504\ud2b8 \ub9d0\uc744 \uc5bc\ub9c8\ub098 \ub530\ub97c\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8\uac12 4.0 \ucd94\ucc9c. \ub108\ubb34 \ub192\uc73c\uba74 \uc5bc\uad74\uc774 \ubd80\uc790\uc5f0\uc2a4\ub7ec\uc6cc\uc9d1\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerCfgLabel.setText(QCoreApplication.translate("MainWindow", u"CFG (\ud504\ub86c\ud504\ud2b8 \ubc18\uc601 \uc138\uae30)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerCfgSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\ud504\ub86c\ud504\ud2b8 \ubc18\uc601 \uc138\uae30\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 4.0 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerCfgValueLabel.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
#if QT_CONFIG(tooltip)
        self.facedetailerFeatherLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uace0\uce5c \uc5bc\uad74\uacfc \uc8fc\ubcc0\uc744 \uc790\uc5f0\uc2a4\ub7fd\uac8c \uc774\uc5b4\uc8fc\ub294 \uc815\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 5 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerFeatherLabel.setText(QCoreApplication.translate("MainWindow", u"Feather (\uc5bc\uad74 \uacbd\uacc4 \uc790\uc5f0\uc2a4\ub7fd\uac8c)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerFeatherSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uacbd\uacc4 \ubd80\ub4dc\ub7ec\uc6c0\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 5 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerFeatherValueLabel.setText(QCoreApplication.translate("MainWindow", u"5", None))
#if QT_CONFIG(tooltip)
        self.facedetailerDropSizeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc774\ubcf4\ub2e4 \uc791\uac8c \uc7a1\ud78c \uc5bc\uad74\uc740 \ubb34\uc2dc\ud569\ub2c8\ub2e4. \uae30\ubcf8\uac12 10 \ucd94\ucc9c. \uc791\uc740 \uc5bc\uad74\uae4c\uc9c0 \uace0\uce58\ub824\uba74 \ub0ae\ucd94\uc138\uc694.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerDropSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Drop Size (\uc791\uc740 \uc5bc\uad74 \ubb34\uc2dc)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerDropSizeSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc791\uc740 \uc5bc\uad74 \ubb34\uc2dc \uae30\uc900\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 10 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerDropSizeValueLabel.setText(QCoreApplication.translate("MainWindow", u"10", None))
#if QT_CONFIG(tooltip)
        self.facedetailerGuideSizeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74\uc744 \ubd84\uc11d\ud560 \ud574\uc0c1\ub3c4\uc785\ub2c8\ub2e4. \ud45c\uc2dc \uac12 \uae30\uc900 \uae30\ubcf8 256 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerGuideSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Guide Size (\uc5bc\uad74 \ubd84\uc11d \ud06c\uae30)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerGuideSizeSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ubd84\uc11d \ud06c\uae30\uc785\ub2c8\ub2e4. \ud45c\uc2dc \uac12 \uae30\uc900 \uae30\ubcf8 256 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerGuideSizeValueLabel.setText(QCoreApplication.translate("MainWindow", u"256", None))
#if QT_CONFIG(tooltip)
        self.facedetailerMaxSizeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\ud55c \ubc88\uc5d0 \uace0\uce60 \uc218 \uc788\ub294 \ucd5c\ub300 \ud06c\uae30\uc785\ub2c8\ub2e4. \ud45c\uc2dc \uac12 \uae30\uc900 \uae30\ubcf8 768 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerMaxSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Max Size (\ubcf4\uc815 \ucd5c\ub300 \ud06c\uae30)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerMaxSizeSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\ubcf4\uc815 \ucd5c\ub300 \ud06c\uae30\uc785\ub2c8\ub2e4. \ud45c\uc2dc \uac12 \uae30\uc900 \uae30\ubcf8 768 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerMaxSizeValueLabel.setText(QCoreApplication.translate("MainWindow", u"768", None))
#if QT_CONFIG(tooltip)
        self.facedetailerCycleLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\ubcf4\uc815\uc744 \uba87 \ubc88 \ubc18\ubcf5\ud560\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8\uac12 1 \ucd94\ucc9c. 2 \uc774\uc0c1\uc740 \uc5bc\uad74\uc774 \ubcc0\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerCycleLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle (\ubcf4\uc815 \ubc18\ubcf5 \ud69f\uc218)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerCycleSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\ubcf4\uc815 \ubc18\ubcf5 \ud69f\uc218\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 1 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerCycleValueLabel.setText(QCoreApplication.translate("MainWindow", u"1", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxThresholdLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74\uc744 \ucc3e\ub294 \ubbfc\uac10\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8 0.50 \ucd94\ucc9c. \uc5bc\uad74\uc744 \ubabb \ucc3e\uc73c\uba74 \ub0ae\ucd94\uc138\uc694.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerBboxThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"BBox Thresh (\uc5bc\uad74 \ucc3e\uae30 \ubbfc\uac10\ub3c4)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxThresholdSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ucc3e\uae30 \ubbfc\uac10\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8 0.50 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerBboxThresholdValueLabel.setText(QCoreApplication.translate("MainWindow", u"0.50", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxDilationLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\ucc3e\uc740 \uc5bc\uad74 \uc0c1\uc790(\ubc15\uc2a4)\ub97c \uc5bc\ub9c8\ub098 \ub113\ud790\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8\uac12 10 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerBboxDilationLabel.setText(QCoreApplication.translate("MainWindow", u"BBox Dilate (\uc5bc\uad74 \ubc15\uc2a4 \ub113\ud788\uae30)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxDilationSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ubc15\uc2a4 \ub113\ud788\uae30\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 10 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerBboxDilationValueLabel.setText(QCoreApplication.translate("MainWindow", u"10", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxCropFactorLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc8fc\ubcc0\uc744 \uc5bc\ub9c8\ub098 \ud568\uaed8 \ubcfc\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8 1.50 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerBboxCropFactorLabel.setText(QCoreApplication.translate("MainWindow", u"Crop Factor (\uc5bc\uad74 \uc8fc\ubcc0 \uac19\uc774 \ubcf4\uae30)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxCropFactorSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc8fc\ubcc0 \uac19\uc774 \ubcf4\uae30\uc785\ub2c8\ub2e4. \uae30\ubcf8 1.50 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerBboxCropFactorValueLabel.setText(QCoreApplication.translate("MainWindow", u"1.50", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamThresholdLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc724\uacfd\uc120(\ub9c8\uc2a4\ud06c) \uc815\ubc00\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8 0.93 \ucd94\ucc9c. \uc9c0\uae08\uc740 SAM \ubbf8\uc0ac\uc6a9\uc73c\ub85c \ubd80\ubd84\ub9cc \uc801\uc6a9\ub429\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"SAM Thresh (\uc724\uacfd\uc120 \uc815\ubc00\ub3c4)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamThresholdSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc724\uacfd\uc120 \uc815\ubc00\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8 0.93 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamThresholdValueLabel.setText(QCoreApplication.translate("MainWindow", u"0.93", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamDilationLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc724\uacfd\uc120(\ub9c8\uc2a4\ud06c)\uc744 \ub113\ud790\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8 0 \ucd94\ucc9c. SAM \ubbf8\uc124\uc815 \uc2dc \uc77c\ubd80\ub9cc \uc801\uc6a9\ub429\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamDilationLabel.setText(QCoreApplication.translate("MainWindow", u"SAM Dilate (\uc724\uacfd\uc120 \ub113\ud788\uae30)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamDilationSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc724\uacfd\uc120 \ub113\ud788\uae30\uc785\ub2c8\ub2e4. \uae30\ubcf8 0 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamDilationValueLabel.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamBboxExpansionLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc724\uacfd\uc120(\ub9c8\uc2a4\ud06c) \uc601\uc5ed\uc744 \ub113\ud790\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8 0 \ucd94\ucc9c. SAM \ubbf8\uc124\uc815 \uc2dc \uc77c\ubd80\ub9cc \uc801\uc6a9\ub429\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamBboxExpansionLabel.setText(QCoreApplication.translate("MainWindow", u"SAM BBox Exp (\uc724\uacfd\uc120 \uc601\uc5ed \ub113\ud788\uae30)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamBboxExpansionSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc724\uacfd\uc120 \uc601\uc5ed \ub113\ud788\uae30\uc785\ub2c8\ub2e4. \uae30\ubcf8 0 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamBboxExpansionValueLabel.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintThresholdLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\ub9c8\uc2a4\ud06c \ud78c\ud2b8\ub97c \uc801\uc6a9\ud560\uc9c0 \ud310\uc815\ud558\ub294 \ubbfc\uac10\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8 0.70 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"Mask Hint Thresh (\ud78c\ud2b8 \ubbfc\uac10\ub3c4)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintThresholdSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\ud78c\ud2b8 \ubbfc\uac10\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8 0.70 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintThresholdValueLabel.setText(QCoreApplication.translate("MainWindow", u"0.70", None))
        self.openOutputFolderButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c1 \U0000d3f4\U0000b354 \U0000c5f4\U0000ae30", None))
        self.chatInputEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\uba54\uc2dc\uc9c0\ub97c \uc785\ub825\ud558\uc138\uc694... \uc608: \uc774\uc058\uace0 \uadc0\uc5ec\uc6b4 \uace0\uc591\uc774 3\ub9c8\ub9ac \uadf8\ub824\uc918", None))
#if QT_CONFIG(tooltip)
        self.sendBtn.setToolTip(QCoreApplication.translate("MainWindow", u"\uc774\ubbf8\uc9c0 \uc0dd\uc131\ud558\uae30 (P2\uc5d0\uc11c \uc5f0\uacb0)", None))
#endif // QT_CONFIG(tooltip)
        self.sendBtn.setText(QCoreApplication.translate("MainWindow", u"\u27a4", None))
    # retranslateUi

