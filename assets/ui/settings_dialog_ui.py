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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(520, 389)
        SettingsDialog.setMinimumSize(QSize(480, 200))
        self.dialogLayout = QVBoxLayout(SettingsDialog)
        self.dialogLayout.setSpacing(12)
        self.dialogLayout.setObjectName(u"dialogLayout")
        self.comfyGroupBox = QGroupBox(SettingsDialog)
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


        self.dialogLayout.addWidget(self.comfyGroupBox)

        self.lmGroupBox = QGroupBox(SettingsDialog)
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


        self.dialogLayout.addWidget(self.lmGroupBox)

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

