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
        self.railHomeBtn = QPushButton(self.railFrame)
        self.railHomeBtn.setObjectName(u"railHomeBtn")
        self.railHomeBtn.setMinimumSize(QSize(55, 55))
        self.railHomeBtn.setMaximumSize(QSize(55, 55))
        self.railHomeBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.railLayout.addWidget(self.railHomeBtn)

        self.railOptionsBtn = QPushButton(self.railFrame)
        self.railOptionsBtn.setObjectName(u"railOptionsBtn")
        self.railOptionsBtn.setMinimumSize(QSize(55, 55))
        self.railOptionsBtn.setMaximumSize(QSize(55, 55))
        self.railOptionsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.railLayout.addWidget(self.railOptionsBtn)

        self.railHistoryBtn = QPushButton(self.railFrame)
        self.railHistoryBtn.setObjectName(u"railHistoryBtn")
        self.railHistoryBtn.setMinimumSize(QSize(55, 55))
        self.railHistoryBtn.setMaximumSize(QSize(55, 55))
        self.railHistoryBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.railLayout.addWidget(self.railHistoryBtn)

        self.railSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.railLayout.addItem(self.railSpacer)

        self.railHelpBtn = QPushButton(self.railFrame)
        self.railHelpBtn.setObjectName(u"railHelpBtn")
        self.railHelpBtn.setMinimumSize(QSize(55, 55))
        self.railHelpBtn.setMaximumSize(QSize(55, 55))
        self.railHelpBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.railLayout.addWidget(self.railHelpBtn)

        self.railSettingsBtn = QPushButton(self.railFrame)
        self.railSettingsBtn.setObjectName(u"railSettingsBtn")
        self.railSettingsBtn.setMinimumSize(QSize(55, 55))
        self.railSettingsBtn.setMaximumSize(QSize(55, 55))
        self.railSettingsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.railLayout.addWidget(self.railSettingsBtn)


        self.studioLayout.addWidget(self.railFrame)

        self.leftScrollArea = QScrollArea(self.studioContainer)
        self.leftScrollArea.setObjectName(u"leftScrollArea")
        self.leftScrollArea.setMaximumSize(QSize(340, 16777215))
        self.leftScrollArea.setVisible(False)
        self.leftScrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.leftScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.leftScrollArea.setWidgetResizable(True)
        self.leftContentWidget = QWidget()
        self.leftContentWidget.setObjectName(u"leftContentWidget")
        self.leftContentWidget.setGeometry(QRect(0, 0, 663, 1138))
        self.optionsLayout = QVBoxLayout(self.leftContentWidget)
        self.optionsLayout.setSpacing(8)
        self.optionsLayout.setObjectName(u"optionsLayout")
        self.capModel = QLabel(self.leftContentWidget)
        self.capModel.setObjectName(u"capModel")

        self.optionsLayout.addWidget(self.capModel)

        self.modelCurrentLabel = QLabel(self.leftContentWidget)
        self.modelCurrentLabel.setObjectName(u"modelCurrentLabel")

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
        self.preset_1024x1024.setMinimumSize(QSize(0, 48))
        self.preset_1024x1024.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.presetsButtonLayout.addWidget(self.preset_1024x1024)

        self.preset_896x1152 = QPushButton(self.leftContentWidget)
        self.preset_896x1152.setObjectName(u"preset_896x1152")
        self.preset_896x1152.setMinimumSize(QSize(0, 48))
        self.preset_896x1152.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.presetsButtonLayout.addWidget(self.preset_896x1152)

        self.preset_1152x896 = QPushButton(self.leftContentWidget)
        self.preset_1152x896.setObjectName(u"preset_1152x896")
        self.preset_1152x896.setMinimumSize(QSize(0, 48))
        self.preset_1152x896.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

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
        self.widthSpinBox.setMinimumSize(QSize(75, 28))

        self.hboxLayout.addWidget(self.widthSpinBox)

        self.heightLabel = QLabel(self.leftContentWidget)
        self.heightLabel.setObjectName(u"heightLabel")
        self.heightLabel.setMinimumSize(QSize(64, 0))

        self.hboxLayout.addWidget(self.heightLabel)

        self.heightSpinBox = QSpinBox(self.leftContentWidget)
        self.heightSpinBox.setObjectName(u"heightSpinBox")
        self.heightSpinBox.setMinimumSize(QSize(75, 28))

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

        self.optionsLayout.addWidget(self.enhancePromptEdit)

        self.positivePromptEdit = QPlainTextEdit(self.leftContentWidget)
        self.positivePromptEdit.setObjectName(u"positivePromptEdit")
        self.positivePromptEdit.setMinimumSize(QSize(0, 76))
        self.positivePromptEdit.setVisible(False)

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
        self.facedetailerPanelHBox = QHBoxLayout(self.facedetailerPanel)
        self.facedetailerPanelHBox.setSpacing(16)
        self.facedetailerPanelHBox.setObjectName(u"facedetailerPanelHBox")
        self.facedetailerPanelHBox.setContentsMargins(8, 8, 8, 8)
        self.fdLeftCol = QVBoxLayout()
        self.fdLeftCol.setSpacing(8)
        self.fdLeftCol.setObjectName(u"fdLeftCol")
        self.fd_denoise_vbox = QVBoxLayout()
        self.fd_denoise_vbox.setSpacing(2)
        self.fd_denoise_vbox.setObjectName(u"fd_denoise_vbox")
        self.fd_denoise_hdr = QHBoxLayout()
        self.fd_denoise_hdr.setObjectName(u"fd_denoise_hdr")
        self.facedetailerDenoiseLabel = QLabel(self.facedetailerPanel)
        self.facedetailerDenoiseLabel.setObjectName(u"facedetailerDenoiseLabel")

        self.fd_denoise_hdr.addWidget(self.facedetailerDenoiseLabel)

        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_denoise_hdr.addItem(self.spacerItem)

        self.facedetailerDenoiseValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerDenoiseValueLabel.setObjectName(u"facedetailerDenoiseValueLabel")

        self.fd_denoise_hdr.addWidget(self.facedetailerDenoiseValueLabel)


        self.fd_denoise_vbox.addLayout(self.fd_denoise_hdr)

        self.facedetailerDenoiseSlider = QSlider(self.facedetailerPanel)
        self.facedetailerDenoiseSlider.setObjectName(u"facedetailerDenoiseSlider")
        self.facedetailerDenoiseSlider.setMinimum(0)
        self.facedetailerDenoiseSlider.setMaximum(100)
        self.facedetailerDenoiseSlider.setValue(40)
        self.facedetailerDenoiseSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_denoise_vbox.addWidget(self.facedetailerDenoiseSlider)


        self.fdLeftCol.addLayout(self.fd_denoise_vbox)

        self.fd_steps_vbox = QVBoxLayout()
        self.fd_steps_vbox.setSpacing(2)
        self.fd_steps_vbox.setObjectName(u"fd_steps_vbox")
        self.fd_steps_hdr = QHBoxLayout()
        self.fd_steps_hdr.setObjectName(u"fd_steps_hdr")
        self.facedetailerStepsLabel = QLabel(self.facedetailerPanel)
        self.facedetailerStepsLabel.setObjectName(u"facedetailerStepsLabel")

        self.fd_steps_hdr.addWidget(self.facedetailerStepsLabel)

        self.spacerItem1 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_steps_hdr.addItem(self.spacerItem1)

        self.facedetailerStepsValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerStepsValueLabel.setObjectName(u"facedetailerStepsValueLabel")

        self.fd_steps_hdr.addWidget(self.facedetailerStepsValueLabel)


        self.fd_steps_vbox.addLayout(self.fd_steps_hdr)

        self.facedetailerStepsSlider = QSlider(self.facedetailerPanel)
        self.facedetailerStepsSlider.setObjectName(u"facedetailerStepsSlider")
        self.facedetailerStepsSlider.setMinimum(1)
        self.facedetailerStepsSlider.setMaximum(50)
        self.facedetailerStepsSlider.setValue(20)
        self.facedetailerStepsSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_steps_vbox.addWidget(self.facedetailerStepsSlider)


        self.fdLeftCol.addLayout(self.fd_steps_vbox)

        self.fd_cfg_vbox = QVBoxLayout()
        self.fd_cfg_vbox.setSpacing(2)
        self.fd_cfg_vbox.setObjectName(u"fd_cfg_vbox")
        self.fd_cfg_hdr = QHBoxLayout()
        self.fd_cfg_hdr.setObjectName(u"fd_cfg_hdr")
        self.facedetailerCfgLabel = QLabel(self.facedetailerPanel)
        self.facedetailerCfgLabel.setObjectName(u"facedetailerCfgLabel")

        self.fd_cfg_hdr.addWidget(self.facedetailerCfgLabel)

        self.spacerItem2 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_cfg_hdr.addItem(self.spacerItem2)

        self.facedetailerCfgValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerCfgValueLabel.setObjectName(u"facedetailerCfgValueLabel")

        self.fd_cfg_hdr.addWidget(self.facedetailerCfgValueLabel)


        self.fd_cfg_vbox.addLayout(self.fd_cfg_hdr)

        self.facedetailerCfgSlider = QSlider(self.facedetailerPanel)
        self.facedetailerCfgSlider.setObjectName(u"facedetailerCfgSlider")
        self.facedetailerCfgSlider.setMinimum(0)
        self.facedetailerCfgSlider.setMaximum(200)
        self.facedetailerCfgSlider.setValue(40)
        self.facedetailerCfgSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_cfg_vbox.addWidget(self.facedetailerCfgSlider)


        self.fdLeftCol.addLayout(self.fd_cfg_vbox)

        self.fd_feather_vbox = QVBoxLayout()
        self.fd_feather_vbox.setSpacing(2)
        self.fd_feather_vbox.setObjectName(u"fd_feather_vbox")
        self.fd_feather_hdr = QHBoxLayout()
        self.fd_feather_hdr.setObjectName(u"fd_feather_hdr")
        self.facedetailerFeatherLabel = QLabel(self.facedetailerPanel)
        self.facedetailerFeatherLabel.setObjectName(u"facedetailerFeatherLabel")

        self.fd_feather_hdr.addWidget(self.facedetailerFeatherLabel)

        self.spacerItem3 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_feather_hdr.addItem(self.spacerItem3)

        self.facedetailerFeatherValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerFeatherValueLabel.setObjectName(u"facedetailerFeatherValueLabel")

        self.fd_feather_hdr.addWidget(self.facedetailerFeatherValueLabel)


        self.fd_feather_vbox.addLayout(self.fd_feather_hdr)

        self.facedetailerFeatherSlider = QSlider(self.facedetailerPanel)
        self.facedetailerFeatherSlider.setObjectName(u"facedetailerFeatherSlider")
        self.facedetailerFeatherSlider.setMinimum(0)
        self.facedetailerFeatherSlider.setMaximum(20)
        self.facedetailerFeatherSlider.setValue(5)
        self.facedetailerFeatherSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_feather_vbox.addWidget(self.facedetailerFeatherSlider)


        self.fdLeftCol.addLayout(self.fd_feather_vbox)

        self.fd_dropsize_vbox = QVBoxLayout()
        self.fd_dropsize_vbox.setSpacing(2)
        self.fd_dropsize_vbox.setObjectName(u"fd_dropsize_vbox")
        self.fd_dropsize_hdr = QHBoxLayout()
        self.fd_dropsize_hdr.setObjectName(u"fd_dropsize_hdr")
        self.facedetailerDropSizeLabel = QLabel(self.facedetailerPanel)
        self.facedetailerDropSizeLabel.setObjectName(u"facedetailerDropSizeLabel")

        self.fd_dropsize_hdr.addWidget(self.facedetailerDropSizeLabel)

        self.spacerItem4 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_dropsize_hdr.addItem(self.spacerItem4)

        self.facedetailerDropSizeValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerDropSizeValueLabel.setObjectName(u"facedetailerDropSizeValueLabel")

        self.fd_dropsize_hdr.addWidget(self.facedetailerDropSizeValueLabel)


        self.fd_dropsize_vbox.addLayout(self.fd_dropsize_hdr)

        self.facedetailerDropSizeSlider = QSlider(self.facedetailerPanel)
        self.facedetailerDropSizeSlider.setObjectName(u"facedetailerDropSizeSlider")
        self.facedetailerDropSizeSlider.setMinimum(1)
        self.facedetailerDropSizeSlider.setMaximum(100)
        self.facedetailerDropSizeSlider.setValue(10)
        self.facedetailerDropSizeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_dropsize_vbox.addWidget(self.facedetailerDropSizeSlider)


        self.fdLeftCol.addLayout(self.fd_dropsize_vbox)

        self.fd_guidesize_vbox = QVBoxLayout()
        self.fd_guidesize_vbox.setSpacing(2)
        self.fd_guidesize_vbox.setObjectName(u"fd_guidesize_vbox")
        self.fd_guidesize_hdr = QHBoxLayout()
        self.fd_guidesize_hdr.setObjectName(u"fd_guidesize_hdr")
        self.facedetailerGuideSizeLabel = QLabel(self.facedetailerPanel)
        self.facedetailerGuideSizeLabel.setObjectName(u"facedetailerGuideSizeLabel")

        self.fd_guidesize_hdr.addWidget(self.facedetailerGuideSizeLabel)

        self.spacerItem5 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_guidesize_hdr.addItem(self.spacerItem5)

        self.facedetailerGuideSizeValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerGuideSizeValueLabel.setObjectName(u"facedetailerGuideSizeValueLabel")

        self.fd_guidesize_hdr.addWidget(self.facedetailerGuideSizeValueLabel)


        self.fd_guidesize_vbox.addLayout(self.fd_guidesize_hdr)

        self.facedetailerGuideSizeSlider = QSlider(self.facedetailerPanel)
        self.facedetailerGuideSizeSlider.setObjectName(u"facedetailerGuideSizeSlider")
        self.facedetailerGuideSizeSlider.setMinimum(1)
        self.facedetailerGuideSizeSlider.setMaximum(16)
        self.facedetailerGuideSizeSlider.setValue(4)
        self.facedetailerGuideSizeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_guidesize_vbox.addWidget(self.facedetailerGuideSizeSlider)


        self.fdLeftCol.addLayout(self.fd_guidesize_vbox)

        self.fd_maxsize_vbox = QVBoxLayout()
        self.fd_maxsize_vbox.setSpacing(2)
        self.fd_maxsize_vbox.setObjectName(u"fd_maxsize_vbox")
        self.fd_maxsize_hdr = QHBoxLayout()
        self.fd_maxsize_hdr.setObjectName(u"fd_maxsize_hdr")
        self.facedetailerMaxSizeLabel = QLabel(self.facedetailerPanel)
        self.facedetailerMaxSizeLabel.setObjectName(u"facedetailerMaxSizeLabel")

        self.fd_maxsize_hdr.addWidget(self.facedetailerMaxSizeLabel)

        self.spacerItem6 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_maxsize_hdr.addItem(self.spacerItem6)

        self.facedetailerMaxSizeValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerMaxSizeValueLabel.setObjectName(u"facedetailerMaxSizeValueLabel")

        self.fd_maxsize_hdr.addWidget(self.facedetailerMaxSizeValueLabel)


        self.fd_maxsize_vbox.addLayout(self.fd_maxsize_hdr)

        self.facedetailerMaxSizeSlider = QSlider(self.facedetailerPanel)
        self.facedetailerMaxSizeSlider.setObjectName(u"facedetailerMaxSizeSlider")
        self.facedetailerMaxSizeSlider.setMinimum(2)
        self.facedetailerMaxSizeSlider.setMaximum(32)
        self.facedetailerMaxSizeSlider.setValue(12)
        self.facedetailerMaxSizeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_maxsize_vbox.addWidget(self.facedetailerMaxSizeSlider)


        self.fdLeftCol.addLayout(self.fd_maxsize_vbox)

        self.fd_cycle_vbox = QVBoxLayout()
        self.fd_cycle_vbox.setSpacing(2)
        self.fd_cycle_vbox.setObjectName(u"fd_cycle_vbox")
        self.fd_cycle_hdr = QHBoxLayout()
        self.fd_cycle_hdr.setObjectName(u"fd_cycle_hdr")
        self.facedetailerCycleLabel = QLabel(self.facedetailerPanel)
        self.facedetailerCycleLabel.setObjectName(u"facedetailerCycleLabel")

        self.fd_cycle_hdr.addWidget(self.facedetailerCycleLabel)

        self.spacerItem7 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_cycle_hdr.addItem(self.spacerItem7)

        self.facedetailerCycleValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerCycleValueLabel.setObjectName(u"facedetailerCycleValueLabel")

        self.fd_cycle_hdr.addWidget(self.facedetailerCycleValueLabel)


        self.fd_cycle_vbox.addLayout(self.fd_cycle_hdr)

        self.facedetailerCycleSlider = QSlider(self.facedetailerPanel)
        self.facedetailerCycleSlider.setObjectName(u"facedetailerCycleSlider")
        self.facedetailerCycleSlider.setMinimum(1)
        self.facedetailerCycleSlider.setMaximum(10)
        self.facedetailerCycleSlider.setValue(1)
        self.facedetailerCycleSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_cycle_vbox.addWidget(self.facedetailerCycleSlider)


        self.fdLeftCol.addLayout(self.fd_cycle_vbox)

        self.spacerItem8 = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.fdLeftCol.addItem(self.spacerItem8)


        self.facedetailerPanelHBox.addLayout(self.fdLeftCol)

        self.fdSeparatorLine = QFrame(self.facedetailerPanel)
        self.fdSeparatorLine.setObjectName(u"fdSeparatorLine")
        self.fdSeparatorLine.setFrameShape(QFrame.Shape.VLine)
        self.fdSeparatorLine.setFrameShadow(QFrame.Shadow.Sunken)

        self.facedetailerPanelHBox.addWidget(self.fdSeparatorLine)

        self.fdRightCol = QVBoxLayout()
        self.fdRightCol.setSpacing(8)
        self.fdRightCol.setObjectName(u"fdRightCol")
        self.fd_bboxthresh_vbox = QVBoxLayout()
        self.fd_bboxthresh_vbox.setSpacing(2)
        self.fd_bboxthresh_vbox.setObjectName(u"fd_bboxthresh_vbox")
        self.fd_bboxthresh_hdr = QHBoxLayout()
        self.fd_bboxthresh_hdr.setObjectName(u"fd_bboxthresh_hdr")
        self.facedetailerBboxThresholdLabel = QLabel(self.facedetailerPanel)
        self.facedetailerBboxThresholdLabel.setObjectName(u"facedetailerBboxThresholdLabel")

        self.fd_bboxthresh_hdr.addWidget(self.facedetailerBboxThresholdLabel)

        self.spacerItem9 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_bboxthresh_hdr.addItem(self.spacerItem9)

        self.facedetailerBboxThresholdValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerBboxThresholdValueLabel.setObjectName(u"facedetailerBboxThresholdValueLabel")

        self.fd_bboxthresh_hdr.addWidget(self.facedetailerBboxThresholdValueLabel)


        self.fd_bboxthresh_vbox.addLayout(self.fd_bboxthresh_hdr)

        self.facedetailerBboxThresholdSlider = QSlider(self.facedetailerPanel)
        self.facedetailerBboxThresholdSlider.setObjectName(u"facedetailerBboxThresholdSlider")
        self.facedetailerBboxThresholdSlider.setMinimum(10)
        self.facedetailerBboxThresholdSlider.setMaximum(100)
        self.facedetailerBboxThresholdSlider.setValue(50)
        self.facedetailerBboxThresholdSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_bboxthresh_vbox.addWidget(self.facedetailerBboxThresholdSlider)


        self.fdRightCol.addLayout(self.fd_bboxthresh_vbox)

        self.fd_bboxdilate_vbox = QVBoxLayout()
        self.fd_bboxdilate_vbox.setSpacing(2)
        self.fd_bboxdilate_vbox.setObjectName(u"fd_bboxdilate_vbox")
        self.fd_bboxdilate_hdr = QHBoxLayout()
        self.fd_bboxdilate_hdr.setObjectName(u"fd_bboxdilate_hdr")
        self.facedetailerBboxDilationLabel = QLabel(self.facedetailerPanel)
        self.facedetailerBboxDilationLabel.setObjectName(u"facedetailerBboxDilationLabel")

        self.fd_bboxdilate_hdr.addWidget(self.facedetailerBboxDilationLabel)

        self.spacerItem10 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_bboxdilate_hdr.addItem(self.spacerItem10)

        self.facedetailerBboxDilationValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerBboxDilationValueLabel.setObjectName(u"facedetailerBboxDilationValueLabel")

        self.fd_bboxdilate_hdr.addWidget(self.facedetailerBboxDilationValueLabel)


        self.fd_bboxdilate_vbox.addLayout(self.fd_bboxdilate_hdr)

        self.facedetailerBboxDilationSlider = QSlider(self.facedetailerPanel)
        self.facedetailerBboxDilationSlider.setObjectName(u"facedetailerBboxDilationSlider")
        self.facedetailerBboxDilationSlider.setMinimum(-20)
        self.facedetailerBboxDilationSlider.setMaximum(100)
        self.facedetailerBboxDilationSlider.setValue(10)
        self.facedetailerBboxDilationSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_bboxdilate_vbox.addWidget(self.facedetailerBboxDilationSlider)


        self.fdRightCol.addLayout(self.fd_bboxdilate_vbox)

        self.fd_cropfactor_vbox = QVBoxLayout()
        self.fd_cropfactor_vbox.setSpacing(2)
        self.fd_cropfactor_vbox.setObjectName(u"fd_cropfactor_vbox")
        self.fd_cropfactor_hdr = QHBoxLayout()
        self.fd_cropfactor_hdr.setObjectName(u"fd_cropfactor_hdr")
        self.facedetailerBboxCropFactorLabel = QLabel(self.facedetailerPanel)
        self.facedetailerBboxCropFactorLabel.setObjectName(u"facedetailerBboxCropFactorLabel")

        self.fd_cropfactor_hdr.addWidget(self.facedetailerBboxCropFactorLabel)

        self.spacerItem11 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_cropfactor_hdr.addItem(self.spacerItem11)

        self.facedetailerBboxCropFactorValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerBboxCropFactorValueLabel.setObjectName(u"facedetailerBboxCropFactorValueLabel")

        self.fd_cropfactor_hdr.addWidget(self.facedetailerBboxCropFactorValueLabel)


        self.fd_cropfactor_vbox.addLayout(self.fd_cropfactor_hdr)

        self.facedetailerBboxCropFactorSlider = QSlider(self.facedetailerPanel)
        self.facedetailerBboxCropFactorSlider.setObjectName(u"facedetailerBboxCropFactorSlider")
        self.facedetailerBboxCropFactorSlider.setMinimum(100)
        self.facedetailerBboxCropFactorSlider.setMaximum(500)
        self.facedetailerBboxCropFactorSlider.setValue(150)
        self.facedetailerBboxCropFactorSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_cropfactor_vbox.addWidget(self.facedetailerBboxCropFactorSlider)


        self.fdRightCol.addLayout(self.fd_cropfactor_vbox)

        self.fd_samthresh_vbox = QVBoxLayout()
        self.fd_samthresh_vbox.setSpacing(2)
        self.fd_samthresh_vbox.setObjectName(u"fd_samthresh_vbox")
        self.fd_samthresh_hdr = QHBoxLayout()
        self.fd_samthresh_hdr.setObjectName(u"fd_samthresh_hdr")
        self.facedetailerSamThresholdLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamThresholdLabel.setObjectName(u"facedetailerSamThresholdLabel")

        self.fd_samthresh_hdr.addWidget(self.facedetailerSamThresholdLabel)

        self.spacerItem12 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_samthresh_hdr.addItem(self.spacerItem12)

        self.facedetailerSamThresholdValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamThresholdValueLabel.setObjectName(u"facedetailerSamThresholdValueLabel")

        self.fd_samthresh_hdr.addWidget(self.facedetailerSamThresholdValueLabel)


        self.fd_samthresh_vbox.addLayout(self.fd_samthresh_hdr)

        self.facedetailerSamThresholdSlider = QSlider(self.facedetailerPanel)
        self.facedetailerSamThresholdSlider.setObjectName(u"facedetailerSamThresholdSlider")
        self.facedetailerSamThresholdSlider.setMinimum(10)
        self.facedetailerSamThresholdSlider.setMaximum(100)
        self.facedetailerSamThresholdSlider.setValue(93)
        self.facedetailerSamThresholdSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_samthresh_vbox.addWidget(self.facedetailerSamThresholdSlider)


        self.fdRightCol.addLayout(self.fd_samthresh_vbox)

        self.fd_samdilate_vbox = QVBoxLayout()
        self.fd_samdilate_vbox.setSpacing(2)
        self.fd_samdilate_vbox.setObjectName(u"fd_samdilate_vbox")
        self.fd_samdilate_hdr = QHBoxLayout()
        self.fd_samdilate_hdr.setObjectName(u"fd_samdilate_hdr")
        self.facedetailerSamDilationLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamDilationLabel.setObjectName(u"facedetailerSamDilationLabel")

        self.fd_samdilate_hdr.addWidget(self.facedetailerSamDilationLabel)

        self.spacerItem13 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_samdilate_hdr.addItem(self.spacerItem13)

        self.facedetailerSamDilationValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamDilationValueLabel.setObjectName(u"facedetailerSamDilationValueLabel")

        self.fd_samdilate_hdr.addWidget(self.facedetailerSamDilationValueLabel)


        self.fd_samdilate_vbox.addLayout(self.fd_samdilate_hdr)

        self.facedetailerSamDilationSlider = QSlider(self.facedetailerPanel)
        self.facedetailerSamDilationSlider.setObjectName(u"facedetailerSamDilationSlider")
        self.facedetailerSamDilationSlider.setMinimum(0)
        self.facedetailerSamDilationSlider.setMaximum(100)
        self.facedetailerSamDilationSlider.setValue(0)
        self.facedetailerSamDilationSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_samdilate_vbox.addWidget(self.facedetailerSamDilationSlider)


        self.fdRightCol.addLayout(self.fd_samdilate_vbox)

        self.fd_sambboxexp_vbox = QVBoxLayout()
        self.fd_sambboxexp_vbox.setSpacing(2)
        self.fd_sambboxexp_vbox.setObjectName(u"fd_sambboxexp_vbox")
        self.fd_sambboxexp_hdr = QHBoxLayout()
        self.fd_sambboxexp_hdr.setObjectName(u"fd_sambboxexp_hdr")
        self.facedetailerSamBboxExpansionLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamBboxExpansionLabel.setObjectName(u"facedetailerSamBboxExpansionLabel")

        self.fd_sambboxexp_hdr.addWidget(self.facedetailerSamBboxExpansionLabel)

        self.spacerItem14 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_sambboxexp_hdr.addItem(self.spacerItem14)

        self.facedetailerSamBboxExpansionValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamBboxExpansionValueLabel.setObjectName(u"facedetailerSamBboxExpansionValueLabel")

        self.fd_sambboxexp_hdr.addWidget(self.facedetailerSamBboxExpansionValueLabel)


        self.fd_sambboxexp_vbox.addLayout(self.fd_sambboxexp_hdr)

        self.facedetailerSamBboxExpansionSlider = QSlider(self.facedetailerPanel)
        self.facedetailerSamBboxExpansionSlider.setObjectName(u"facedetailerSamBboxExpansionSlider")
        self.facedetailerSamBboxExpansionSlider.setMinimum(0)
        self.facedetailerSamBboxExpansionSlider.setMaximum(100)
        self.facedetailerSamBboxExpansionSlider.setValue(0)
        self.facedetailerSamBboxExpansionSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_sambboxexp_vbox.addWidget(self.facedetailerSamBboxExpansionSlider)


        self.fdRightCol.addLayout(self.fd_sambboxexp_vbox)

        self.fd_maskhintthresh_vbox = QVBoxLayout()
        self.fd_maskhintthresh_vbox.setSpacing(2)
        self.fd_maskhintthresh_vbox.setObjectName(u"fd_maskhintthresh_vbox")
        self.fd_maskhintthresh_hdr = QHBoxLayout()
        self.fd_maskhintthresh_hdr.setObjectName(u"fd_maskhintthresh_hdr")
        self.facedetailerSamMaskHintThresholdLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamMaskHintThresholdLabel.setObjectName(u"facedetailerSamMaskHintThresholdLabel")

        self.fd_maskhintthresh_hdr.addWidget(self.facedetailerSamMaskHintThresholdLabel)

        self.spacerItem15 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_maskhintthresh_hdr.addItem(self.spacerItem15)

        self.facedetailerSamMaskHintThresholdValueLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamMaskHintThresholdValueLabel.setObjectName(u"facedetailerSamMaskHintThresholdValueLabel")

        self.fd_maskhintthresh_hdr.addWidget(self.facedetailerSamMaskHintThresholdValueLabel)


        self.fd_maskhintthresh_vbox.addLayout(self.fd_maskhintthresh_hdr)

        self.facedetailerSamMaskHintThresholdSlider = QSlider(self.facedetailerPanel)
        self.facedetailerSamMaskHintThresholdSlider.setObjectName(u"facedetailerSamMaskHintThresholdSlider")
        self.facedetailerSamMaskHintThresholdSlider.setMinimum(10)
        self.facedetailerSamMaskHintThresholdSlider.setMaximum(100)
        self.facedetailerSamMaskHintThresholdSlider.setValue(70)
        self.facedetailerSamMaskHintThresholdSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_maskhintthresh_vbox.addWidget(self.facedetailerSamMaskHintThresholdSlider)


        self.fdRightCol.addLayout(self.fd_maskhintthresh_vbox)

        self.fd_samhint_row = QHBoxLayout()
        self.fd_samhint_row.setObjectName(u"fd_samhint_row")
        self.facedetailerSamDetectionHintLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamDetectionHintLabel.setObjectName(u"facedetailerSamDetectionHintLabel")

        self.fd_samhint_row.addWidget(self.facedetailerSamDetectionHintLabel)

        self.spacerItem16 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_samhint_row.addItem(self.spacerItem16)

        self.facedetailerSamDetectionHintComboBox = QComboBox(self.facedetailerPanel)
        self.facedetailerSamDetectionHintComboBox.setObjectName(u"facedetailerSamDetectionHintComboBox")
        self.facedetailerSamDetectionHintComboBox.setMinimumSize(QSize(105, 26))

        self.fd_samhint_row.addWidget(self.facedetailerSamDetectionHintComboBox)


        self.fdRightCol.addLayout(self.fd_samhint_row)

        self.fd_maskhintneg_row = QHBoxLayout()
        self.fd_maskhintneg_row.setObjectName(u"fd_maskhintneg_row")
        self.facedetailerSamMaskHintUseNegativeLabel = QLabel(self.facedetailerPanel)
        self.facedetailerSamMaskHintUseNegativeLabel.setObjectName(u"facedetailerSamMaskHintUseNegativeLabel")

        self.fd_maskhintneg_row.addWidget(self.facedetailerSamMaskHintUseNegativeLabel)

        self.spacerItem17 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_maskhintneg_row.addItem(self.spacerItem17)

        self.facedetailerSamMaskHintUseNegativeComboBox = QComboBox(self.facedetailerPanel)
        self.facedetailerSamMaskHintUseNegativeComboBox.setObjectName(u"facedetailerSamMaskHintUseNegativeComboBox")
        self.facedetailerSamMaskHintUseNegativeComboBox.setMinimumSize(QSize(105, 26))

        self.fd_maskhintneg_row.addWidget(self.facedetailerSamMaskHintUseNegativeComboBox)


        self.fdRightCol.addLayout(self.fd_maskhintneg_row)

        self.spacerItem18 = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.fdRightCol.addItem(self.spacerItem18)


        self.facedetailerPanelHBox.addLayout(self.fdRightCol)


        self.optionsLayout.addWidget(self.facedetailerPanel)

        self.openOutputFolderButton = QPushButton(self.leftContentWidget)
        self.openOutputFolderButton.setObjectName(u"openOutputFolderButton")
        self.openOutputFolderButton.setMinimumSize(QSize(0, 34))
        self.openOutputFolderButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.optionsLayout.addWidget(self.openOutputFolderButton)

        self.leftScrollArea.setWidget(self.leftContentWidget)

        self.studioLayout.addWidget(self.leftScrollArea)

        self.chatFrame = QFrame(self.studioContainer)
        self.chatFrame.setObjectName(u"chatFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chatFrame.sizePolicy().hasHeightForWidth())
        self.chatFrame.setSizePolicy(sizePolicy)
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
        self.facedetailerDenoiseValueLabel.setText(QCoreApplication.translate("MainWindow", u"0.40", None))
#if QT_CONFIG(tooltip)
        self.facedetailerDenoiseSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74\uc744 \uc5bc\ub9c8\ub098 \uc0c8\ub85c \uadf8\ub9b4\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8\uac12 0.40 \ucd94\ucc9c. \uc5bc\uad74\uc774 \uacfc\ud558\uac8c \ubc14\ub00c\uba74 \uc774 \uac12\uc744 \ub0ae\ucd94\uc138\uc694.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerStepsLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74\uc744 \uace0\uce58\ub294 \uacc4\uc0b0 \ud69f\uc218\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 20 \ucd94\ucc9c. \uc62c\ub9ac\uba74 \uc815\ubc00\ud574\uc9c0\uc9c0\ub9cc \ub290\ub824\uc9d1\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerStepsLabel.setText(QCoreApplication.translate("MainWindow", u"Steps (\ubcf4\uc815 \uc815\ubc00\ub3c4)", None))
        self.facedetailerStepsValueLabel.setText(QCoreApplication.translate("MainWindow", u"20", None))
#if QT_CONFIG(tooltip)
        self.facedetailerStepsSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74\uc744 \uace0\uce58\ub294 \uacc4\uc0b0 \ud69f\uc218\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 20 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerCfgLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\ud504\ub86c\ud504\ud2b8 \ub9d0\uc744 \uc5bc\ub9c8\ub098 \ub530\ub97c\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8\uac12 4.0 \ucd94\ucc9c. \ub108\ubb34 \ub192\uc73c\uba74 \uc5bc\uad74\uc774 \ubd80\uc790\uc5f0\uc2a4\ub7ec\uc6cc\uc9d1\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerCfgLabel.setText(QCoreApplication.translate("MainWindow", u"CFG (\ud504\ub86c\ud504\ud2b8 \ubc18\uc601 \uc138\uae30)", None))
        self.facedetailerCfgValueLabel.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
#if QT_CONFIG(tooltip)
        self.facedetailerCfgSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\ud504\ub86c\ud504\ud2b8 \ubc18\uc601 \uc138\uae30\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 4.0 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerFeatherLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uace0\uce5c \uc5bc\uad74\uacfc \uc8fc\ubcc0\uc744 \uc790\uc5f0\uc2a4\ub7fd\uac8c \uc774\uc5b4\uc8fc\ub294 \uc815\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 5 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerFeatherLabel.setText(QCoreApplication.translate("MainWindow", u"Feather (\uc5bc\uad74 \uacbd\uacc4 \uc790\uc5f0\uc2a4\ub7fd\uac8c)", None))
        self.facedetailerFeatherValueLabel.setText(QCoreApplication.translate("MainWindow", u"5", None))
#if QT_CONFIG(tooltip)
        self.facedetailerFeatherSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uacbd\uacc4 \ubd80\ub4dc\ub7ec\uc6c0\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 5 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerDropSizeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc774\ubcf4\ub2e4 \uc791\uac8c \uc7a1\ud78c \uc5bc\uad74\uc740 \ubb34\uc2dc\ud569\ub2c8\ub2e4. \uae30\ubcf8\uac12 10 \ucd94\ucc9c. \uc791\uc740 \uc5bc\uad74\uae4c\uc9c0 \uace0\uce58\ub824\uba74 \ub0ae\ucd94\uc138\uc694.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerDropSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Drop Size (\uc791\uc740 \uc5bc\uad74 \ubb34\uc2dc)", None))
        self.facedetailerDropSizeValueLabel.setText(QCoreApplication.translate("MainWindow", u"10", None))
#if QT_CONFIG(tooltip)
        self.facedetailerDropSizeSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc791\uc740 \uc5bc\uad74 \ubb34\uc2dc \uae30\uc900\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 10 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerGuideSizeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74\uc744 \ubd84\uc11d\ud560 \ud574\uc0c1\ub3c4\uc785\ub2c8\ub2e4. \ud45c\uc2dc \uac12 \uae30\uc900 \uae30\ubcf8 256 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerGuideSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Guide Size (\uc5bc\uad74 \ubd84\uc11d \ud06c\uae30)", None))
        self.facedetailerGuideSizeValueLabel.setText(QCoreApplication.translate("MainWindow", u"256", None))
#if QT_CONFIG(tooltip)
        self.facedetailerGuideSizeSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ubd84\uc11d \ud06c\uae30\uc785\ub2c8\ub2e4. \ud45c\uc2dc \uac12 \uae30\uc900 \uae30\ubcf8 256 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerMaxSizeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\ud55c \ubc88\uc5d0 \uace0\uce60 \uc218 \uc788\ub294 \ucd5c\ub300 \ud06c\uae30\uc785\ub2c8\ub2e4. \ud45c\uc2dc \uac12 \uae30\uc900 \uae30\ubcf8 768 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerMaxSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Max Size (\ubcf4\uc815 \ucd5c\ub300 \ud06c\uae30)", None))
        self.facedetailerMaxSizeValueLabel.setText(QCoreApplication.translate("MainWindow", u"768", None))
#if QT_CONFIG(tooltip)
        self.facedetailerMaxSizeSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\ubcf4\uc815 \ucd5c\ub300 \ud06c\uae30\uc785\ub2c8\ub2e4. \ud45c\uc2dc \uac12 \uae30\uc900 \uae30\ubcf8 768 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerCycleLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\ubcf4\uc815\uc744 \uba87 \ubc88 \ubc18\ubcf5\ud560\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8\uac12 1 \ucd94\ucc9c. 2 \uc774\uc0c1\uc740 \uc5bc\uad74\uc774 \ubcc0\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerCycleLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle (\ubcf4\uc815 \ubc18\ubcf5 \ud69f\uc218)", None))
        self.facedetailerCycleValueLabel.setText(QCoreApplication.translate("MainWindow", u"1", None))
#if QT_CONFIG(tooltip)
        self.facedetailerCycleSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\ubcf4\uc815 \ubc18\ubcf5 \ud69f\uc218\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 1 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerBboxThresholdLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74\uc744 \ucc3e\ub294 \ubbfc\uac10\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8 0.50 \ucd94\ucc9c. \uc5bc\uad74\uc744 \ubabb \ucc3e\uc73c\uba74 \ub0ae\ucd94\uc138\uc694.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerBboxThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"BBox Thresh (\uc5bc\uad74 \ucc3e\uae30 \ubbfc\uac10\ub3c4)", None))
        self.facedetailerBboxThresholdValueLabel.setText(QCoreApplication.translate("MainWindow", u"0.50", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxThresholdSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ucc3e\uae30 \ubbfc\uac10\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8 0.50 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerBboxDilationLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\ucc3e\uc740 \uc5bc\uad74 \uc0c1\uc790(\ubc15\uc2a4)\ub97c \uc5bc\ub9c8\ub098 \ub113\ud790\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8\uac12 10 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerBboxDilationLabel.setText(QCoreApplication.translate("MainWindow", u"BBox Dilate (\uc5bc\uad74 \ubc15\uc2a4 \ub113\ud788\uae30)", None))
        self.facedetailerBboxDilationValueLabel.setText(QCoreApplication.translate("MainWindow", u"10", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxDilationSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ubc15\uc2a4 \ub113\ud788\uae30\uc785\ub2c8\ub2e4. \uae30\ubcf8\uac12 10 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerBboxCropFactorLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc8fc\ubcc0\uc744 \uc5bc\ub9c8\ub098 \ud568\uaed8 \ubcfc\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8 1.50 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerBboxCropFactorLabel.setText(QCoreApplication.translate("MainWindow", u"Crop Factor (\uc5bc\uad74 \uc8fc\ubcc0 \uac19\uc774 \ubcf4\uae30)", None))
        self.facedetailerBboxCropFactorValueLabel.setText(QCoreApplication.translate("MainWindow", u"1.50", None))
#if QT_CONFIG(tooltip)
        self.facedetailerBboxCropFactorSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc8fc\ubcc0 \uac19\uc774 \ubcf4\uae30\uc785\ub2c8\ub2e4. \uae30\ubcf8 1.50 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerSamThresholdLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc724\uacfd\uc120(\ub9c8\uc2a4\ud06c) \uc815\ubc00\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8 0.93 \ucd94\ucc9c. \uc9c0\uae08\uc740 SAM \ubbf8\uc0ac\uc6a9\uc73c\ub85c \ubd80\ubd84\ub9cc \uc801\uc6a9\ub429\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"SAM Thresh (\uc724\uacfd\uc120 \uc815\ubc00\ub3c4)", None))
        self.facedetailerSamThresholdValueLabel.setText(QCoreApplication.translate("MainWindow", u"0.93", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamThresholdSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc724\uacfd\uc120 \uc815\ubc00\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8 0.93 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerSamDilationLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc724\uacfd\uc120(\ub9c8\uc2a4\ud06c)\uc744 \ub113\ud790\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8 0 \ucd94\ucc9c. SAM \ubbf8\uc124\uc815 \uc2dc \uc77c\ubd80\ub9cc \uc801\uc6a9\ub429\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamDilationLabel.setText(QCoreApplication.translate("MainWindow", u"SAM Dilate (\uc724\uacfd\uc120 \ub113\ud788\uae30)", None))
        self.facedetailerSamDilationValueLabel.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamDilationSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc724\uacfd\uc120 \ub113\ud788\uae30\uc785\ub2c8\ub2e4. \uae30\ubcf8 0 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerSamBboxExpansionLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc724\uacfd\uc120(\ub9c8\uc2a4\ud06c) \uc601\uc5ed\uc744 \ub113\ud790\uc9c0 \uc815\ud569\ub2c8\ub2e4. \uae30\ubcf8 0 \ucd94\ucc9c. SAM \ubbf8\uc124\uc815 \uc2dc \uc77c\ubd80\ub9cc \uc801\uc6a9\ub429\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamBboxExpansionLabel.setText(QCoreApplication.translate("MainWindow", u"SAM BBox Exp (\uc724\uacfd\uc120 \uc601\uc5ed \ub113\ud788\uae30)", None))
        self.facedetailerSamBboxExpansionValueLabel.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamBboxExpansionSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\uc724\uacfd\uc120 \uc601\uc5ed \ub113\ud788\uae30\uc785\ub2c8\ub2e4. \uae30\ubcf8 0 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintThresholdLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\ub9c8\uc2a4\ud06c \ud78c\ud2b8\ub97c \uc801\uc6a9\ud560\uc9c0 \ud310\uc815\ud558\ub294 \ubbfc\uac10\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8 0.70 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"Mask Hint Thresh (\ud78c\ud2b8 \ubbfc\uac10\ub3c4)", None))
        self.facedetailerSamMaskHintThresholdValueLabel.setText(QCoreApplication.translate("MainWindow", u"0.70", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintThresholdSlider.setToolTip(QCoreApplication.translate("MainWindow", u"\ud78c\ud2b8 \ubbfc\uac10\ub3c4\uc785\ub2c8\ub2e4. \uae30\ubcf8 0.70 \ucd94\ucc9c.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerSamDetectionHintLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74\uc744 \uc7a1\uc744 \uae30\uc900 \uc704\uce58\ub97c \uace0\ub985\ub2c8\ub2e4. center-1\uc774 \uae30\ubcf8\uc774\uace0 \uac00\uc7a5 \uc548\uc804\ud569\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamDetectionHintLabel.setText(QCoreApplication.translate("MainWindow", u"SAM Hint (\uc5bc\uad74 \uc704\uce58 \ud78c\ud2b8)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamDetectionHintComboBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc704\uce58 \ud78c\ud2b8: center-1(\uac00\uc6b4\ub370 1\uc810, \uae30\ubcf8), horizontal-2/vertical-2(2\uc810), rect-4/diamond-4(4\uc810), mask-area/mask-points/mask-point-bbox(\ub9c8\uc2a4\ud06c \uae30\uc900, \uace0\uae09), none(\ud78c\ud2b8 \uc5c6\uc74c).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintUseNegativeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\ubc18\ub300 \uc601\uc5ed(\ub9c8\uc2a4\ud06c \ubc14\uae65)\ub3c4 \uc4f8\uc9c0 \uc815\ud569\ub2c8\ub2e4. False\uac00 \uae30\ubcf8\uc774\uace0 \uac00\uc7a5 \uc548\uc804\ud569\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintUseNegativeLabel.setText(QCoreApplication.translate("MainWindow", u"Mask Hint Neg (\ubc18\ub300\uc601\uc5ed \uc81c\uc678)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerSamMaskHintUseNegativeComboBox.setToolTip(QCoreApplication.translate("MainWindow", u"\ubc18\ub300 \uc601\uc5ed(\ub9c8\uc2a4\ud06c \ubc14\uae65) \uc0ac\uc6a9 \uc5ec\ubd80. False(\uae30\ubcf8, \uc548\uc804)\ub97c \ucd94\ucc9c\ud569\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.openOutputFolderButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c1 \U0000d3f4\U0000b354 \U0000c5f4\U0000ae30", None))
        self.chatInputEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\uba54\uc2dc\uc9c0\ub97c \uc785\ub825\ud558\uc138\uc694... \uc608: \uc774\uc058\uace0 \uadc0\uc5ec\uc6b4 \uace0\uc591\uc774 3\ub9c8\ub9ac \uadf8\ub824\uc918", None))
#if QT_CONFIG(tooltip)
        self.sendBtn.setToolTip(QCoreApplication.translate("MainWindow", u"\uc774\ubbf8\uc9c0 \uc0dd\uc131\ud558\uae30 (P2\uc5d0\uc11c \uc5f0\uacb0)", None))
#endif // QT_CONFIG(tooltip)
        self.sendBtn.setText(QCoreApplication.translate("MainWindow", u"\u27a4", None))
    # retranslateUi

