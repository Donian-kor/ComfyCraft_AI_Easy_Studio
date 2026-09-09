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
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPlainTextEdit, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QTextBrowser, QVBoxLayout,
    QWidget)

from app.gui.play_stop_button import PlayStopButton

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1360, 975)
        MainWindow.setMinimumSize(QSize(1100, 760))
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.mainVerticalLayout = QVBoxLayout(self.centralWidget)
        self.mainVerticalLayout.setSpacing(8)
        self.mainVerticalLayout.setObjectName(u"mainVerticalLayout")
        self.mainVerticalLayout.setContentsMargins(16, 10, 16, 10)
        self.headerFrame = QFrame(self.centralWidget)
        self.headerFrame.setObjectName(u"headerFrame")
        self.headerFrame.setMinimumSize(QSize(0, 50))
        self.headerFrame.setMaximumSize(QSize(16777215, 50))
        self.headerFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.headerLayout = QHBoxLayout(self.headerFrame)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(12, 4, 12, 4)
        self.appTitle = QLabel(self.headerFrame)
        self.appTitle.setObjectName(u"appTitle")

        self.headerLayout.addWidget(self.appTitle)

        self.badgeLabel = QLabel(self.headerFrame)
        self.badgeLabel.setObjectName(u"badgeLabel")

        self.headerLayout.addWidget(self.badgeLabel)

        self.headerDivider = QFrame(self.headerFrame)
        self.headerDivider.setObjectName(u"headerDivider")
        self.headerDivider.setFrameShape(QFrame.Shape.VLine)

        self.headerLayout.addWidget(self.headerDivider)

        self.comfyStatusBtn = QPushButton(self.headerFrame)
        self.comfyStatusBtn.setObjectName(u"comfyStatusBtn")
        self.comfyStatusBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.headerLayout.addWidget(self.comfyStatusBtn)

        self.lmStatusBtn = QPushButton(self.headerFrame)
        self.lmStatusBtn.setObjectName(u"lmStatusBtn")
        self.lmStatusBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.headerLayout.addWidget(self.lmStatusBtn)

        self.headerSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)

        self.themeComboBox = QComboBox(self.headerFrame)
        self.themeComboBox.setObjectName(u"themeComboBox")
        self.themeComboBox.setMinimumSize(QSize(170, 30))

        self.headerLayout.addWidget(self.themeComboBox)

        self.helpButton = QPushButton(self.headerFrame)
        self.helpButton.setObjectName(u"helpButton")
        self.helpButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.headerLayout.addWidget(self.helpButton)

        self.settingsButton = QPushButton(self.headerFrame)
        self.settingsButton.setObjectName(u"settingsButton")
        self.settingsButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.headerLayout.addWidget(self.settingsButton)


        self.mainVerticalLayout.addWidget(self.headerFrame)

        self.studioContainer = QFrame(self.centralWidget)
        self.studioContainer.setObjectName(u"studioContainer")
        self.studioContainer.setFrameShape(QFrame.Shape.NoFrame)
        self.studioLayout = QHBoxLayout(self.studioContainer)
        self.studioLayout.setSpacing(16)
        self.studioLayout.setObjectName(u"studioLayout")
        self.studioLayout.setContentsMargins(0, 0, 0, 0)
        self.leftScrollArea = QScrollArea(self.studioContainer)
        self.leftScrollArea.setObjectName(u"leftScrollArea")
        self.leftScrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.leftScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.leftScrollArea.setWidgetResizable(True)
        self.leftContentWidget = QWidget()
        self.leftContentWidget.setObjectName(u"leftContentWidget")
        self.leftContentWidget.setGeometry(QRect(0, 0, 708, 1488))
        self.leftContentLayout = QVBoxLayout(self.leftContentWidget)
        self.leftContentLayout.setSpacing(14)
        self.leftContentLayout.setObjectName(u"leftContentLayout")
        self.leftContentLayout.setContentsMargins(4, 0, 8, 4)
        self.step1Card = QFrame(self.leftContentWidget)
        self.step1Card.setObjectName(u"step1Card")
        self.step1Card.setFrameShape(QFrame.Shape.StyledPanel)
        self.step1Layout = QVBoxLayout(self.step1Card)
        self.step1Layout.setSpacing(10)
        self.step1Layout.setObjectName(u"step1Layout")
        self.step1Layout.setContentsMargins(14, 14, 14, 14)
        self.step1HeaderLayout = QHBoxLayout()
        self.step1HeaderLayout.setObjectName(u"step1HeaderLayout")
        self.step1Badge = QLabel(self.step1Card)
        self.step1Badge.setObjectName(u"step1Badge")
        self.step1Badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.step1HeaderLayout.addWidget(self.step1Badge)

        self.step1Title = QLabel(self.step1Card)
        self.step1Title.setObjectName(u"step1Title")

        self.step1HeaderLayout.addWidget(self.step1Title)

        self.step1Spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.step1HeaderLayout.addItem(self.step1Spacer)

        self.positivePromptCounterLabel = QLabel(self.step1Card)
        self.positivePromptCounterLabel.setObjectName(u"positivePromptCounterLabel")

        self.step1HeaderLayout.addWidget(self.positivePromptCounterLabel)


        self.step1Layout.addLayout(self.step1HeaderLayout)

        self.lmModelSelectLayout = QVBoxLayout()
        self.lmModelSelectLayout.setSpacing(4)
        self.lmModelSelectLayout.setObjectName(u"lmModelSelectLayout")
        self.lmModelSelectLabel = QLabel(self.step1Card)
        self.lmModelSelectLabel.setObjectName(u"lmModelSelectLabel")

        self.lmModelSelectLayout.addWidget(self.lmModelSelectLabel)

        self.lmModelCombo = QComboBox(self.step1Card)
        self.lmModelCombo.setObjectName(u"lmModelCombo")
        self.lmModelCombo.setMinimumSize(QSize(0, 34))

        self.lmModelSelectLayout.addWidget(self.lmModelCombo)


        self.step1Layout.addLayout(self.lmModelSelectLayout)

        self.positivePromptEdit = QPlainTextEdit(self.step1Card)
        self.positivePromptEdit.setObjectName(u"positivePromptEdit")
        self.positivePromptEdit.setMinimumSize(QSize(0, 76))

        self.step1Layout.addWidget(self.positivePromptEdit)

        self.enhancePromptButton = QPushButton(self.step1Card)
        self.enhancePromptButton.setObjectName(u"enhancePromptButton")
        self.enhancePromptButton.setMinimumSize(QSize(0, 38))
        self.enhancePromptButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.step1Layout.addWidget(self.enhancePromptButton)

        self.enhancePromptCard = QFrame(self.step1Card)
        self.enhancePromptCard.setObjectName(u"enhancePromptCard")
        self.enhanceCardLayout = QVBoxLayout(self.enhancePromptCard)
        self.enhanceCardLayout.setSpacing(6)
        self.enhanceCardLayout.setObjectName(u"enhanceCardLayout")
        self.enhanceCardLayout.setContentsMargins(10, 10, 10, 10)
        self.enhanceCardHeader = QHBoxLayout()
        self.enhanceCardHeader.setObjectName(u"enhanceCardHeader")
        self.enhancePromptLabel = QLabel(self.enhancePromptCard)
        self.enhancePromptLabel.setObjectName(u"enhancePromptLabel")

        self.enhanceCardHeader.addWidget(self.enhancePromptLabel)

        self.enhanceSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.enhanceCardHeader.addItem(self.enhanceSpacer)

        self.enhancePromptCounterLabel = QLabel(self.enhancePromptCard)
        self.enhancePromptCounterLabel.setObjectName(u"enhancePromptCounterLabel")

        self.enhanceCardHeader.addWidget(self.enhancePromptCounterLabel)

        self.copyPromptButton = QPushButton(self.enhancePromptCard)
        self.copyPromptButton.setObjectName(u"copyPromptButton")
        self.copyPromptButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.enhanceCardHeader.addWidget(self.copyPromptButton)


        self.enhanceCardLayout.addLayout(self.enhanceCardHeader)

        self.enhancePromptEdit = QPlainTextEdit(self.enhancePromptCard)
        self.enhancePromptEdit.setObjectName(u"enhancePromptEdit")
        self.enhancePromptEdit.setMinimumSize(QSize(0, 68))

        self.enhanceCardLayout.addWidget(self.enhancePromptEdit)


        self.step1Layout.addWidget(self.enhancePromptCard)

        self.negativePromptFrame = QFrame(self.step1Card)
        self.negativePromptFrame.setObjectName(u"negativePromptFrame")
        self.negativePromptFrame.setVisible(False)
        self.negLayout = QVBoxLayout(self.negativePromptFrame)
        self.negLayout.setSpacing(4)
        self.negLayout.setObjectName(u"negLayout")
        self.negLayout.setContentsMargins(0, 4, 0, 0)
        self.negHeaderLayout = QHBoxLayout()
        self.negHeaderLayout.setObjectName(u"negHeaderLayout")
        self.negTitleLabel = QLabel(self.negativePromptFrame)
        self.negTitleLabel.setObjectName(u"negTitleLabel")

        self.negHeaderLayout.addWidget(self.negTitleLabel)

        self.negSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.negHeaderLayout.addItem(self.negSpacer)

        self.negativePromptCounterLabel = QLabel(self.negativePromptFrame)
        self.negativePromptCounterLabel.setObjectName(u"negativePromptCounterLabel")

        self.negHeaderLayout.addWidget(self.negativePromptCounterLabel)


        self.negLayout.addLayout(self.negHeaderLayout)

        self.negativePromptEdit = QPlainTextEdit(self.negativePromptFrame)
        self.negativePromptEdit.setObjectName(u"negativePromptEdit")
        self.negativePromptEdit.setMinimumSize(QSize(0, 54))

        self.negLayout.addWidget(self.negativePromptEdit)


        self.step1Layout.addWidget(self.negativePromptFrame)


        self.leftContentLayout.addWidget(self.step1Card)

        self.step2Card = QFrame(self.leftContentWidget)
        self.step2Card.setObjectName(u"step2Card")
        self.step2Card.setFrameShape(QFrame.Shape.StyledPanel)
        self.step2Layout = QVBoxLayout(self.step2Card)
        self.step2Layout.setSpacing(12)
        self.step2Layout.setObjectName(u"step2Layout")
        self.step2Layout.setContentsMargins(14, 14, 14, 14)
        self.step2HeaderLayout = QHBoxLayout()
        self.step2HeaderLayout.setObjectName(u"step2HeaderLayout")
        self.step2Badge = QLabel(self.step2Card)
        self.step2Badge.setObjectName(u"step2Badge")
        self.step2Badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.step2HeaderLayout.addWidget(self.step2Badge)

        self.step2Title = QLabel(self.step2Card)
        self.step2Title.setObjectName(u"step2Title")

        self.step2HeaderLayout.addWidget(self.step2Title)

        self.step2Spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.step2HeaderLayout.addItem(self.step2Spacer)

        self.modelProfileNoticeLabel = QLabel(self.step2Card)
        self.modelProfileNoticeLabel.setObjectName(u"modelProfileNoticeLabel")

        self.step2HeaderLayout.addWidget(self.modelProfileNoticeLabel)


        self.step2Layout.addLayout(self.step2HeaderLayout)

        self.modelSelectLayout = QVBoxLayout()
        self.modelSelectLayout.setSpacing(4)
        self.modelSelectLayout.setObjectName(u"modelSelectLayout")
        self.modelSelectLabel = QLabel(self.step2Card)
        self.modelSelectLabel.setObjectName(u"modelSelectLabel")

        self.modelSelectLayout.addWidget(self.modelSelectLabel)

        self.comfyModelCombo = QComboBox(self.step2Card)
        self.comfyModelCombo.setObjectName(u"comfyModelCombo")
        self.comfyModelCombo.setMinimumSize(QSize(0, 34))

        self.modelSelectLayout.addWidget(self.comfyModelCombo)


        self.step2Layout.addLayout(self.modelSelectLayout)

        self.aspectRatioLayout = QVBoxLayout()
        self.aspectRatioLayout.setSpacing(6)
        self.aspectRatioLayout.setObjectName(u"aspectRatioLayout")
        self.aspectRatioTitle = QLabel(self.step2Card)
        self.aspectRatioTitle.setObjectName(u"aspectRatioTitle")

        self.aspectRatioLayout.addWidget(self.aspectRatioTitle)

        self.presetsButtonLayout = QHBoxLayout()
        self.presetsButtonLayout.setSpacing(8)
        self.presetsButtonLayout.setObjectName(u"presetsButtonLayout")
        self.preset_1024x1024 = QPushButton(self.step2Card)
        self.preset_1024x1024.setObjectName(u"preset_1024x1024")
        self.preset_1024x1024.setMinimumSize(QSize(0, 48))
        self.preset_1024x1024.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.presetsButtonLayout.addWidget(self.preset_1024x1024)

        self.preset_896x1152 = QPushButton(self.step2Card)
        self.preset_896x1152.setObjectName(u"preset_896x1152")
        self.preset_896x1152.setMinimumSize(QSize(0, 48))
        self.preset_896x1152.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.presetsButtonLayout.addWidget(self.preset_896x1152)

        self.preset_1152x896 = QPushButton(self.step2Card)
        self.preset_1152x896.setObjectName(u"preset_1152x896")
        self.preset_1152x896.setMinimumSize(QSize(0, 48))
        self.preset_1152x896.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.presetsButtonLayout.addWidget(self.preset_1152x896)


        self.aspectRatioLayout.addLayout(self.presetsButtonLayout)


        self.step2Layout.addLayout(self.aspectRatioLayout)

        self.dimensionContainer = QWidget(self.step2Card)
        self.dimensionContainer.setObjectName(u"dimensionContainer")
        self.dimensionLayout = QHBoxLayout(self.dimensionContainer)
        self.dimensionLayout.setObjectName(u"dimensionLayout")
        self.dimensionLayout.setContentsMargins(0, 0, 0, 0)
        self.widthLabel = QLabel(self.dimensionContainer)
        self.widthLabel.setObjectName(u"widthLabel")

        self.dimensionLayout.addWidget(self.widthLabel)

        self.widthSpinBox = QSpinBox(self.dimensionContainer)
        self.widthSpinBox.setObjectName(u"widthSpinBox")
        self.widthSpinBox.setMinimumSize(QSize(75, 28))

        self.dimensionLayout.addWidget(self.widthSpinBox)

        self.heightLabel = QLabel(self.dimensionContainer)
        self.heightLabel.setObjectName(u"heightLabel")

        self.dimensionLayout.addWidget(self.heightLabel)

        self.heightSpinBox = QSpinBox(self.dimensionContainer)
        self.heightSpinBox.setObjectName(u"heightSpinBox")
        self.heightSpinBox.setMinimumSize(QSize(75, 28))

        self.dimensionLayout.addWidget(self.heightSpinBox)

        self.dimSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.dimensionLayout.addItem(self.dimSpacer)


        self.step2Layout.addWidget(self.dimensionContainer)

        self.faceDetailerCard = QFrame(self.step2Card)
        self.faceDetailerCard.setObjectName(u"faceDetailerCard")
        self.faceDetailerCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.faceDetailerLayout = QVBoxLayout(self.faceDetailerCard)
        self.faceDetailerLayout.setSpacing(8)
        self.faceDetailerLayout.setObjectName(u"faceDetailerLayout")
        self.faceDetailerLayout.setContentsMargins(12, 10, 12, 10)
        self.facedetailerCheckBox = QCheckBox(self.faceDetailerCard)
        self.facedetailerCheckBox.setObjectName(u"facedetailerCheckBox")
        self.facedetailerCheckBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.faceDetailerLayout.addWidget(self.facedetailerCheckBox)

        self.facedetailerPanel = QFrame(self.faceDetailerCard)
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

        self.facedetailerDenoiseSpinBox = QDoubleSpinBox(self.facedetailerPanel)
        self.facedetailerDenoiseSpinBox.setObjectName(u"facedetailerDenoiseSpinBox")
        self.facedetailerDenoiseSpinBox.setMinimumSize(QSize(60, 22))
        self.facedetailerDenoiseSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerDenoiseSpinBox.setMinimum(0.000000000000000)
        self.facedetailerDenoiseSpinBox.setMaximum(1.000000000000000)
        self.facedetailerDenoiseSpinBox.setSingleStep(0.010000000000000)
        self.facedetailerDenoiseSpinBox.setValue(0.400000000000000)

        self.fd_denoise_hdr.addWidget(self.facedetailerDenoiseSpinBox)


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

        self.facedetailerStepsSpinBox = QSpinBox(self.facedetailerPanel)
        self.facedetailerStepsSpinBox.setObjectName(u"facedetailerStepsSpinBox")
        self.facedetailerStepsSpinBox.setMinimumSize(QSize(60, 22))
        self.facedetailerStepsSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerStepsSpinBox.setMinimum(1)
        self.facedetailerStepsSpinBox.setMaximum(50)
        self.facedetailerStepsSpinBox.setValue(20)

        self.fd_steps_hdr.addWidget(self.facedetailerStepsSpinBox)


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

        self.facedetailerCfgSpinBox = QDoubleSpinBox(self.facedetailerPanel)
        self.facedetailerCfgSpinBox.setObjectName(u"facedetailerCfgSpinBox")
        self.facedetailerCfgSpinBox.setMinimumSize(QSize(60, 22))
        self.facedetailerCfgSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerCfgSpinBox.setMinimum(0.000000000000000)
        self.facedetailerCfgSpinBox.setMaximum(20.000000000000000)
        self.facedetailerCfgSpinBox.setSingleStep(0.100000000000000)
        self.facedetailerCfgSpinBox.setValue(4.000000000000000)

        self.fd_cfg_hdr.addWidget(self.facedetailerCfgSpinBox)


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

        self.facedetailerFeatherSpinBox = QSpinBox(self.facedetailerPanel)
        self.facedetailerFeatherSpinBox.setObjectName(u"facedetailerFeatherSpinBox")
        self.facedetailerFeatherSpinBox.setMinimumSize(QSize(60, 22))
        self.facedetailerFeatherSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerFeatherSpinBox.setMinimum(0)
        self.facedetailerFeatherSpinBox.setMaximum(20)
        self.facedetailerFeatherSpinBox.setValue(5)

        self.fd_feather_hdr.addWidget(self.facedetailerFeatherSpinBox)


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

        self.facedetailerDropSizeSpinBox = QSpinBox(self.facedetailerPanel)
        self.facedetailerDropSizeSpinBox.setObjectName(u"facedetailerDropSizeSpinBox")
        self.facedetailerDropSizeSpinBox.setMinimumSize(QSize(60, 22))
        self.facedetailerDropSizeSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerDropSizeSpinBox.setMinimum(1)
        self.facedetailerDropSizeSpinBox.setMaximum(100)
        self.facedetailerDropSizeSpinBox.setValue(10)

        self.fd_dropsize_hdr.addWidget(self.facedetailerDropSizeSpinBox)


        self.fd_dropsize_vbox.addLayout(self.fd_dropsize_hdr)

        self.facedetailerDropSizeSlider = QSlider(self.facedetailerPanel)
        self.facedetailerDropSizeSlider.setObjectName(u"facedetailerDropSizeSlider")
        self.facedetailerDropSizeSlider.setMinimum(1)
        self.facedetailerDropSizeSlider.setMaximum(100)
        self.facedetailerDropSizeSlider.setValue(10)
        self.facedetailerDropSizeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.fd_dropsize_vbox.addWidget(self.facedetailerDropSizeSlider)


        self.fdLeftCol.addLayout(self.fd_dropsize_vbox)

        self.fd_guidesize_row = QHBoxLayout()
        self.fd_guidesize_row.setObjectName(u"fd_guidesize_row")
        self.facedetailerGuideSizeLabel = QLabel(self.facedetailerPanel)
        self.facedetailerGuideSizeLabel.setObjectName(u"facedetailerGuideSizeLabel")

        self.fd_guidesize_row.addWidget(self.facedetailerGuideSizeLabel)

        self.spacerItem5 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_guidesize_row.addItem(self.spacerItem5)

        self.facedetailerGuideSizeSpinBox = QSpinBox(self.facedetailerPanel)
        self.facedetailerGuideSizeSpinBox.setObjectName(u"facedetailerGuideSizeSpinBox")
        self.facedetailerGuideSizeSpinBox.setMinimumSize(QSize(75, 24))
        self.facedetailerGuideSizeSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerGuideSizeSpinBox.setMinimum(64)
        self.facedetailerGuideSizeSpinBox.setMaximum(1024)
        self.facedetailerGuideSizeSpinBox.setSingleStep(64)
        self.facedetailerGuideSizeSpinBox.setValue(256)

        self.fd_guidesize_row.addWidget(self.facedetailerGuideSizeSpinBox)


        self.fdLeftCol.addLayout(self.fd_guidesize_row)

        self.fd_maxsize_row = QHBoxLayout()
        self.fd_maxsize_row.setObjectName(u"fd_maxsize_row")
        self.facedetailerMaxSizeLabel = QLabel(self.facedetailerPanel)
        self.facedetailerMaxSizeLabel.setObjectName(u"facedetailerMaxSizeLabel")

        self.fd_maxsize_row.addWidget(self.facedetailerMaxSizeLabel)

        self.spacerItem6 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_maxsize_row.addItem(self.spacerItem6)

        self.facedetailerMaxSizeSpinBox = QSpinBox(self.facedetailerPanel)
        self.facedetailerMaxSizeSpinBox.setObjectName(u"facedetailerMaxSizeSpinBox")
        self.facedetailerMaxSizeSpinBox.setMinimumSize(QSize(75, 24))
        self.facedetailerMaxSizeSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerMaxSizeSpinBox.setMinimum(128)
        self.facedetailerMaxSizeSpinBox.setMaximum(2048)
        self.facedetailerMaxSizeSpinBox.setSingleStep(64)
        self.facedetailerMaxSizeSpinBox.setValue(768)

        self.fd_maxsize_row.addWidget(self.facedetailerMaxSizeSpinBox)


        self.fdLeftCol.addLayout(self.fd_maxsize_row)

        self.fd_cycle_row = QHBoxLayout()
        self.fd_cycle_row.setObjectName(u"fd_cycle_row")
        self.facedetailerCycleLabel = QLabel(self.facedetailerPanel)
        self.facedetailerCycleLabel.setObjectName(u"facedetailerCycleLabel")

        self.fd_cycle_row.addWidget(self.facedetailerCycleLabel)

        self.spacerItem7 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fd_cycle_row.addItem(self.spacerItem7)

        self.facedetailerCycleSpinBox = QSpinBox(self.facedetailerPanel)
        self.facedetailerCycleSpinBox.setObjectName(u"facedetailerCycleSpinBox")
        self.facedetailerCycleSpinBox.setMinimumSize(QSize(75, 24))
        self.facedetailerCycleSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerCycleSpinBox.setMinimum(1)
        self.facedetailerCycleSpinBox.setMaximum(10)
        self.facedetailerCycleSpinBox.setValue(1)

        self.fd_cycle_row.addWidget(self.facedetailerCycleSpinBox)


        self.fdLeftCol.addLayout(self.fd_cycle_row)

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

        self.facedetailerBboxThresholdSpinBox = QDoubleSpinBox(self.facedetailerPanel)
        self.facedetailerBboxThresholdSpinBox.setObjectName(u"facedetailerBboxThresholdSpinBox")
        self.facedetailerBboxThresholdSpinBox.setMinimumSize(QSize(60, 22))
        self.facedetailerBboxThresholdSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerBboxThresholdSpinBox.setMinimum(0.100000000000000)
        self.facedetailerBboxThresholdSpinBox.setMaximum(1.000000000000000)
        self.facedetailerBboxThresholdSpinBox.setSingleStep(0.010000000000000)
        self.facedetailerBboxThresholdSpinBox.setValue(0.500000000000000)

        self.fd_bboxthresh_hdr.addWidget(self.facedetailerBboxThresholdSpinBox)


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

        self.facedetailerBboxDilationSpinBox = QSpinBox(self.facedetailerPanel)
        self.facedetailerBboxDilationSpinBox.setObjectName(u"facedetailerBboxDilationSpinBox")
        self.facedetailerBboxDilationSpinBox.setMinimumSize(QSize(60, 22))
        self.facedetailerBboxDilationSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerBboxDilationSpinBox.setMinimum(-20)
        self.facedetailerBboxDilationSpinBox.setMaximum(100)
        self.facedetailerBboxDilationSpinBox.setValue(10)

        self.fd_bboxdilate_hdr.addWidget(self.facedetailerBboxDilationSpinBox)


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

        self.facedetailerBboxCropFactorSpinBox = QDoubleSpinBox(self.facedetailerPanel)
        self.facedetailerBboxCropFactorSpinBox.setObjectName(u"facedetailerBboxCropFactorSpinBox")
        self.facedetailerBboxCropFactorSpinBox.setMinimumSize(QSize(60, 22))
        self.facedetailerBboxCropFactorSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerBboxCropFactorSpinBox.setMinimum(1.000000000000000)
        self.facedetailerBboxCropFactorSpinBox.setMaximum(5.000000000000000)
        self.facedetailerBboxCropFactorSpinBox.setSingleStep(0.050000000000000)
        self.facedetailerBboxCropFactorSpinBox.setValue(1.500000000000000)

        self.fd_cropfactor_hdr.addWidget(self.facedetailerBboxCropFactorSpinBox)


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

        self.facedetailerSamThresholdSpinBox = QDoubleSpinBox(self.facedetailerPanel)
        self.facedetailerSamThresholdSpinBox.setObjectName(u"facedetailerSamThresholdSpinBox")
        self.facedetailerSamThresholdSpinBox.setMinimumSize(QSize(60, 22))
        self.facedetailerSamThresholdSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerSamThresholdSpinBox.setMinimum(0.100000000000000)
        self.facedetailerSamThresholdSpinBox.setMaximum(1.000000000000000)
        self.facedetailerSamThresholdSpinBox.setSingleStep(0.010000000000000)
        self.facedetailerSamThresholdSpinBox.setValue(0.930000000000000)

        self.fd_samthresh_hdr.addWidget(self.facedetailerSamThresholdSpinBox)


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

        self.facedetailerSamDilationSpinBox = QSpinBox(self.facedetailerPanel)
        self.facedetailerSamDilationSpinBox.setObjectName(u"facedetailerSamDilationSpinBox")
        self.facedetailerSamDilationSpinBox.setMinimumSize(QSize(60, 22))
        self.facedetailerSamDilationSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerSamDilationSpinBox.setMinimum(0)
        self.facedetailerSamDilationSpinBox.setMaximum(100)
        self.facedetailerSamDilationSpinBox.setValue(0)

        self.fd_samdilate_hdr.addWidget(self.facedetailerSamDilationSpinBox)


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

        self.facedetailerSamBboxExpansionSpinBox = QSpinBox(self.facedetailerPanel)
        self.facedetailerSamBboxExpansionSpinBox.setObjectName(u"facedetailerSamBboxExpansionSpinBox")
        self.facedetailerSamBboxExpansionSpinBox.setMinimumSize(QSize(60, 22))
        self.facedetailerSamBboxExpansionSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerSamBboxExpansionSpinBox.setMinimum(0)
        self.facedetailerSamBboxExpansionSpinBox.setMaximum(100)
        self.facedetailerSamBboxExpansionSpinBox.setValue(0)

        self.fd_sambboxexp_hdr.addWidget(self.facedetailerSamBboxExpansionSpinBox)


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

        self.facedetailerSamMaskHintThresholdSpinBox = QDoubleSpinBox(self.facedetailerPanel)
        self.facedetailerSamMaskHintThresholdSpinBox.setObjectName(u"facedetailerSamMaskHintThresholdSpinBox")
        self.facedetailerSamMaskHintThresholdSpinBox.setMinimumSize(QSize(60, 22))
        self.facedetailerSamMaskHintThresholdSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.facedetailerSamMaskHintThresholdSpinBox.setMinimum(0.100000000000000)
        self.facedetailerSamMaskHintThresholdSpinBox.setMaximum(1.000000000000000)
        self.facedetailerSamMaskHintThresholdSpinBox.setSingleStep(0.010000000000000)
        self.facedetailerSamMaskHintThresholdSpinBox.setValue(0.700000000000000)

        self.fd_maskhintthresh_hdr.addWidget(self.facedetailerSamMaskHintThresholdSpinBox)


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


        self.faceDetailerLayout.addWidget(self.facedetailerPanel)


        self.step2Layout.addWidget(self.faceDetailerCard)

        self.advancedSettingsFrame = QFrame(self.step2Card)
        self.advancedSettingsFrame.setObjectName(u"advancedSettingsFrame")
        self.advancedLayout = QVBoxLayout(self.advancedSettingsFrame)
        self.advancedLayout.setSpacing(8)
        self.advancedLayout.setObjectName(u"advancedLayout")
        self.advancedLayout.setContentsMargins(10, 10, 10, 10)
        self.advancedToggleBtn = QPushButton(self.advancedSettingsFrame)
        self.advancedToggleBtn.setObjectName(u"advancedToggleBtn")
        self.advancedToggleBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.advancedLayout.addWidget(self.advancedToggleBtn)

        self.advancedContentWidget = QWidget(self.advancedSettingsFrame)
        self.advancedContentWidget.setObjectName(u"advancedContentWidget")
        self.advancedContentLayout = QVBoxLayout(self.advancedContentWidget)
        self.advancedContentLayout.setSpacing(10)
        self.advancedContentLayout.setObjectName(u"advancedContentLayout")
        self.advancedContentLayout.setContentsMargins(0, 6, 0, 0)
        self.seedRowLayout = QHBoxLayout()
        self.seedRowLayout.setSpacing(6)
        self.seedRowLayout.setObjectName(u"seedRowLayout")
        self.seedTitleLabel = QLabel(self.advancedContentWidget)
        self.seedTitleLabel.setObjectName(u"seedTitleLabel")

        self.seedRowLayout.addWidget(self.seedTitleLabel)

        self.seedSpinBox = QSpinBox(self.advancedContentWidget)
        self.seedSpinBox.setObjectName(u"seedSpinBox")
        self.seedSpinBox.setMinimumSize(QSize(120, 28))

        self.seedRowLayout.addWidget(self.seedSpinBox)

        self.randomSeedButton = QPushButton(self.advancedContentWidget)
        self.randomSeedButton.setObjectName(u"randomSeedButton")
        self.randomSeedButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.seedRowLayout.addWidget(self.randomSeedButton)

        self.lockSeedButton = QPushButton(self.advancedContentWidget)
        self.lockSeedButton.setObjectName(u"lockSeedButton")
        self.lockSeedButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.lockSeedButton.setCheckable(True)

        self.seedRowLayout.addWidget(self.lockSeedButton)


        self.advancedContentLayout.addLayout(self.seedRowLayout)

        self.cfgSliderContainer = QVBoxLayout()
        self.cfgSliderContainer.setSpacing(2)
        self.cfgSliderContainer.setObjectName(u"cfgSliderContainer")
        self.cfgHeaderRow = QHBoxLayout()
        self.cfgHeaderRow.setObjectName(u"cfgHeaderRow")
        self.cfgLabelTitle = QLabel(self.advancedContentWidget)
        self.cfgLabelTitle.setObjectName(u"cfgLabelTitle")

        self.cfgHeaderRow.addWidget(self.cfgLabelTitle)

        self.cfgSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.cfgHeaderRow.addItem(self.cfgSpacer)

        self.cfgValueLabel = QLabel(self.advancedContentWidget)
        self.cfgValueLabel.setObjectName(u"cfgValueLabel")

        self.cfgHeaderRow.addWidget(self.cfgValueLabel)


        self.cfgSliderContainer.addLayout(self.cfgHeaderRow)

        self.cfgControlRow = QHBoxLayout()
        self.cfgControlRow.setObjectName(u"cfgControlRow")
        self.cfgSlider = QSlider(self.advancedContentWidget)
        self.cfgSlider.setObjectName(u"cfgSlider")
        self.cfgSlider.setMinimum(10)
        self.cfgSlider.setMaximum(150)
        self.cfgSlider.setValue(35)
        self.cfgSlider.setOrientation(Qt.Orientation.Horizontal)

        self.cfgControlRow.addWidget(self.cfgSlider)

        self.cfgSpinBox = QDoubleSpinBox(self.advancedContentWidget)
        self.cfgSpinBox.setObjectName(u"cfgSpinBox")
        self.cfgSpinBox.setMinimumSize(QSize(65, 24))

        self.cfgControlRow.addWidget(self.cfgSpinBox)


        self.cfgSliderContainer.addLayout(self.cfgControlRow)


        self.advancedContentLayout.addLayout(self.cfgSliderContainer)

        self.stepsSliderContainer = QVBoxLayout()
        self.stepsSliderContainer.setSpacing(2)
        self.stepsSliderContainer.setObjectName(u"stepsSliderContainer")
        self.stepsHeaderRow = QHBoxLayout()
        self.stepsHeaderRow.setObjectName(u"stepsHeaderRow")
        self.stepsLabelTitle = QLabel(self.advancedContentWidget)
        self.stepsLabelTitle.setObjectName(u"stepsLabelTitle")

        self.stepsHeaderRow.addWidget(self.stepsLabelTitle)

        self.stepsSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.stepsHeaderRow.addItem(self.stepsSpacer)

        self.stepsValueLabel = QLabel(self.advancedContentWidget)
        self.stepsValueLabel.setObjectName(u"stepsValueLabel")

        self.stepsHeaderRow.addWidget(self.stepsValueLabel)


        self.stepsSliderContainer.addLayout(self.stepsHeaderRow)

        self.stepsControlRow = QHBoxLayout()
        self.stepsControlRow.setObjectName(u"stepsControlRow")
        self.stepsSlider = QSlider(self.advancedContentWidget)
        self.stepsSlider.setObjectName(u"stepsSlider")
        self.stepsSlider.setMinimum(1)
        self.stepsSlider.setMaximum(50)
        self.stepsSlider.setValue(24)
        self.stepsSlider.setOrientation(Qt.Orientation.Horizontal)

        self.stepsControlRow.addWidget(self.stepsSlider)

        self.stepsSpinBox = QSpinBox(self.advancedContentWidget)
        self.stepsSpinBox.setObjectName(u"stepsSpinBox")
        self.stepsSpinBox.setMinimumSize(QSize(65, 24))

        self.stepsControlRow.addWidget(self.stepsSpinBox)


        self.stepsSliderContainer.addLayout(self.stepsControlRow)


        self.advancedContentLayout.addLayout(self.stepsSliderContainer)

        self.samplerRowLayout = QHBoxLayout()
        self.samplerRowLayout.setSpacing(8)
        self.samplerRowLayout.setObjectName(u"samplerRowLayout")
        self.samplerCol = QVBoxLayout()
        self.samplerCol.setSpacing(2)
        self.samplerCol.setObjectName(u"samplerCol")
        self.samplerLabel = QLabel(self.advancedContentWidget)
        self.samplerLabel.setObjectName(u"samplerLabel")

        self.samplerCol.addWidget(self.samplerLabel)

        self.samplerComboBox = QComboBox(self.advancedContentWidget)
        self.samplerComboBox.setObjectName(u"samplerComboBox")

        self.samplerCol.addWidget(self.samplerComboBox)


        self.samplerRowLayout.addLayout(self.samplerCol)

        self.schedulerCol = QVBoxLayout()
        self.schedulerCol.setSpacing(2)
        self.schedulerCol.setObjectName(u"schedulerCol")
        self.schedulerLabel = QLabel(self.advancedContentWidget)
        self.schedulerLabel.setObjectName(u"schedulerLabel")

        self.schedulerCol.addWidget(self.schedulerLabel)

        self.schedulerComboBox = QComboBox(self.advancedContentWidget)
        self.schedulerComboBox.setObjectName(u"schedulerComboBox")

        self.schedulerCol.addWidget(self.schedulerComboBox)


        self.samplerRowLayout.addLayout(self.schedulerCol)

        self.denoiseCol = QVBoxLayout()
        self.denoiseCol.setSpacing(2)
        self.denoiseCol.setObjectName(u"denoiseCol")
        self.denoiseLabel = QLabel(self.advancedContentWidget)
        self.denoiseLabel.setObjectName(u"denoiseLabel")

        self.denoiseCol.addWidget(self.denoiseLabel)

        self.denoiseSpinBox = QDoubleSpinBox(self.advancedContentWidget)
        self.denoiseSpinBox.setObjectName(u"denoiseSpinBox")

        self.denoiseCol.addWidget(self.denoiseSpinBox)


        self.samplerRowLayout.addLayout(self.denoiseCol)


        self.advancedContentLayout.addLayout(self.samplerRowLayout)


        self.advancedLayout.addWidget(self.advancedContentWidget)


        self.step2Layout.addWidget(self.advancedSettingsFrame)


        self.leftContentLayout.addWidget(self.step2Card)

        self.leftScrollArea.setWidget(self.leftContentWidget)

        self.studioLayout.addWidget(self.leftScrollArea)

        self.rightContainer = QFrame(self.studioContainer)
        self.rightContainer.setObjectName(u"rightContainer")
        self.rightContainer.setFrameShape(QFrame.Shape.NoFrame)
        self.rightLayout = QVBoxLayout(self.rightContainer)
        self.rightLayout.setSpacing(12)
        self.rightLayout.setObjectName(u"rightLayout")
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.viewerCard = QFrame(self.rightContainer)
        self.viewerCard.setObjectName(u"viewerCard")
        self.viewerCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.viewerLayout = QVBoxLayout(self.viewerCard)
        self.viewerLayout.setSpacing(8)
        self.viewerLayout.setObjectName(u"viewerLayout")
        self.viewerLayout.setContentsMargins(14, 14, 14, 14)
        self.viewerHeaderLayout = QHBoxLayout()
        self.viewerHeaderLayout.setObjectName(u"viewerHeaderLayout")
        self.viewerStatusDot = QLabel(self.viewerCard)
        self.viewerStatusDot.setObjectName(u"viewerStatusDot")

        self.viewerHeaderLayout.addWidget(self.viewerStatusDot)

        self.viewerTitle = QLabel(self.viewerCard)
        self.viewerTitle.setObjectName(u"viewerTitle")

        self.viewerHeaderLayout.addWidget(self.viewerTitle)

        self.viewerSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.viewerHeaderLayout.addItem(self.viewerSpacer)

        self.elapsedLabel = QLabel(self.viewerCard)
        self.elapsedLabel.setObjectName(u"elapsedLabel")

        self.viewerHeaderLayout.addWidget(self.elapsedLabel)


        self.viewerLayout.addLayout(self.viewerHeaderLayout)

        self.previewLabel = QLabel(self.viewerCard)
        self.previewLabel.setObjectName(u"previewLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewLabel.sizePolicy().hasHeightForWidth())
        self.previewLabel.setSizePolicy(sizePolicy)
        self.previewLabel.setMinimumSize(QSize(380, 380))
        self.previewLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.viewerLayout.addWidget(self.previewLabel)

        self.progressContainer = QVBoxLayout()
        self.progressContainer.setSpacing(3)
        self.progressContainer.setObjectName(u"progressContainer")
        self.progressTextRow = QHBoxLayout()
        self.progressTextRow.setObjectName(u"progressTextRow")
        self.progressStatusLabel = QLabel(self.viewerCard)
        self.progressStatusLabel.setObjectName(u"progressStatusLabel")

        self.progressTextRow.addWidget(self.progressStatusLabel)

        self.progSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.progressTextRow.addItem(self.progSpacer)

        self.progressPercentLabel = QLabel(self.viewerCard)
        self.progressPercentLabel.setObjectName(u"progressPercentLabel")

        self.progressTextRow.addWidget(self.progressPercentLabel)


        self.progressContainer.addLayout(self.progressTextRow)

        self.progressBar = QProgressBar(self.viewerCard)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(0, 8))
        self.progressBar.setMaximumSize(QSize(16777215, 8))
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.progressContainer.addWidget(self.progressBar)


        self.viewerLayout.addLayout(self.progressContainer)

        self.viewerActionLayout = QHBoxLayout()
        self.viewerActionLayout.setSpacing(8)
        self.viewerActionLayout.setObjectName(u"viewerActionLayout")
        self.saveImageButton = QPushButton(self.viewerCard)
        self.saveImageButton.setObjectName(u"saveImageButton")
        self.saveImageButton.setMinimumSize(QSize(0, 34))
        self.saveImageButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.viewerActionLayout.addWidget(self.saveImageButton)

        self.copyImageButton = QPushButton(self.viewerCard)
        self.copyImageButton.setObjectName(u"copyImageButton")
        self.copyImageButton.setMinimumSize(QSize(0, 34))
        self.copyImageButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.viewerActionLayout.addWidget(self.copyImageButton)

        self.openOutputFolderButton = QPushButton(self.viewerCard)
        self.openOutputFolderButton.setObjectName(u"openOutputFolderButton")
        self.openOutputFolderButton.setMinimumSize(QSize(0, 34))
        self.openOutputFolderButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.viewerActionLayout.addWidget(self.openOutputFolderButton)


        self.viewerLayout.addLayout(self.viewerActionLayout)


        self.rightLayout.addWidget(self.viewerCard)

        self.generateButton = PlayStopButton(self.rightContainer)
        self.generateButton.setObjectName(u"generateButton")
        self.generateButton.setMinimumSize(QSize(0, 46))
        self.generateButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.rightLayout.addWidget(self.generateButton)

        self.historyCard = QFrame(self.rightContainer)
        self.historyCard.setObjectName(u"historyCard")
        self.historyCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.historyLayout = QVBoxLayout(self.historyCard)
        self.historyLayout.setSpacing(8)
        self.historyLayout.setObjectName(u"historyLayout")
        self.historyLayout.setContentsMargins(12, 10, 12, 10)
        self.historyHeader = QHBoxLayout()
        self.historyHeader.setObjectName(u"historyHeader")
        self.historyTitle = QLabel(self.historyCard)
        self.historyTitle.setObjectName(u"historyTitle")

        self.historyHeader.addWidget(self.historyTitle)

        self.histSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.historyHeader.addItem(self.histSpacer)


        self.historyLayout.addLayout(self.historyHeader)

        self.thumbGridLayout = QHBoxLayout()
        self.thumbGridLayout.setSpacing(8)
        self.thumbGridLayout.setObjectName(u"thumbGridLayout")
        self.thumbBtn_0 = QPushButton(self.historyCard)
        self.thumbBtn_0.setObjectName(u"thumbBtn_0")
        self.thumbBtn_0.setMinimumSize(QSize(72, 72))
        self.thumbBtn_0.setMaximumSize(QSize(90, 90))
        self.thumbBtn_0.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.thumbGridLayout.addWidget(self.thumbBtn_0)

        self.thumbBtn_1 = QPushButton(self.historyCard)
        self.thumbBtn_1.setObjectName(u"thumbBtn_1")
        self.thumbBtn_1.setMinimumSize(QSize(72, 72))
        self.thumbBtn_1.setMaximumSize(QSize(90, 90))
        self.thumbBtn_1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.thumbGridLayout.addWidget(self.thumbBtn_1)

        self.thumbBtn_2 = QPushButton(self.historyCard)
        self.thumbBtn_2.setObjectName(u"thumbBtn_2")
        self.thumbBtn_2.setMinimumSize(QSize(72, 72))
        self.thumbBtn_2.setMaximumSize(QSize(90, 90))
        self.thumbBtn_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.thumbGridLayout.addWidget(self.thumbBtn_2)

        self.thumbBtn_3 = QPushButton(self.historyCard)
        self.thumbBtn_3.setObjectName(u"thumbBtn_3")
        self.thumbBtn_3.setMinimumSize(QSize(72, 72))
        self.thumbBtn_3.setMaximumSize(QSize(90, 90))
        self.thumbBtn_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.thumbGridLayout.addWidget(self.thumbBtn_3)


        self.historyLayout.addLayout(self.thumbGridLayout)


        self.rightLayout.addWidget(self.historyCard)


        self.studioLayout.addWidget(self.rightContainer)


        self.mainVerticalLayout.addWidget(self.studioContainer)

        self.logSectionFrame = QFrame(self.centralWidget)
        self.logSectionFrame.setObjectName(u"logSectionFrame")
        self.logSectionFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.logSectionLayout = QVBoxLayout(self.logSectionFrame)
        self.logSectionLayout.setSpacing(4)
        self.logSectionLayout.setObjectName(u"logSectionLayout")
        self.logSectionLayout.setContentsMargins(0, 0, 0, 0)
        self.logToggleBar = QHBoxLayout()
        self.logToggleBar.setObjectName(u"logToggleBar")
        self.toggleLogButton = QPushButton(self.logSectionFrame)
        self.toggleLogButton.setObjectName(u"toggleLogButton")
        self.toggleLogButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.logToggleBar.addWidget(self.toggleLogButton)

        self.logToggleSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.logToggleBar.addItem(self.logToggleSpacer)

        self.resetButton = QPushButton(self.logSectionFrame)
        self.resetButton.setObjectName(u"resetButton")
        self.resetButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.logToggleBar.addWidget(self.resetButton)


        self.logSectionLayout.addLayout(self.logToggleBar)

        self.logGroupBox = QGroupBox(self.logSectionFrame)
        self.logGroupBox.setObjectName(u"logGroupBox")
        self.logGroupLayout = QVBoxLayout(self.logGroupBox)
        self.logGroupLayout.setObjectName(u"logGroupLayout")
        self.logGroupLayout.setContentsMargins(6, 6, 6, 6)
        self.logTextEdit = QPlainTextEdit(self.logGroupBox)
        self.logTextEdit.setObjectName(u"logTextEdit")
        self.logTextEdit.setMaximumSize(QSize(16777215, 120))
        self.logTextEdit.setReadOnly(True)

        self.logGroupLayout.addWidget(self.logTextEdit)


        self.logSectionLayout.addWidget(self.logGroupBox)


        self.mainVerticalLayout.addWidget(self.logSectionFrame)

        self.hiddenSettingsContainer = QFrame(self.centralWidget)
        self.hiddenSettingsContainer.setObjectName(u"hiddenSettingsContainer")
        self.hiddenSettingsContainer.setVisible(False)
        self.settingsLayout = QVBoxLayout(self.hiddenSettingsContainer)
        self.settingsLayout.setSpacing(6)
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.comfyUrlEdit = QLineEdit(self.hiddenSettingsContainer)
        self.comfyUrlEdit.setObjectName(u"comfyUrlEdit")

        self.settingsLayout.addWidget(self.comfyUrlEdit)

        self.comfyCheckButton = QPushButton(self.hiddenSettingsContainer)
        self.comfyCheckButton.setObjectName(u"comfyCheckButton")

        self.settingsLayout.addWidget(self.comfyCheckButton)

        self.comfyStatusLabel = QLabel(self.hiddenSettingsContainer)
        self.comfyStatusLabel.setObjectName(u"comfyStatusLabel")

        self.settingsLayout.addWidget(self.comfyStatusLabel)

        self.comfyModelPathEdit = QLineEdit(self.hiddenSettingsContainer)
        self.comfyModelPathEdit.setObjectName(u"comfyModelPathEdit")

        self.settingsLayout.addWidget(self.comfyModelPathEdit)

        self.browseModelFolderButton = QPushButton(self.hiddenSettingsContainer)
        self.browseModelFolderButton.setObjectName(u"browseModelFolderButton")

        self.settingsLayout.addWidget(self.browseModelFolderButton)

        self.modelPathStatusLabel = QLabel(self.hiddenSettingsContainer)
        self.modelPathStatusLabel.setObjectName(u"modelPathStatusLabel")

        self.settingsLayout.addWidget(self.modelPathStatusLabel)

        self.lmUrlEdit = QLineEdit(self.hiddenSettingsContainer)
        self.lmUrlEdit.setObjectName(u"lmUrlEdit")

        self.settingsLayout.addWidget(self.lmUrlEdit)

        self.lmCheckButton = QPushButton(self.hiddenSettingsContainer)
        self.lmCheckButton.setObjectName(u"lmCheckButton")

        self.settingsLayout.addWidget(self.lmCheckButton)

        self.lmStatusLabel = QLabel(self.hiddenSettingsContainer)
        self.lmStatusLabel.setObjectName(u"lmStatusLabel")

        self.settingsLayout.addWidget(self.lmStatusLabel)

        self.loadConfigButton = QPushButton(self.hiddenSettingsContainer)
        self.loadConfigButton.setObjectName(u"loadConfigButton")

        self.settingsLayout.addWidget(self.loadConfigButton)

        self.saveConfigButton = QPushButton(self.hiddenSettingsContainer)
        self.saveConfigButton.setObjectName(u"saveConfigButton")

        self.settingsLayout.addWidget(self.saveConfigButton)

        self.restoreDefaultsButton = QPushButton(self.hiddenSettingsContainer)
        self.restoreDefaultsButton.setObjectName(u"restoreDefaultsButton")

        self.settingsLayout.addWidget(self.restoreDefaultsButton)

        self.exitButton = QPushButton(self.hiddenSettingsContainer)
        self.exitButton.setObjectName(u"exitButton")

        self.settingsLayout.addWidget(self.exitButton)

        self.helpBrowser = QTextBrowser(self.hiddenSettingsContainer)
        self.helpBrowser.setObjectName(u"helpBrowser")

        self.settingsLayout.addWidget(self.helpBrowser)


        self.mainVerticalLayout.addWidget(self.hiddenSettingsContainer)

        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ComfyUI Craft AI Easy Studio", None))
        self.appTitle.setText(QCoreApplication.translate("MainWindow", u"\u2728 ComfyUI Craft AI", None))
        self.badgeLabel.setText(QCoreApplication.translate("MainWindow", u"Easy Studio", None))
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
        self.helpButton.setText(QCoreApplication.translate("MainWindow", u"\u2753 \ub3c4\uc6c0\ub9d0", None))
        self.settingsButton.setText(QCoreApplication.translate("MainWindow", u"\u2699\ufe0f \uc124\uc815", None))
        self.step1Badge.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.step1Title.setText(QCoreApplication.translate("MainWindow", u"\ud55c\uad6d\uc5b4 \uc544\uc774\ub514\uc5b4 \uc785\ub825 & AI \ud504\ub86c\ud504\ud2b8 \ubcc0\ud658", None))
        self.positivePromptCounterLabel.setText(QCoreApplication.translate("MainWindow", u"0\uc790", None))
        self.lmModelSelectLabel.setText(QCoreApplication.translate("MainWindow", u"\uc5b8\uc5b4 \ubaa8\ub378 (LM Studio AI)", None))
