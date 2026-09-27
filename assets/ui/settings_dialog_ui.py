# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QDoubleSpinBox,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(500, 822)
        SettingsDialog.setMinimumSize(QSize(500, 820))
        self.dialogLayout = QVBoxLayout(SettingsDialog)
        self.dialogLayout.setSpacing(10)
        self.dialogLayout.setObjectName(u"dialogLayout")
        self.settingsTabWidget = QTabWidget(SettingsDialog)
        self.settingsTabWidget.setObjectName(u"settingsTabWidget")
        self.tabAiServer = QWidget()
        self.tabAiServer.setObjectName(u"tabAiServer")
        self.tabAiServerLayout = QVBoxLayout(self.tabAiServer)
        self.tabAiServerLayout.setObjectName(u"tabAiServerLayout")
        self.comfyGroupBox = QGroupBox(self.tabAiServer)
        self.comfyGroupBox.setObjectName(u"comfyGroupBox")
        self.gridLayout = QGridLayout(self.comfyGroupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comfyNameLabel = QLabel(self.comfyGroupBox)
        self.comfyNameLabel.setObjectName(u"comfyNameLabel")

        self.horizontalLayout.addWidget(self.comfyNameLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.dlgComfyStatusLabel = QLabel(self.comfyGroupBox)
        self.dlgComfyStatusLabel.setObjectName(u"dlgComfyStatusLabel")

        self.horizontalLayout.addWidget(self.dlgComfyStatusLabel)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.comfyUrlRow = QHBoxLayout()
        self.comfyUrlRow.setObjectName(u"comfyUrlRow")
        self.comfyUrlLabel = QLabel(self.comfyGroupBox)
        self.comfyUrlLabel.setObjectName(u"comfyUrlLabel")

        self.comfyUrlRow.addWidget(self.comfyUrlLabel)

        self.dlgComfyUrlEdit = QLineEdit(self.comfyGroupBox)
        self.dlgComfyUrlEdit.setObjectName(u"dlgComfyUrlEdit")

        self.comfyUrlRow.addWidget(self.dlgComfyUrlEdit)

        self.dlgComfyCheckBtn = QPushButton(self.comfyGroupBox)
        self.dlgComfyCheckBtn.setObjectName(u"dlgComfyCheckBtn")

        self.comfyUrlRow.addWidget(self.dlgComfyCheckBtn)


        self.gridLayout.addLayout(self.comfyUrlRow, 1, 0, 1, 1)

        self.modelPathRow = QHBoxLayout()
        self.modelPathRow.setObjectName(u"modelPathRow")
        self.modelPathLabel = QLabel(self.comfyGroupBox)
        self.modelPathLabel.setObjectName(u"modelPathLabel")

        self.modelPathRow.addWidget(self.modelPathLabel)

        self.dlgModelPathEdit = QLineEdit(self.comfyGroupBox)
        self.dlgModelPathEdit.setObjectName(u"dlgModelPathEdit")

        self.modelPathRow.addWidget(self.dlgModelPathEdit)

        self.dlgBrowseBtn = QPushButton(self.comfyGroupBox)
        self.dlgBrowseBtn.setObjectName(u"dlgBrowseBtn")

        self.modelPathRow.addWidget(self.dlgBrowseBtn)


        self.gridLayout.addLayout(self.modelPathRow, 2, 0, 1, 1)

        self.dlgModelPathStatusLabel = QLabel(self.comfyGroupBox)
        self.dlgModelPathStatusLabel.setObjectName(u"dlgModelPathStatusLabel")
        self.dlgModelPathStatusLabel.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.dlgModelPathStatusLabel.setAutoFillBackground(False)

        self.gridLayout.addWidget(self.dlgModelPathStatusLabel, 3, 0, 1, 1)


        self.tabAiServerLayout.addWidget(self.comfyGroupBox)

        self.lmGroupBox = QGroupBox(self.tabAiServer)
        self.lmGroupBox.setObjectName(u"lmGroupBox")
        self.gridLayout_2 = QGridLayout(self.lmGroupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lmNameLabel = QLabel(self.lmGroupBox)
        self.lmNameLabel.setObjectName(u"lmNameLabel")

        self.horizontalLayout_2.addWidget(self.lmNameLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.dlgLmStatusLabel = QLabel(self.lmGroupBox)
        self.dlgLmStatusLabel.setObjectName(u"dlgLmStatusLabel")

        self.horizontalLayout_2.addWidget(self.dlgLmStatusLabel)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.lmUrlRow = QHBoxLayout()
        self.lmUrlRow.setObjectName(u"lmUrlRow")
        self.lmUrlLabel = QLabel(self.lmGroupBox)
        self.lmUrlLabel.setObjectName(u"lmUrlLabel")

        self.lmUrlRow.addWidget(self.lmUrlLabel)

        self.dlgLmUrlEdit = QLineEdit(self.lmGroupBox)
        self.dlgLmUrlEdit.setObjectName(u"dlgLmUrlEdit")

        self.lmUrlRow.addWidget(self.dlgLmUrlEdit)

        self.dlgLmCheckBtn = QPushButton(self.lmGroupBox)
        self.dlgLmCheckBtn.setObjectName(u"dlgLmCheckBtn")

        self.lmUrlRow.addWidget(self.dlgLmCheckBtn)


        self.gridLayout_2.addLayout(self.lmUrlRow, 1, 0, 1, 1)


        self.tabAiServerLayout.addWidget(self.lmGroupBox)

        self.settingsTabWidget.addTab(self.tabAiServer, "")
        self.tabModel = QWidget()
        self.tabModel.setObjectName(u"tabModel")
        self.tabModelLayout = QVBoxLayout(self.tabModel)
        self.tabModelLayout.setObjectName(u"tabModelLayout")
        self.profileAutoLabel = QLabel(self.tabModel)
        self.profileAutoLabel.setObjectName(u"profileAutoLabel")

        self.tabModelLayout.addWidget(self.profileAutoLabel)

        self.profileAutoList = QListWidget(self.tabModel)
        self.profileAutoList.setObjectName(u"profileAutoList")
        self.profileAutoList.setMinimumSize(QSize(0, 90))
        self.profileAutoList.setMaximumSize(QSize(16777215, 140))

        self.tabModelLayout.addWidget(self.profileAutoList)

        self.profileManualLabel = QLabel(self.tabModel)
        self.profileManualLabel.setObjectName(u"profileManualLabel")

        self.tabModelLayout.addWidget(self.profileManualLabel)

        self.p8RowLayout_modelFile = QHBoxLayout()
        self.p8RowLayout_modelFile.setSpacing(8)
        self.p8RowLayout_modelFile.setObjectName(u"p8RowLayout_modelFile")
        self.label = QLabel(self.tabModel)
        self.label.setObjectName(u"label")

        self.p8RowLayout_modelFile.addWidget(self.label)

        self.profileModelFileEdit = QLineEdit(self.tabModel)
        self.profileModelFileEdit.setObjectName(u"profileModelFileEdit")

        self.p8RowLayout_modelFile.addWidget(self.profileModelFileEdit)

        self.profileModelFileBrowseBtn = QPushButton(self.tabModel)
        self.profileModelFileBrowseBtn.setObjectName(u"profileModelFileBrowseBtn")
        self.profileModelFileBrowseBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.p8RowLayout_modelFile.addWidget(self.profileModelFileBrowseBtn)


        self.tabModelLayout.addLayout(self.p8RowLayout_modelFile)

        self.p8RowLayout_workflow = QHBoxLayout()
        self.p8RowLayout_workflow.setSpacing(8)
        self.p8RowLayout_workflow.setObjectName(u"p8RowLayout_workflow")
        self.label1 = QLabel(self.tabModel)
        self.label1.setObjectName(u"label1")

        self.p8RowLayout_workflow.addWidget(self.label1)

        self.profileWorkflowFileEdit = QLineEdit(self.tabModel)
        self.profileWorkflowFileEdit.setObjectName(u"profileWorkflowFileEdit")
        self.profileWorkflowFileEdit.setReadOnly(True)

        self.p8RowLayout_workflow.addWidget(self.profileWorkflowFileEdit)

        self.profileWorkflowBrowseBtn = QPushButton(self.tabModel)
        self.profileWorkflowBrowseBtn.setObjectName(u"profileWorkflowBrowseBtn")
        self.profileWorkflowBrowseBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.p8RowLayout_workflow.addWidget(self.profileWorkflowBrowseBtn)

        self.profileAiWorkflowBtn = QPushButton(self.tabModel)
        self.profileAiWorkflowBtn.setObjectName(u"profileAiWorkflowBtn")
        self.profileAiWorkflowBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.p8RowLayout_workflow.addWidget(self.profileAiWorkflowBtn)


        self.tabModelLayout.addLayout(self.p8RowLayout_workflow)

        self.p8RowLayout_1 = QHBoxLayout()
        self.p8RowLayout_1.setSpacing(8)
        self.p8RowLayout_1.setObjectName(u"p8RowLayout_1")
        self.label2 = QLabel(self.tabModel)
        self.label2.setObjectName(u"label2")

        self.p8RowLayout_1.addWidget(self.label2)

        self.profileNameEdit = QLineEdit(self.tabModel)
        self.profileNameEdit.setObjectName(u"profileNameEdit")

        self.p8RowLayout_1.addWidget(self.profileNameEdit)


        self.tabModelLayout.addLayout(self.p8RowLayout_1)

        self.p8RowLayout_2 = QHBoxLayout()
        self.p8RowLayout_2.setSpacing(8)
        self.p8RowLayout_2.setObjectName(u"p8RowLayout_2")
        self.label3 = QLabel(self.tabModel)
        self.label3.setObjectName(u"label3")

        self.p8RowLayout_2.addWidget(self.label3)

        self.profilePatternsEdit = QLineEdit(self.tabModel)
        self.profilePatternsEdit.setObjectName(u"profilePatternsEdit")

        self.p8RowLayout_2.addWidget(self.profilePatternsEdit)


        self.tabModelLayout.addLayout(self.p8RowLayout_2)

        self.p8RowLayout_3 = QHBoxLayout()
        self.p8RowLayout_3.setSpacing(8)
        self.p8RowLayout_3.setObjectName(u"p8RowLayout_3")
        self.label4 = QLabel(self.tabModel)
        self.label4.setObjectName(u"label4")

        self.p8RowLayout_3.addWidget(self.label4)

        self.profileWorkflowCombo = QComboBox(self.tabModel)
        self.profileWorkflowCombo.addItem("")
        self.profileWorkflowCombo.addItem("")
        self.profileWorkflowCombo.addItem("")
        self.profileWorkflowCombo.addItem("")
        self.profileWorkflowCombo.setObjectName(u"profileWorkflowCombo")

        self.p8RowLayout_3.addWidget(self.profileWorkflowCombo)


        self.tabModelLayout.addLayout(self.p8RowLayout_3)

        self.p8RowLayout_4 = QHBoxLayout()
        self.p8RowLayout_4.setSpacing(8)
        self.p8RowLayout_4.setObjectName(u"p8RowLayout_4")
        self.label5 = QLabel(self.tabModel)
        self.label5.setObjectName(u"label5")

        self.p8RowLayout_4.addWidget(self.label5)

        self.profileStepsSpin = QSpinBox(self.tabModel)
        self.profileStepsSpin.setObjectName(u"profileStepsSpin")
        self.profileStepsSpin.setMinimum(1)
        self.profileStepsSpin.setMaximum(200)
        self.profileStepsSpin.setSingleStep(1)
        self.profileStepsSpin.setValue(20)

        self.p8RowLayout_4.addWidget(self.profileStepsSpin)


        self.tabModelLayout.addLayout(self.p8RowLayout_4)

        self.p8RowLayout_5 = QHBoxLayout()
        self.p8RowLayout_5.setSpacing(8)
        self.p8RowLayout_5.setObjectName(u"p8RowLayout_5")
        self.label6 = QLabel(self.tabModel)
        self.label6.setObjectName(u"label6")

        self.p8RowLayout_5.addWidget(self.label6)

        self.profileCfgSpin = QDoubleSpinBox(self.tabModel)
        self.profileCfgSpin.setObjectName(u"profileCfgSpin")
        self.profileCfgSpin.setMinimum(0.100000000000000)
        self.profileCfgSpin.setMaximum(30.000000000000000)
        self.profileCfgSpin.setSingleStep(0.100000000000000)
        self.profileCfgSpin.setValue(7.000000000000000)

        self.p8RowLayout_5.addWidget(self.profileCfgSpin)


        self.tabModelLayout.addLayout(self.p8RowLayout_5)

        self.p8RowLayout_6 = QHBoxLayout()
        self.p8RowLayout_6.setSpacing(8)
        self.p8RowLayout_6.setObjectName(u"p8RowLayout_6")
        self.label7 = QLabel(self.tabModel)
        self.label7.setObjectName(u"label7")

        self.p8RowLayout_6.addWidget(self.label7)

        self.profileSamplerCombo = QComboBox(self.tabModel)
        self.profileSamplerCombo.addItem("")
        self.profileSamplerCombo.addItem("")
        self.profileSamplerCombo.addItem("")
        self.profileSamplerCombo.addItem("")
        self.profileSamplerCombo.addItem("")
        self.profileSamplerCombo.addItem("")
        self.profileSamplerCombo.setObjectName(u"profileSamplerCombo")

        self.p8RowLayout_6.addWidget(self.profileSamplerCombo)


        self.tabModelLayout.addLayout(self.p8RowLayout_6)

        self.p8RowLayout_7 = QHBoxLayout()
        self.p8RowLayout_7.setSpacing(8)
        self.p8RowLayout_7.setObjectName(u"p8RowLayout_7")
        self.label8 = QLabel(self.tabModel)
        self.label8.setObjectName(u"label8")

        self.p8RowLayout_7.addWidget(self.label8)

        self.profileSchedulerCombo = QComboBox(self.tabModel)
        self.profileSchedulerCombo.addItem("")
        self.profileSchedulerCombo.addItem("")
        self.profileSchedulerCombo.addItem("")
        self.profileSchedulerCombo.addItem("")
        self.profileSchedulerCombo.setObjectName(u"profileSchedulerCombo")

        self.p8RowLayout_7.addWidget(self.profileSchedulerCombo)


        self.tabModelLayout.addLayout(self.p8RowLayout_7)

        self.p8RowLayout_8 = QHBoxLayout()
        self.p8RowLayout_8.setSpacing(8)
        self.p8RowLayout_8.setObjectName(u"p8RowLayout_8")
        self.label9 = QLabel(self.tabModel)
        self.label9.setObjectName(u"label9")

        self.p8RowLayout_8.addWidget(self.label9)

        self.profileClip1Edit = QLineEdit(self.tabModel)
        self.profileClip1Edit.setObjectName(u"profileClip1Edit")

        self.p8RowLayout_8.addWidget(self.profileClip1Edit)


        self.tabModelLayout.addLayout(self.p8RowLayout_8)

        self.p8RowLayout_9 = QHBoxLayout()
        self.p8RowLayout_9.setSpacing(8)
        self.p8RowLayout_9.setObjectName(u"p8RowLayout_9")
        self.label10 = QLabel(self.tabModel)
        self.label10.setObjectName(u"label10")

        self.p8RowLayout_9.addWidget(self.label10)

        self.profileClip2Edit = QLineEdit(self.tabModel)
        self.profileClip2Edit.setObjectName(u"profileClip2Edit")

        self.p8RowLayout_9.addWidget(self.profileClip2Edit)


        self.tabModelLayout.addLayout(self.p8RowLayout_9)

        self.p8RowLayout_10 = QHBoxLayout()
        self.p8RowLayout_10.setSpacing(8)
        self.p8RowLayout_10.setObjectName(u"p8RowLayout_10")
        self.label11 = QLabel(self.tabModel)
        self.label11.setObjectName(u"label11")

        self.p8RowLayout_10.addWidget(self.label11)

        self.profileVaeEdit = QLineEdit(self.tabModel)
        self.profileVaeEdit.setObjectName(u"profileVaeEdit")

        self.p8RowLayout_10.addWidget(self.profileVaeEdit)


        self.tabModelLayout.addLayout(self.p8RowLayout_10)

        self.p8RowLayout_11 = QHBoxLayout()
        self.p8RowLayout_11.setSpacing(8)
        self.p8RowLayout_11.setObjectName(u"p8RowLayout_11")
        self.profileDeleteBtn = QPushButton(self.tabModel)
        self.profileDeleteBtn.setObjectName(u"profileDeleteBtn")
        self.profileDeleteBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.p8RowLayout_11.addWidget(self.profileDeleteBtn)

        self.profileFileCombo = QComboBox(self.tabModel)
        self.profileFileCombo.setObjectName(u"profileFileCombo")

        self.p8RowLayout_11.addWidget(self.profileFileCombo)


        self.tabModelLayout.addLayout(self.p8RowLayout_11)

        self.profileValidateLabel = QLabel(self.tabModel)
        self.profileValidateLabel.setObjectName(u"profileValidateLabel")
        self.profileValidateLabel.setWordWrap(True)

        self.tabModelLayout.addWidget(self.profileValidateLabel)

        self.profileSaveBtn = QPushButton(self.tabModel)
        self.profileSaveBtn.setObjectName(u"profileSaveBtn")
        self.profileSaveBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tabModelLayout.addWidget(self.profileSaveBtn)

        self.settingsTabWidget.addTab(self.tabModel, "")
        self.tabLog = QWidget()
        self.tabLog.setObjectName(u"tabLog")
        self.tabLogLayout = QVBoxLayout(self.tabLog)
        self.tabLogLayout.setSpacing(8)
        self.tabLogLayout.setObjectName(u"tabLogLayout")
        self.logTabTitle = QLabel(self.tabLog)
        self.logTabTitle.setObjectName(u"logTabTitle")

        self.tabLogLayout.addWidget(self.logTabTitle)

        self.logTabEdit = QTextEdit(self.tabLog)
        self.logTabEdit.setObjectName(u"logTabEdit")
        self.logTabEdit.setReadOnly(True)

        self.tabLogLayout.addWidget(self.logTabEdit)

        self.logTabButtons = QHBoxLayout()
        self.logTabButtons.setSpacing(8)
        self.logTabButtons.setObjectName(u"logTabButtons")
        self.logClearBtn = QPushButton(self.tabLog)
        self.logClearBtn.setObjectName(u"logClearBtn")

        self.logTabButtons.addWidget(self.logClearBtn)

        self.logSaveBtn = QPushButton(self.tabLog)
        self.logSaveBtn.setObjectName(u"logSaveBtn")

        self.logTabButtons.addWidget(self.logSaveBtn)

        self.logCopyBtn = QPushButton(self.tabLog)
        self.logCopyBtn.setObjectName(u"logCopyBtn")

        self.logTabButtons.addWidget(self.logCopyBtn)


        self.tabLogLayout.addLayout(self.logTabButtons)

        self.settingsTabWidget.addTab(self.tabLog, "")

        self.dialogLayout.addWidget(self.settingsTabWidget)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.dialogLayout.addItem(self.verticalSpacer)

        self.bottomBtnRow = QHBoxLayout()
        self.bottomBtnRow.setObjectName(u"bottomBtnRow")
        self.dlgLoadConfigBtn = QPushButton(SettingsDialog)
        self.dlgLoadConfigBtn.setObjectName(u"dlgLoadConfigBtn")

        self.bottomBtnRow.addWidget(self.dlgLoadConfigBtn)

        self.dlgResetDefaultsBtn = QPushButton(SettingsDialog)
        self.dlgResetDefaultsBtn.setObjectName(u"dlgResetDefaultsBtn")

        self.bottomBtnRow.addWidget(self.dlgResetDefaultsBtn)

        self.btnSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomBtnRow.addItem(self.btnSpacer)

        self.dlgSaveCloseBtn = QPushButton(SettingsDialog)
        self.dlgSaveCloseBtn.setObjectName(u"dlgSaveCloseBtn")

        self.bottomBtnRow.addWidget(self.dlgSaveCloseBtn)


        self.dialogLayout.addLayout(self.bottomBtnRow)


        self.retranslateUi(SettingsDialog)

        self.settingsTabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"\uc11c\ubc84 \uc5f0\uacb0 \ubc0f \ubaa8\ub378 \ud3f4\ub354 \uc124\uc815", None))
        self.comfyGroupBox.setTitle("")
        self.comfyNameLabel.setText(QCoreApplication.translate("SettingsDialog", u"\U0001f3a8 ComfyUI \U0000c124\U0000c815", None))
        self.dlgComfyStatusLabel.setText(QCoreApplication.translate("SettingsDialog", u"\uc5f0\uacb0 \ub300\uae30\uc911", None))
        self.comfyUrlLabel.setText(QCoreApplication.translate("SettingsDialog", u"\uc11c\ubc84 \uc8fc\uc18c:", None))
        self.dlgComfyCheckBtn.setText(QCoreApplication.translate("SettingsDialog", u"\uc5f0\uacb0 \ud655\uc778", None))
        self.modelPathLabel.setText(QCoreApplication.translate("SettingsDialog", u"\ubaa8\ub378 \ud3f4\ub354:", None))
        self.dlgBrowseBtn.setText(QCoreApplication.translate("SettingsDialog", u"\ucc3e\uc544\ubcf4\uae30", None))
        self.dlgModelPathStatusLabel.setText(QCoreApplication.translate("SettingsDialog", u"comfyUI\uc758 \uc124\uce58\ub41c \ubaa8\ub378\ud3f4\ub354\ub97c \ubd88\ub7ec\uc624\uc138\uc694", None))
        self.lmGroupBox.setTitle("")
        self.lmNameLabel.setText(QCoreApplication.translate("SettingsDialog", u"\U0001f4ac LM Studio \U0000c124\U0000c815", None))
        self.dlgLmStatusLabel.setText(QCoreApplication.translate("SettingsDialog", u"\uc5f0\uacb0 \ub300\uae30\uc911", None))
        self.lmUrlLabel.setText(QCoreApplication.translate("SettingsDialog", u"\uc11c\ubc84 \uc8fc\uc18c:", None))
        self.dlgLmCheckBtn.setText(QCoreApplication.translate("SettingsDialog", u"\uc5f0\uacb0 \ud655\uc778", None))
        self.settingsTabWidget.setTabText(self.settingsTabWidget.indexOf(self.tabAiServer), QCoreApplication.translate("SettingsDialog", u"AI \uc11c\ubc84", None))
        self.profileAutoLabel.setText(QCoreApplication.translate("SettingsDialog", u"\uc790\ub3d9 \ud310\ubcc4 \ubaa8\ub378 (\uc77d\uae30 \uc804\uc6a9)", None))
        self.profileManualLabel.setText(QCoreApplication.translate("SettingsDialog", u"\uc218\ub3d9 \ud504\ub85c\ud544 (\uace0\uae09 \u00b7 \uc2e0\uaddc/\uc608\uc678 \ubaa8\ub378\uc6a9)", None))
        self.label.setText(QCoreApplication.translate("SettingsDialog", u"\ubaa8\ub378 \ud30c\uc77c", None))
        self.profileModelFileEdit.setPlaceholderText(QCoreApplication.translate("SettingsDialog", u"\uc608: my-model.safetensors", None))
        self.profileModelFileBrowseBtn.setText(QCoreApplication.translate("SettingsDialog", u"\ucc3e\uc544\ubcf4\uae30", None))
        self.label1.setText(QCoreApplication.translate("SettingsDialog", u"\uc6cc\ud06c\ud50c\ub85c\uc6b0", None))
        self.profileWorkflowFileEdit.setPlaceholderText(QCoreApplication.translate("SettingsDialog", u"\ubaa8\ub378 \ud30c\uc77c\uc744 \uace0\ub974\uba74 \uc790\ub3d9\uc73c\ub85c \ub9cc\ub4e4\uc5b4\uc9d1\ub2c8\ub2e4", None))
        self.profileWorkflowBrowseBtn.setText(QCoreApplication.translate("SettingsDialog", u"\ucc3e\uc544\ubcf4\uae30", None))
        self.profileAiWorkflowBtn.setText(QCoreApplication.translate("SettingsDialog", u"AI\ub85c \ub9cc\ub4e4\uae30 (\uc2e4\ud5d8\uc801)", None))
        self.label2.setText(QCoreApplication.translate("SettingsDialog", u"\ud504\ub85c\ud544\uba85", None))
        self.profileNameEdit.setPlaceholderText(QCoreApplication.translate("SettingsDialog", u"\uc608: my-model", None))
        self.label3.setText(QCoreApplication.translate("SettingsDialog", u"\ub9e4\uce6d \ud328\ud134", None))
        self.profilePatternsEdit.setPlaceholderText(QCoreApplication.translate("SettingsDialog", u"\ud30c\uc77c\uba85 \uc77c\ubd80, \uc27c\ud45c \uad6c\ubd84", None))
        self.label4.setText(QCoreApplication.translate("SettingsDialog", u"\uc6cc\ud06c\ud50c\ub85c\uc6b0 \uc885\ub958", None))
        self.profileWorkflowCombo.setItemText(0, QCoreApplication.translate("SettingsDialog", u"checkpoint", None))
        self.profileWorkflowCombo.setItemText(1, QCoreApplication.translate("SettingsDialog", u"gguf", None))
        self.profileWorkflowCombo.setItemText(2, QCoreApplication.translate("SettingsDialog", u"flux_gguf", None))
        self.profileWorkflowCombo.setItemText(3, QCoreApplication.translate("SettingsDialog", u"zimage", None))

        self.label5.setText(QCoreApplication.translate("SettingsDialog", u"Steps", None))
        self.label6.setText(QCoreApplication.translate("SettingsDialog", u"CFG", None))
        self.label7.setText(QCoreApplication.translate("SettingsDialog", u"\uc0d8\ud50c\ub7ec", None))
        self.profileSamplerCombo.setItemText(0, QCoreApplication.translate("SettingsDialog", u"euler", None))
        self.profileSamplerCombo.setItemText(1, QCoreApplication.translate("SettingsDialog", u"dpmpp_2m", None))
        self.profileSamplerCombo.setItemText(2, QCoreApplication.translate("SettingsDialog", u"dpmpp_2m_sde", None))
        self.profileSamplerCombo.setItemText(3, QCoreApplication.translate("SettingsDialog", u"euler_ancestral", None))
        self.profileSamplerCombo.setItemText(4, QCoreApplication.translate("SettingsDialog", u"lcm", None))
        self.profileSamplerCombo.setItemText(5, QCoreApplication.translate("SettingsDialog", u"ddim", None))

        self.label8.setText(QCoreApplication.translate("SettingsDialog", u"\uc2a4\ucf00\uc904\ub7ec", None))
        self.profileSchedulerCombo.setItemText(0, QCoreApplication.translate("SettingsDialog", u"normal", None))
        self.profileSchedulerCombo.setItemText(1, QCoreApplication.translate("SettingsDialog", u"karras", None))
        self.profileSchedulerCombo.setItemText(2, QCoreApplication.translate("SettingsDialog", u"exponential", None))
        self.profileSchedulerCombo.setItemText(3, QCoreApplication.translate("SettingsDialog", u"simple", None))

        self.label9.setText(QCoreApplication.translate("SettingsDialog", u"CLIP 1", None))
        self.profileClip1Edit.setPlaceholderText(QCoreApplication.translate("SettingsDialog", u"\uc120\ud0dd \uc0ac\ud56d", None))
        self.label10.setText(QCoreApplication.translate("SettingsDialog", u"CLIP 2", None))
        self.profileClip2Edit.setPlaceholderText(QCoreApplication.translate("SettingsDialog", u"\uc120\ud0dd \uc0ac\ud56d", None))
        self.label11.setText(QCoreApplication.translate("SettingsDialog", u"VAE", None))
        self.profileVaeEdit.setPlaceholderText(QCoreApplication.translate("SettingsDialog", u"\uc120\ud0dd \uc0ac\ud56d", None))
        self.profileDeleteBtn.setText(QCoreApplication.translate("SettingsDialog", u"\ud504\ub85c\ud544 \uc0ad\uc81c", None))
#if QT_CONFIG(accessibility)
        self.profileValidateLabel.setAccessibleName(QCoreApplication.translate("SettingsDialog", u"\uc218\ub3d9 \ud504\ub85c\ud544 \uac80\uc99d \uacb0\uacfc", None))
#endif // QT_CONFIG(accessibility)
        self.profileValidateLabel.setText(QCoreApplication.translate("SettingsDialog", u"\uc2e0\uaddc \ud504\ub85c\ud544 \uc815\ubcf4\ub97c \uc785\ub825\ud558\uace0 [\ubaa8\ub378 \uc815\ubcf4 \uc800\uc7a5]\uc744 \ub204\ub974\uc138\uc694.", None))
        self.profileSaveBtn.setText(QCoreApplication.translate("SettingsDialog", u"\ubaa8\ub378 \uc815\ubcf4 \uc800\uc7a5", None))
        self.settingsTabWidget.setTabText(self.settingsTabWidget.indexOf(self.tabModel), QCoreApplication.translate("SettingsDialog", u"\uc774\ubbf8\uc9c0 \ubaa8\ub378 \ud504\ub85c\ud544", None))
        self.logTabTitle.setText(QCoreApplication.translate("SettingsDialog", u"\uc2e4\ud589 \ub85c\uadf8 (\uc77d\uae30 \uc804\uc6a9, \ucd5c\ub300 5000\uc904)", None))
        self.logClearBtn.setText(QCoreApplication.translate("SettingsDialog", u"\ub85c\uadf8 \ucd08\uae30\ud654", None))
        self.logSaveBtn.setText(QCoreApplication.translate("SettingsDialog", u"\ud30c\uc77c\ub85c \uc800\uc7a5", None))
        self.logCopyBtn.setText(QCoreApplication.translate("SettingsDialog", u"\uc804\uccb4 \ubcf5\uc0ac", None))
        self.settingsTabWidget.setTabText(self.settingsTabWidget.indexOf(self.tabLog), QCoreApplication.translate("SettingsDialog", u"\ub85c\uadf8", None))
#if QT_CONFIG(tooltip)
        self.dlgLoadConfigBtn.setToolTip(QCoreApplication.translate("SettingsDialog", u"\uc800\uc7a5\ub41c \uc124\uc815 \ud30c\uc77c(app_config.json)\uc744 \ubd88\ub7ec\uc635\ub2c8\ub2e4", None))
#endif // QT_CONFIG(tooltip)
        self.dlgLoadConfigBtn.setText(QCoreApplication.translate("SettingsDialog", u"\U0001f4c2 \U0000c124\U0000c815 \U0000bd88\U0000b7ec\U0000c624\U0000ae30", None))
#if QT_CONFIG(tooltip)
        self.dlgResetDefaultsBtn.setToolTip(QCoreApplication.translate("SettingsDialog", u"\ubaa8\ub4e0 \uac12\uc744 \ud504\ub85c\uadf8\ub7a8 \uae30\ubcf8\uac12\uc73c\ub85c \ub418\ub3cc\ub9bd\ub2c8\ub2e4", None))
#endif // QT_CONFIG(tooltip)
        self.dlgResetDefaultsBtn.setText(QCoreApplication.translate("SettingsDialog", u"\u21a9 \ucd08\uae30\ud654", None))
#if QT_CONFIG(tooltip)
        self.dlgSaveCloseBtn.setToolTip(QCoreApplication.translate("SettingsDialog", u"\ud604\uc7ac \uac12\uc744 \uc800\uc7a5\ud558\uace0 \ucc3d\uc744 \ub2eb\uc2b5\ub2c8\ub2e4", None))
#endif // QT_CONFIG(tooltip)
        self.dlgSaveCloseBtn.setText(QCoreApplication.translate("SettingsDialog", u"\U0001f4be \U0000c124\U0000c815 \U0000c800\U0000c7a5 \U0000d6c4 \U0000b2eb\U0000ae30", None))
    # retranslateUi