#if QT_CONFIG(tooltip)
        self.lmModelCombo.setToolTip(QCoreApplication.translate("MainWindow", u"\ud504\ub86c\ud504\ud2b8 \ubc88\uc5ed \ubc0f \ud655\uc7a5\uc5d0 \uc0ac\uc6a9\ud560 LM Studio \uc5b8\uc5b4 \ubaa8\ub378\uc744 \uc120\ud0dd\ud569\ub2c8\ub2e4.", None))
#endif // QT_CONFIG(tooltip)
        self.positivePromptEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\ub9cc\ub4e4\uace0 \uc2f6\uc740 \uc774\ubbf8\uc9c0\ub97c \uc790\uc5f0\uc2a4\ub7ec\uc6b4 \ud55c\uad6d\uc5b4\ub85c \uc801\uc5b4\ubcf4\uc138\uc694. (\uc608: \ube44 \ub0b4\ub9ac\ub294 \ub124\uc628\uc0ac\uc778 \ub3c4\uc2dc\uc758 \uc740\ubc1c \uc548\ub4dc\ub85c\uc774\ub4dc \uc18c\ub140, \uc601\ud654 \uac19\uc740 \uc870\uba85)", None))
        self.enhancePromptButton.setText(QCoreApplication.translate("MainWindow", u"\u2728 AI \ud504\ub86c\ud504\ud2b8 \ub9c8\ubc95\uc0ac\ub85c \uc601\ubb38 \ud655\uc7a5 \uc0dd\uc131", None))
        self.enhancePromptLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f310 \U0000c0dd\U0000c131\U0000b41c \U0000c601\U0000bb38 \U0000d504\U0000b86c\U0000d504\U0000d2b8 (\U0000c9c1\U0000c811 \U0000c218\U0000c815 \U0000ac00\U0000b2a5)", None))
        self.enhancePromptCounterLabel.setText(QCoreApplication.translate("MainWindow", u"0\uc790", None))
        self.copyPromptButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4cb \U0000bcf5\U0000c0ac", None))
        self.enhancePromptEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"AI \ub9c8\ubc95\uc0ac\ub97c \uc2e4\ud589\ud558\uba74 \uc601\ubb38 \ucd5c\uc801\ud654 \ud504\ub86c\ud504\ud2b8\uac00 \uc0dd\uc131\ub418\uba70, \ud544\uc694\uc2dc \uc5ec\uae30\uc11c \uc9c1\uc811 \uc218\uc815\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.", None))
        self.negTitleLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f6ab \U0000bd80\U0000c815 \U0000d504\U0000b86c\U0000d504\U0000d2b8 (Negative Prompt)", None))
        self.negativePromptCounterLabel.setText(QCoreApplication.translate("MainWindow", u"0\uc790", None))
        self.negativePromptEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\ud488\uc9c8 \uc800\ud558 \ubc29\uc9c0\uc6a9 \ubd80\uc815\uc5b4 (SDXL \ub4f1 \uc804\uc6a9)", None))
        self.step2Badge.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.step2Title.setText(QCoreApplication.translate("MainWindow", u"\ud575\uc2ec \uc0dd\uc131 \uc635\uc158", None))
        self.modelProfileNoticeLabel.setText(QCoreApplication.translate("MainWindow", u"\u2713 \ucd5c\uc801 \uc124\uc815 \uc790\ub3d9 \uc801\uc6a9\ub428", None))
        self.modelSelectLabel.setText(QCoreApplication.translate("MainWindow", u"\uc0dd\uc131 \ubaa8\ub378 (AI \uc5d4\uc9c4)", None))
        self.aspectRatioTitle.setText(QCoreApplication.translate("MainWindow", u"\uc774\ubbf8\uc9c0 \ube44\uc728 \uc120\ud0dd", None))
        self.preset_1024x1024.setText(QCoreApplication.translate("MainWindow", u"\u25a1 \uc815\uc0ac\uac01 (1:1)\n"
"1024\u00d71024", None))
        self.preset_896x1152.setText(QCoreApplication.translate("MainWindow", u"\u25af \uc138\ub85c\ud615 (9:16) \u2605\n"
"896\u00d71152", None))
        self.preset_1152x896.setText(QCoreApplication.translate("MainWindow", u"\u25ad \uc640\uc774\ub4dc (16:9)\n"
"1152\u00d7896", None))
        self.widthLabel.setText(QCoreApplication.translate("MainWindow", u"\uac00\ub85c \ud3ed:", None))
        self.heightLabel.setText(QCoreApplication.translate("MainWindow", u"\uc138\ub85c \ub192\uc774:", None))
        self.facedetailerCheckBox.setText(QCoreApplication.translate("MainWindow", u"\U0001f464 FaceDetailer (\U0000c5bc\U0000ad74 \U0000c138\U0000bd80 \U0000bcf4\U0000c815 \U0000d65c\U0000c131\U0000d654)", None))
        self.facedetailerDenoiseLabel.setText(QCoreApplication.translate("MainWindow", u"Denoise (\ubcc0\ud654 \uac15\ub3c4)", None))
        self.facedetailerStepsLabel.setText(QCoreApplication.translate("MainWindow", u"Steps (\ubcf4\uc815 \uc2a4\ud15d)", None))
        self.facedetailerCfgLabel.setText(QCoreApplication.translate("MainWindow", u"CFG (\ud504\ub86c\ud504\ud2b8 \ubc18\uc601\ub3c4)", None))
        self.facedetailerFeatherLabel.setText(QCoreApplication.translate("MainWindow", u"Feather (\uacbd\uacc4 \ubd80\ub4dc\ub7ec\uc6c0)", None))
        self.facedetailerDropSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Drop Size (\ucd5c\uc18c \ud06c\uae30 \ud544\ud130)", None))
        self.facedetailerGuideSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Guide Size (\uac00\uc774\ub4dc \ud574\uc0c1\ub3c4)", None))
        self.facedetailerMaxSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Max Size (\ucd5c\ub300 \ud574\uc0c1\ub3c4)", None))
        self.facedetailerCycleLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle (\ubcf4\uc815 \ubc18\ubcf5 \ud69f\uc218)", None))
        self.facedetailerBboxThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"BBox Thresh (\uac10\uc9c0 \ubbfc\uac10\ub3c4)", None))
        self.facedetailerBboxDilationLabel.setText(QCoreApplication.translate("MainWindow", u"BBox Dilate (\ubc15\uc2a4 \ud655\uc7a5)", None))
        self.facedetailerBboxCropFactorLabel.setText(QCoreApplication.translate("MainWindow", u"Crop Factor (\ud06c\ub86d \uc5ec\ubc31)", None))
        self.facedetailerSamThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"SAM Thresh (\ub9c8\uc2a4\ud06c \uc815\ubc00\ub3c4)", None))
        self.facedetailerSamDilationLabel.setText(QCoreApplication.translate("MainWindow", u"SAM Dilate (\ub9c8\uc2a4\ud06c \ud33d\ucc3d)", None))
        self.facedetailerSamBboxExpansionLabel.setText(QCoreApplication.translate("MainWindow", u"SAM BBox Exp (SAM \uc601\uc5ed)", None))
        self.facedetailerSamMaskHintThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"Mask Hint Thresh (\ud78c\ud2b8 \uc784\uacc4)", None))
        self.facedetailerSamDetectionHintLabel.setText(QCoreApplication.translate("MainWindow", u"SAM Hint (\ud0d0\uc9c0 \uc704\uce58)", None))
        self.facedetailerSamMaskHintUseNegativeLabel.setText(QCoreApplication.translate("MainWindow", u"Mask Hint Neg (\uc5ed\ub9c8\uc2a4\ud06c)", None))
        self.advancedToggleBtn.setText(QCoreApplication.translate("MainWindow", u"\u2699\ufe0f \uace0\uae09 \uc124\uc815 \uc811\uae30 / \ud3bc\uce58\uae30 (\uc2dc\ub4dc, \uc2ac\ub77c\uc774\ub354, \uc0d8\ud50c\ub7ec)  \u25bc", None))
        self.seedTitleLabel.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\ub4dc \ubc88\ud638:", None))
        self.randomSeedButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f3b2 \U0000b79c\U0000b364", None))
        self.lockSeedButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f513 \U0000ace0\U0000c815 \U0000c548\U0000d568", None))
        self.cfgLabelTitle.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub86c\ud504\ud2b8 \ucda9\uc2e4\ub3c4 (CFG)", None))
        self.cfgValueLabel.setText(QCoreApplication.translate("MainWindow", u"3.5", None))
        self.stepsLabelTitle.setText(QCoreApplication.translate("MainWindow", u"\uc0d8\ud50c\ub9c1 \uc2a4\ud15d (Steps)", None))
        self.stepsValueLabel.setText(QCoreApplication.translate("MainWindow", u"24", None))
        self.samplerLabel.setText(QCoreApplication.translate("MainWindow", u"\uc0d8\ud50c\ub7ec", None))
        self.schedulerLabel.setText(QCoreApplication.translate("MainWindow", u"\uc2a4\ucf00\uc904\ub7ec", None))
        self.denoiseLabel.setText(QCoreApplication.translate("MainWindow", u"\ub514\ub178\uc774\uc988", None))
        self.viewerStatusDot.setText(QCoreApplication.translate("MainWindow", u"\u25cf", None))
        self.viewerTitle.setText(QCoreApplication.translate("MainWindow", u"\uc0dd\uc131 \uacb0\uacfc \ubdf0\uc5b4", None))
        self.elapsedLabel.setText(QCoreApplication.translate("MainWindow", u"0.0\ucd08", None))
        self.previewLabel.setText(QCoreApplication.translate("MainWindow", u"\uc0dd\uc131\ub41c \uc774\ubbf8\uc9c0\uac00 \uc5ec\uae30\uc5d0 \ud45c\uc2dc\ub429\ub2c8\ub2e4.", None))
        self.progressStatusLabel.setText(QCoreApplication.translate("MainWindow", u"\ub300\uae30 \uc911", None))
        self.progressPercentLabel.setText(QCoreApplication.translate("MainWindow", u"0%", None))
        self.saveImageButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4be \U0000b2e4\U0000b978 \U0000c774\U0000b984\U0000c73c\U0000b85c \U0000c800\U0000c7a5", None))
        self.copyImageButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4cb \U0000d074\U0000b9bd\U0000bcf4\U0000b4dc \U0000bcf5\U0000c0ac", None))
        self.openOutputFolderButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c1 \U0000d3f4\U0000b354 \U0000c5f4\U0000ae30", None))
        self.generateButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f680 \U0000c774\U0000bbf8\U0000c9c0 \U0000c0dd\U0000c131\U0000d558\U0000ae30 (ComfyUI \U0000c804\U0000c1a1)", None))
        self.historyTitle.setText(QCoreApplication.translate("MainWindow", u"\ucd5c\uadfc \uc0dd\uc131 \uae30\ub85d (\ud074\ub9ad \uc2dc \uc774\ubbf8\uc9c0 & \uc124\uc815 \ubcf5\uc6d0)", None))
        self.thumbBtn_0.setText(QCoreApplication.translate("MainWindow", u"\ub300\uae30 \uc911", None))
        self.thumbBtn_1.setText(QCoreApplication.translate("MainWindow", u"\ub300\uae30 \uc911", None))
        self.thumbBtn_2.setText(QCoreApplication.translate("MainWindow", u"\ub300\uae30 \uc911", None))
        self.thumbBtn_3.setText(QCoreApplication.translate("MainWindow", u"\ub300\uae30 \uc911", None))
        self.toggleLogButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4dc \U0000cf58\U0000c194 \U0000b85c\U0000adf8 \U0000bcf4\U0000ae30 / \U0000c811\U0000ae30  \U000025bc", None))
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"\ub85c\uadf8 \uc9c0\uc6b0\uae30", None))
        self.logGroupBox.setTitle("")
    # retranslateUi

