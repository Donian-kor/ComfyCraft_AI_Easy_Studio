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
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPlainTextEdit, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QSplitter, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget)
import icon_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1663, 1158)
        MainWindow.setMinimumSize(QSize(1323, 810))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"background-color: #0e1016;\n"
"color: #e8eaf0;\n"
"font-family: \"Segoe UI\", \"Malgun Gothic\", \"Segoe UI Emoji\", Arial, sans-serif;\n"
"font-size: 13px;")
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setStyleSheet(u"background-color: #0e1016;\n"
"color: #e8eaf0;")
        self.mainSplitter = QSplitter(self.centralWidget)
        self.mainSplitter.setObjectName(u"mainSplitter")
        self.mainSplitter.setGeometry(QRect(530, 60, 631, 441))
        self.mainSplitter.setStyleSheet(u"QSplitter::handle {\n"
"    background-color: #262b3a;\n"
"    width: 2px;\n"
"    height: 2px;\n"
"}\n"
"QSplitter::handle:hover {\n"
"    background-color: #7c6cff;\n"
"}")
        self.mainSplitter.setOrientation(Qt.Orientation.Horizontal)
        self.mainModeTabWidget = QTabWidget(self.mainSplitter)
        self.mainModeTabWidget.setObjectName(u"mainModeTabWidget")
        self.mainModeTabWidget.setEnabled(True)
        self.mainModeTabWidget.setMinimumSize(QSize(400, 0))
        self.mainModeTabWidget.setStyleSheet(u"QTabWidget::pane {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    border-radius: 16px;\n"
"}\n"
"QTabBar::tab {\n"
"    background-color: #171a23;\n"
"    color: #9aa2b8;\n"
"    border: 1px solid #262b3a;\n"
"    border-bottom: none;\n"
"    border-top-left-radius: 10px;\n"
"    border-top-right-radius: 10px;\n"
"    padding: 10px 24px;\n"
"    margin-right: 4px;\n"
"    font-weight: 500;\n"
"    font-size: 13px;\n"
"}\n"
"QTabBar::tab:selected {\n"
"    background-color: #1d212c;\n"
"    color: #f4f5f8;\n"
"    border-color: #3d4356;\n"
"    border-bottom: 2px solid #7c6cff;\n"
"}\n"
"QTabBar::tab:hover:!selected {\n"
"    background-color: #191c26;\n"
"    color: #cdd2e0;\n"
"}")
        self.settingsTabPage = QWidget()
        self.settingsTabPage.setObjectName(u"settingsTabPage")
        self.mainModeTabWidget.addTab(self.settingsTabPage, "")
        self.generationTabPage = QWidget()
        self.generationTabPage.setObjectName(u"generationTabPage")
        self.helpTabLayout = QVBoxLayout(self.generationTabPage)
        self.helpTabLayout.setObjectName(u"helpTabLayout")
        self.helpTabLayout.setContentsMargins(16, 16, 16, 16)
        self.helpBrowser = QTextBrowser(self.generationTabPage)
        self.helpBrowser.setObjectName(u"helpBrowser")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.helpBrowser.sizePolicy().hasHeightForWidth())
        self.helpBrowser.setSizePolicy(sizePolicy)
        self.helpBrowser.setStyleSheet(u"QTextBrowser {\n"
"    background-color: #171a23;\n"
"    border: 1px solid #262b3a;\n"
"    border-radius: 10px;\n"
"    padding: 16px;\n"
"    font-family: \"Segoe UI\", \"Malgun Gothic\", sans-serif;\n"
"    font-size: 13px;\n"
"    color: #cdd2e0;\n"
"}\n"
"QTextBrowser QScrollBar:vertical { background-color: #171a23; width: 10px; border-radius: 5px; }\n"
"QTextBrowser QScrollBar::handle:vertical { background-color: #3d4356; border-radius: 5px; min-height: 30px; }\n"
"QTextBrowser QScrollBar::handle:vertical:hover { background-color: #565d72; }\n"
"QTextBrowser QScrollBar::add-line:vertical, QTextBrowser QScrollBar::sub-line:vertical { height: 0px; }")
        self.helpBrowser.setOpenExternalLinks(True)

        self.helpTabLayout.addWidget(self.helpBrowser)

        self.mainModeTabWidget.addTab(self.generationTabPage, "")
        self.mainSplitter.addWidget(self.mainModeTabWidget)
        self.resultPanel = QGroupBox(self.centralWidget)
        self.resultPanel.setObjectName(u"resultPanel")
        self.resultPanel.setGeometry(QRect(1260, 80, 391, 581))
        self.resultPanel.setMinimumSize(QSize(250, 0))
        self.resultPanel.setStyleSheet(u"QGroupBox {\n"
"    background-color: #171a23;\n"
"    border: 1px solid #262b3a;\n"
"    border-radius: 16px;\n"
"    margin-top: 8px;\n"
"    padding: 12px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 16px;\n"
"    padding: 0 8px;\n"
"    background-color: #171a23;\n"
"    color: #f4f5f8;\n"
"    font-size: 20px;\n"
"    font-weight: 600;\n"
"}")
        self.gridLayout = QGridLayout(self.resultPanel)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(2, -1, 2, 2)
        self.previewLabel = QLabel(self.resultPanel)
        self.previewLabel.setObjectName(u"previewLabel")
        self.previewLabel.setMinimumSize(QSize(200, 288))
        self.previewLabel.setFont(font)
        self.previewLabel.setStyleSheet(u"background-color: #0e1016;\n"
"border: 1px solid #262b3a;\n"
"border-radius: 12px;\n"
"color: #565d72;\n"
"padding: 20px;")
        self.previewLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.previewLabel.setWordWrap(True)

        self.gridLayout.addWidget(self.previewLabel, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.openOutputFolderButton = QPushButton(self.resultPanel)
        self.openOutputFolderButton.setObjectName(u"openOutputFolderButton")
        self.openOutputFolderButton.setMinimumSize(QSize(100, 32))
        self.openOutputFolderButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    color: #cdd2e0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 8px;\n"
"    padding: 6px 16px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton:hover { background-color: #262b3a; border-color: #7c6cff; color: #f4f5f8; }\n"
"QPushButton:pressed { background-color: #14161f; }\n"
"QPushButton:disabled { background-color: #14161f; color: #565d72; border-color: #202430; }")

        self.horizontalLayout.addWidget(self.openOutputFolderButton)

        self.saveImageButton = QPushButton(self.resultPanel)
        self.saveImageButton.setObjectName(u"saveImageButton")
        self.saveImageButton.setMinimumSize(QSize(100, 32))
        self.saveImageButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    color: #cdd2e0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 8px;\n"
"    padding: 6px 16px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton:hover { background-color: #262b3a; border-color: #7c6cff; color: #f4f5f8; }\n"
"QPushButton:pressed { background-color: #14161f; }\n"
"QPushButton:disabled { background-color: #14161f; color: #565d72; border-color: #202430; }")

        self.horizontalLayout.addWidget(self.saveImageButton)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 2)
        self.executionPanel = QGroupBox(self.centralWidget)
        self.executionPanel.setObjectName(u"executionPanel")
        self.executionPanel.setGeometry(QRect(860, 500, 391, 151))
        self.executionPanel.setStyleSheet(u"QGroupBox {\n"
"    background-color: #171a23;\n"
"    border: 1px solid #262b3a;\n"
"    border-radius: 16px;\n"
"    margin-top: 8px;\n"
"    padding: 16px 20px 20px 20px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 16px;\n"
"    padding: 0 8px;\n"
"    background-color: #171a23;\n"
"    color: #f4f5f8;\n"
"    font-size: 20px;\n"
"    font-weight: 600;\n"
"}")
        self.executionLayout = QVBoxLayout(self.executionPanel)
        self.executionLayout.setSpacing(0)
        self.executionLayout.setObjectName(u"executionLayout")
        self.executionLayout.setContentsMargins(0, 6, 0, 0)
        self.progressStatusLayout = QHBoxLayout()
        self.progressStatusLayout.setObjectName(u"progressStatusLayout")
        self.progressStatusLabel = QLabel(self.executionPanel)
        self.progressStatusLabel.setObjectName(u"progressStatusLabel")
        self.progressStatusLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #9aa2b8;\n"
"font-size: 12px;")

        self.progressStatusLayout.addWidget(self.progressStatusLabel)

        self.progressStatusSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.progressStatusLayout.addItem(self.progressStatusSpacer)

        self.elapsedLabel = QLabel(self.executionPanel)
        self.elapsedLabel.setObjectName(u"elapsedLabel")
        self.elapsedLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #9aa2b8;\n"
"font-size: 12px;")
        self.elapsedLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.progressStatusLayout.addWidget(self.elapsedLabel)


        self.executionLayout.addLayout(self.progressStatusLayout)

        self.progressBarLayout = QHBoxLayout()
        self.progressBarLayout.setObjectName(u"progressBarLayout")
        self.progressBar = QProgressBar(self.executionPanel)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy1)
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"    background-color: #262b3a;\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    height: 12px;\n"
"    text-align: center;\n"
"    color: #e8eaf0;\n"
"}\n"
"QProgressBar::chunk { background-color: #7c6cff; border-radius: 10px; }\n"
"QProgressBar[value=\"100\"]::chunk { background-color: #22c55e; }")
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.progressBarLayout.addWidget(self.progressBar)

        self.progressPercentLabel = QLabel(self.executionPanel)
        self.progressPercentLabel.setObjectName(u"progressPercentLabel")
        self.progressPercentLabel.setStyleSheet(u"background-color: transparent;\n"
"font-size: 22px;\n"
"font-weight: 700;\n"
"color: #f4f5f8;")
        self.progressPercentLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.progressBarLayout.addWidget(self.progressPercentLabel)


        self.executionLayout.addLayout(self.progressBarLayout)

        self.generateStopLayout = QHBoxLayout()
        self.generateStopLayout.setObjectName(u"generateStopLayout")
        self.generateButton = QPushButton(self.executionPanel)
        self.generateButton.setObjectName(u"generateButton")
        sizePolicy.setHeightForWidth(self.generateButton.sizePolicy().hasHeightForWidth())
        self.generateButton.setSizePolicy(sizePolicy)
        self.generateButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #7c6cff;\n"
"    color: #ffffff;\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    padding: 12px 24px;\n"
"    font-size: 15px;\n"
"    font-weight: 600;\n"
"}\n"
"QPushButton:hover { background-color: #6a58f5; }\n"
"QPushButton:pressed { background-color: #5847d8; }\n"
"QPushButton:disabled { background-color: #322b5c; color: #8a83b8; }")
        icon = QIcon()
        icon.addFile(u":/newPrefix1/play.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.generateButton.setIcon(icon)
        self.generateButton.setCheckable(False)
        self.generateButton.setAutoDefault(False)

        self.generateStopLayout.addWidget(self.generateButton)

        self.stopButton = QPushButton(self.executionPanel)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.stopButton.sizePolicy().hasHeightForWidth())
        self.stopButton.setSizePolicy(sizePolicy2)
        self.stopButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    color: #fb7185;\n"
"    border: 1px solid #4a2530;\n"
"    border-radius: 8px;\n"
"    padding: 6px 16px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton:hover { background-color: #2a151a; border-color: #f0455c; }\n"
"QPushButton:disabled { background-color: #14161f; color: #565d72; border-color: #202430; }")
        icon1 = QIcon()
        icon1.addFile(u":/newPrefix1/stop-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.stopButton.setIcon(icon1)

        self.generateStopLayout.addWidget(self.stopButton)


        self.executionLayout.addLayout(self.generateStopLayout)

        self.executionLayout.setStretch(1, 1)
        self.executionLayout.setStretch(2, 2)
        self.exitButton = QPushButton(self.centralWidget)
        self.exitButton.setObjectName(u"exitButton")
        self.exitButton.setGeometry(QRect(1530, 10, 121, 41))
        sizePolicy.setHeightForWidth(self.exitButton.sizePolicy().hasHeightForWidth())
        self.exitButton.setSizePolicy(sizePolicy)
        self.exitButton.setMinimumSize(QSize(120, 32))
        self.exitButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    color: #cdd2e0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 8px;\n"
"    padding: 6px 16px;\n"
"    font-size: 18px;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton:hover { background-color: #262b3a; border-color: #7c6cff; color: #f4f5f8; }\n"
"QPushButton:pressed { background-color: #14161f; }\n"
"QPushButton:disabled { background-color: #14161f; color: #565d72; border-color: #202430; }")
        icon2 = QIcon()
        icon2.addFile(u":/newPrefix1/off-2.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exitButton.setIcon(icon2)
        self.logGroupBox = QGroupBox(self.centralWidget)
        self.logGroupBox.setObjectName(u"logGroupBox")
        self.logGroupBox.setGeometry(QRect(20, 760, 381, 211))
        sizePolicy.setHeightForWidth(self.logGroupBox.sizePolicy().hasHeightForWidth())
        self.logGroupBox.setSizePolicy(sizePolicy)
        self.logGroupBox.setMinimumSize(QSize(381, 100))
        self.logGroupBox.setMaximumSize(QSize(16777215, 16777215))
        self.logGroupBox.setStyleSheet(u"QGroupBox {\n"
"    background-color: #171a23;\n"
"    border: 1px solid #262b3a;\n"
"    border-radius: 16px;\n"
"    margin-top: 8px;\n"
"    padding: 16px 20px 20px 20px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 16px;\n"
"    padding: 0 8px;\n"
"    background-color: #171a23;\n"
"    color: #f4f5f8;\n"
"    font-size: 20px;\n"
"    font-weight: 600;\n"
"}")
        self.logGroupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logTextEdit = QPlainTextEdit(self.logGroupBox)
        self.logTextEdit.setObjectName(u"logTextEdit")
        self.logTextEdit.setGeometry(QRect(11, 25, 361, 171))
        self.logTextEdit.setStyleSheet(u"QPlainTextEdit {\n"
"    background-color: #0a0b10;\n"
"    color: #a9b0c4;\n"
"    border: 1px solid #1c1f29;\n"
"    border-radius: 12px;\n"
"    padding: 16px 18px;\n"
"    font-family: \"Cascadia Code\", \"Consolas\", \"Monaco\", monospace;\n"
"    font-size: 13px;\n"
"}\n"
"QPlainTextEdit:focus { border-color: #3d4356; background-color: #0a0b10; }")
        self.logTextEdit.setReadOnly(True)
        self.resetButton = QPushButton(self.logGroupBox)
        self.resetButton.setObjectName(u"resetButton")
        self.resetButton.setGeometry(QRect(282, 25, 91, 32))
        sizePolicy.setHeightForWidth(self.resetButton.sizePolicy().hasHeightForWidth())
        self.resetButton.setSizePolicy(sizePolicy)
        self.resetButton.setMinimumSize(QSize(80, 32))
        self.resetButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    color: #cdd2e0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 8px;\n"
"    padding: 6px 16px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton:hover { background-color: #262b3a; border-color: #7c6cff; color: #f4f5f8; }\n"
"QPushButton:pressed { background-color: #14161f; }\n"
"QPushButton:disabled { background-color: #14161f; color: #565d72; border-color: #202430; }")
        self.promptPanel = QGroupBox(self.centralWidget)
        self.promptPanel.setObjectName(u"promptPanel")
        self.promptPanel.setGeometry(QRect(420, 670, 511, 351))
        self.promptPanel.setStyleSheet(u"QGroupBox {\n"
"    background-color: #171a23;\n"
"    border: 1px solid #262b3a;\n"
"    border-radius: 16px;\n"
"    margin-top: 8px;\n"
"    padding: 16px 20px 20px 20px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 16px;\n"
"    padding: 0 8px;\n"
"    background-color: #171a23;\n"
"    color: #f4f5f8;\n"
"    font-size: 20px;\n"
"    font-weight: 600;\n"
"}")
        self.gridLayout_3 = QGridLayout(self.promptPanel)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(0)
        self.gridLayout_3.setVerticalSpacing(6)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.positivePromptHeaderLayout = QHBoxLayout()
        self.positivePromptHeaderLayout.setObjectName(u"positivePromptHeaderLayout")
        self.positivePromptLabel = QLabel(self.promptPanel)
        self.positivePromptLabel.setObjectName(u"positivePromptLabel")
        self.positivePromptLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")

        self.positivePromptHeaderLayout.addWidget(self.positivePromptLabel)

        self.positivePromptHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.positivePromptHeaderLayout.addItem(self.positivePromptHeaderSpacer)

        self.positivePromptCounterLabel = QLabel(self.promptPanel)
        self.positivePromptCounterLabel.setObjectName(u"positivePromptCounterLabel")
        self.positivePromptCounterLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #6b7288;\n"
"font-size: 12px;")
        self.positivePromptCounterLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.positivePromptHeaderLayout.addWidget(self.positivePromptCounterLabel)


        self.gridLayout_3.addLayout(self.positivePromptHeaderLayout, 0, 0, 1, 1)

        self.positivePromptEdit = QPlainTextEdit(self.promptPanel)
        self.positivePromptEdit.setObjectName(u"positivePromptEdit")
        self.positivePromptEdit.setStyleSheet(u"QPlainTextEdit {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 8px 14px;\n"
"    selection-background-color: #7c6cff;\n"
"    selection-color: #ffffff;\n"
"}\n"
"QPlainTextEdit:hover { border-color: #3d4356; }\n"
"QPlainTextEdit:focus { border-color: #7c6cff; background-color: #14161f; }")

        self.gridLayout_3.addWidget(self.positivePromptEdit, 1, 0, 1, 1)

        self.negativePromptHeaderLayout = QHBoxLayout()
        self.negativePromptHeaderLayout.setObjectName(u"negativePromptHeaderLayout")
        self.negativePromptLabel = QLabel(self.promptPanel)
        self.negativePromptLabel.setObjectName(u"negativePromptLabel")
        self.negativePromptLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")

        self.negativePromptHeaderLayout.addWidget(self.negativePromptLabel)

        self.negativePromptHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.negativePromptHeaderLayout.addItem(self.negativePromptHeaderSpacer)

        self.negativePromptCounterLabel = QLabel(self.promptPanel)
        self.negativePromptCounterLabel.setObjectName(u"negativePromptCounterLabel")
        self.negativePromptCounterLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #6b7288;\n"
"font-size: 12px;")
        self.negativePromptCounterLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.negativePromptHeaderLayout.addWidget(self.negativePromptCounterLabel)


        self.gridLayout_3.addLayout(self.negativePromptHeaderLayout, 2, 0, 1, 1)

        self.negativePromptEdit = QPlainTextEdit(self.promptPanel)
        self.negativePromptEdit.setObjectName(u"negativePromptEdit")
        self.negativePromptEdit.setMaximumSize(QSize(16777215, 80))
        self.negativePromptEdit.setStyleSheet(u"QPlainTextEdit {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 8px 14px;\n"
"    selection-background-color: #7c6cff;\n"
"    selection-color: #ffffff;\n"
"}\n"
"QPlainTextEdit:hover { border-color: #3d4356; }\n"
"QPlainTextEdit:focus { border-color: #7c6cff; background-color: #14161f; }")

        self.gridLayout_3.addWidget(self.negativePromptEdit, 3, 0, 1, 1)

        self.enhancePromptHeaderLayout = QHBoxLayout()
        self.enhancePromptHeaderLayout.setObjectName(u"enhancePromptHeaderLayout")
        self.enhancePromptLabel = QLabel(self.promptPanel)
        self.enhancePromptLabel.setObjectName(u"enhancePromptLabel")
        self.enhancePromptLabel.setFont(font)
        self.enhancePromptLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")

        self.enhancePromptHeaderLayout.addWidget(self.enhancePromptLabel)

        self.enhancePromptHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.enhancePromptHeaderLayout.addItem(self.enhancePromptHeaderSpacer)

        self.enhancePromptButton = QPushButton(self.promptPanel)
        self.enhancePromptButton.setObjectName(u"enhancePromptButton")
        self.enhancePromptButton.setMinimumSize(QSize(0, 28))
        self.enhancePromptButton.setMaximumSize(QSize(16777215, 28))
        self.enhancePromptButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #38bdf8;\n"
"    color: #0b1220;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 4px 12px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover { background-color: #0ea5e9; }\n"
"QPushButton:pressed { background-color: #0284c7; }\n"
"QPushButton:disabled { background-color: #23324a; color: #5c6b85; }")
        icon3 = QIcon()
        icon3.addFile(u":/newPrefix1/sparkel.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.enhancePromptButton.setIcon(icon3)

        self.enhancePromptHeaderLayout.addWidget(self.enhancePromptButton)

        self.enhancePromptCounterLabel = QLabel(self.promptPanel)
        self.enhancePromptCounterLabel.setObjectName(u"enhancePromptCounterLabel")
        self.enhancePromptCounterLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #6b7288;\n"
"font-size: 12px;")
        self.enhancePromptCounterLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.enhancePromptHeaderLayout.addWidget(self.enhancePromptCounterLabel)


        self.gridLayout_3.addLayout(self.enhancePromptHeaderLayout, 4, 0, 1, 1)

        self.enhancePromptEdit = QPlainTextEdit(self.promptPanel)
        self.enhancePromptEdit.setObjectName(u"enhancePromptEdit")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.enhancePromptEdit.sizePolicy().hasHeightForWidth())
        self.enhancePromptEdit.setSizePolicy(sizePolicy3)
        self.enhancePromptEdit.setMaximumSize(QSize(16777215, 16777215))
        self.enhancePromptEdit.setStyleSheet(u"QPlainTextEdit {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 8px 14px;\n"
"    selection-background-color: #7c6cff;\n"
"    selection-color: #ffffff;\n"
"}\n"
"QPlainTextEdit:hover { border-color: #3d4356; }\n"
"QPlainTextEdit:focus { border-color: #7c6cff; background-color: #14161f; }")

        self.gridLayout_3.addWidget(self.enhancePromptEdit, 5, 0, 1, 1)

        self.gridLayout_3.setRowStretch(1, 1)
        self.layoutWidget0 = QWidget(self.centralWidget)
        self.layoutWidget0.setObjectName(u"layoutWidget0")
        self.layoutWidget0.setGeometry(QRect(450, 1080, 511, 34))
        self.actionButtonLayout = QHBoxLayout(self.layoutWidget0)
        self.actionButtonLayout.setObjectName(u"actionButtonLayout")
        self.actionButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.restoreDefaultsButton = QPushButton(self.layoutWidget0)
        self.restoreDefaultsButton.setObjectName(u"restoreDefaultsButton")
        self.restoreDefaultsButton.setMinimumSize(QSize(100, 32))
        self.restoreDefaultsButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    color: #cdd2e0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 8px;\n"
"    padding: 6px 16px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton:hover { background-color: #262b3a; border-color: #7c6cff; color: #f4f5f8; }\n"
"QPushButton:pressed { background-color: #14161f; }\n"
"QPushButton:disabled { background-color: #14161f; color: #565d72; border-color: #202430; }")

        self.actionButtonLayout.addWidget(self.restoreDefaultsButton)

        self.loadConfigButton = QPushButton(self.layoutWidget0)
        self.loadConfigButton.setObjectName(u"loadConfigButton")
        self.loadConfigButton.setMinimumSize(QSize(100, 32))
        self.loadConfigButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    color: #cdd2e0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 8px;\n"
"    padding: 6px 16px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton:hover { background-color: #262b3a; border-color: #7c6cff; color: #f4f5f8; }\n"
"QPushButton:pressed { background-color: #14161f; }\n"
"QPushButton:disabled { background-color: #14161f; color: #565d72; border-color: #202430; }")

        self.actionButtonLayout.addWidget(self.loadConfigButton)

        self.saveConfigButton = QPushButton(self.layoutWidget0)
        self.saveConfigButton.setObjectName(u"saveConfigButton")
        self.saveConfigButton.setMinimumSize(QSize(100, 32))
        self.saveConfigButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    color: #cdd2e0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 8px;\n"
"    padding: 6px 16px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton:hover { background-color: #262b3a; border-color: #7c6cff; color: #f4f5f8; }\n"
"QPushButton:pressed { background-color: #14161f; }\n"
"QPushButton:disabled { background-color: #14161f; color: #565d72; border-color: #202430; }")

        self.actionButtonLayout.addWidget(self.saveConfigButton)

        self.sidebar_frame = QFrame(self.centralWidget)
        self.sidebar_frame.setObjectName(u"sidebar_frame")
        self.sidebar_frame.setGeometry(QRect(-1, 0, 491, 721))
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.sidebar_frame.sizePolicy().hasHeightForWidth())
        self.sidebar_frame.setSizePolicy(sizePolicy4)
        self.sidebar_frame.setMinimumSize(QSize(55, 0))
        self.sidebar_frame.setMaximumSize(QSize(5555, 16777215))
        self.sidebar_frame.setStyleSheet(u"background-color: #b9b9b9;\n"
"border-top-right-radius: 25px;\n"
"border-bottom-right-radius: 25px;\n"
"border: 3px solid #ffffff")
        self.sidebar_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.pushButton = QPushButton(self.sidebar_frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 30, 31, 31))
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/newPrefix1/network-success.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon4)
        self.pushButton.setIconSize(QSize(26, 26))
        self.connectionPanel = QGroupBox(self.sidebar_frame)
        self.connectionPanel.setObjectName(u"connectionPanel")
        self.connectionPanel.setGeometry(QRect(90, 40, 381, 591))
        self.connectionPanel.setStyleSheet(u"QGroupBox {\n"
"    background-color: #171a23;\n"
"    border: 1px solid #262b3a;\n"
"    border-radius: 16px;\n"
"    margin-top: 8px;\n"
"    padding: 24px 20px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 16px;\n"
"    padding: 0 8px;\n"
"    background-color: #171a23;\n"
"    color: #f4f5f8;\n"
"    font-size: 20px;\n"
"    font-weight: 600;\n"
"}")
        self.lmgroupBox = QGroupBox(self.connectionPanel)
        self.lmgroupBox.setObjectName(u"lmgroupBox")
        self.lmgroupBox.setGeometry(QRect(9, 26, 351, 201))
        self.lmgroupBox.setStyleSheet(u"QGroupBox {\n"
"    background-color: #1d212c;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 16px;\n"
"    margin-top: 8px;\n"
"    padding: 18px 20px 20px 20px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 16px;\n"
"    padding: 0 8px;\n"
"    background-color: #1d212c;\n"
"    color: #f4f5f8;\n"
"    font-size: 20px;\n"
"    font-weight: 600;\n"
"}")
        self.lmAddressLabel = QLabel(self.lmgroupBox)
        self.lmAddressLabel.setObjectName(u"lmAddressLabel")
        self.lmAddressLabel.setGeometry(QRect(13, 45, 91, 20))
        self.lmAddressLabel.setStyleSheet(u"background-color: transparent;\n"
"font-size: 12px;\n"
"color: #6b7288;\n"
"font-family: \"Cascadia Code\", \"Consolas\", monospace;\n"
"    border: none;\n"
"    background-color: transparent;")
        self.lmUrlEdit = QLineEdit(self.lmgroupBox)
        self.lmUrlEdit.setObjectName(u"lmUrlEdit")
        self.lmUrlEdit.setGeometry(QRect(13, 70, 221, 41))
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lmUrlEdit.sizePolicy().hasHeightForWidth())
        self.lmUrlEdit.setSizePolicy(sizePolicy5)
        self.lmUrlEdit.setMinimumSize(QSize(0, 32))
        self.lmUrlEdit.setStyleSheet(u"QLineEdit {\n"
"    background-color: #12141c;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 10px 16px;\n"
"    font-family: \"Cascadia Code\", \"Consolas\", monospace;\n"
"    font-size: 14px;\n"
"    color: #cdd2e0;\n"
"    selection-background-color: #7c6cff;\n"
"    selection-color: #ffffff;\n"
"}\n"
"QLineEdit:hover { border-color: #3d4356; }\n"
"QLineEdit:focus { border-color: #7c6cff; background-color: #14161f; }")
        self.lmTitleLabel = QLabel(self.lmgroupBox)
        self.lmTitleLabel.setObjectName(u"lmTitleLabel")
        self.lmTitleLabel.setGeometry(QRect(109, 15, 151, 25))
        font1 = QFont()
        font1.setFamilies([u"Cascadia Code"])
        self.lmTitleLabel.setFont(font1)
        self.lmTitleLabel.setStyleSheet(u"background-color: transparent;\n"
"font-size: 16px;\n"
"color: #ffffff;\n"
"font-family: \"Cascadia Code\", \"Consolas\", monospace;\n"
"    border: none;\n"
"    background-color: transparent;")
        self.lmTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lmStatusLabel = QLabel(self.lmgroupBox)
        self.lmStatusLabel.setObjectName(u"lmStatusLabel")
        self.lmStatusLabel.setGeometry(QRect(230, 40, 121, 31))
        self.lmStatusLabel.setStyleSheet(u"QLabel {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    padding: 4px 14px 4px 10px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    color: #e8eaf0;\n"
"}\n"
"QLabel[text*=\"\uc5f0\uacb0 \uc131\uacf5\"] { color: #4ade80; }\n"
"QLabel[text*=\"\uc5f0\uacb0 \uc2e4\ud328\"] { color: #fb7185; }")
        self.lmStatusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lmCheckButton = QPushButton(self.lmgroupBox)
        self.lmCheckButton.setObjectName(u"lmCheckButton")
        self.lmCheckButton.setGeometry(QRect(240, 70, 101, 41))
        self.lmCheckButton.setMinimumSize(QSize(80, 32))
        self.lmCheckButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    color: #cdd2e0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 8px;\n"
"    padding: 6px 16px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton:hover { background-color: #262b3a; border-color: #7c6cff; color: #f4f5f8; }\n"
"QPushButton:pressed { background-color: #14161f; }\n"
"QPushButton:disabled { background-color: #14161f; color: #565d72; border-color: #202430; }")
        self.lmModelLabel = QLabel(self.lmgroupBox)
        self.lmModelLabel.setObjectName(u"lmModelLabel")
        self.lmModelLabel.setGeometry(QRect(11, 121, 78, 16))
        self.lmModelLabel.setStyleSheet(u"background-color: transparent;\n"
"font-size: 12px;\n"
"color: #6b7288;\n"
"font-family: \"Cascadia Code\", \"Consolas\", monospace;\n"
"    border: none;\n"
"    background-color: transparent;")
        self.lmModelCombo = QComboBox(self.lmgroupBox)
        self.lmModelCombo.setObjectName(u"lmModelCombo")
        self.lmModelCombo.setGeometry(QRect(11, 149, 104, 42))
        self.lmModelCombo.setMinimumSize(QSize(0, 42))
        self.lmModelCombo.setStyleSheet(u"QComboBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 8px 14px;\n"
"    min-height: 24px;\n"
"}\n"
"QComboBox:hover { border-color: #3d4356; }\n"
"QComboBox:focus { border-color: #7c6cff; }\n"
"QComboBox::drop-down { border: none; width: 30px; background: transparent; }\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"    width: 0;\n"
"    height: 0;\n"
"    border-left: 6px solid transparent;\n"
"    border-right: 6px solid transparent;\n"
"    border-top: 6px solid #9aa2b8;\n"
"    margin: 0px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1d212c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #3d4356;\n"
"    border-radius: 10px;\n"
"    padding: 4px;\n"
"    outline: none;\n"
"    selection-background-color: #2a2440;\n"
"    selection-color: #cdc4ff;\n"
"}\n"
"QComboBox QAbstractItemView::item { padding: 6px 8px; border-radius: 6px; }\n"
"QComboBox QAbstractItemView::item:hover { ba"
                        "ckground-color: #262b3a; }")
        self.ComfygroupBox = QGroupBox(self.connectionPanel)
        self.ComfygroupBox.setObjectName(u"ComfygroupBox")
        self.ComfygroupBox.setGeometry(QRect(10, 220, 351, 301))
        self.ComfygroupBox.setStyleSheet(u"QGroupBox {\n"
"    background-color: #1d212c;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 16px;\n"
"    margin-top: 8px;\n"
"    padding: 18px 20px 20px 20px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 16px;\n"
"    padding: 0 8px;\n"
"    background-color: #1d212c;\n"
"    color: #f4f5f8;\n"
"    font-size: 20px;\n"
"    font-weight: 600;\n"
"}")
        self.comfyAddressLabel = QLabel(self.ComfygroupBox)
        self.comfyAddressLabel.setObjectName(u"comfyAddressLabel")
        self.comfyAddressLabel.setGeometry(QRect(10, 54, 91, 20))
        self.comfyAddressLabel.setStyleSheet(u"background-color: transparent;\n"
"font-size: 12px;\n"
"color: #6b7288;\n"
"font-family: \"Cascadia Code\", \"Consolas\", monospace;\n"
"    border: none;\n"
"    background-color: transparent;")
        self.comfyUrlEdit = QLineEdit(self.ComfygroupBox)
        self.comfyUrlEdit.setObjectName(u"comfyUrlEdit")
        self.comfyUrlEdit.setGeometry(QRect(10, 77, 221, 41))
        sizePolicy5.setHeightForWidth(self.comfyUrlEdit.sizePolicy().hasHeightForWidth())
        self.comfyUrlEdit.setSizePolicy(sizePolicy5)
        self.comfyUrlEdit.setMinimumSize(QSize(0, 32))
        self.comfyUrlEdit.setStyleSheet(u"QLineEdit {\n"
"    background-color: #12141c;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 10px 16px;\n"
"    font-family: \"Cascadia Code\", \"Consolas\", monospace;\n"
"    font-size: 14px;\n"
"    color: #cdd2e0;\n"
"    selection-background-color: #7c6cff;\n"
"    selection-color: #ffffff;\n"
"}\n"
"QLineEdit:hover { border-color: #3d4356; }\n"
"QLineEdit:focus { border-color: #7c6cff; background-color: #14161f; }")
        self.comfyPathLabel = QLabel(self.ComfygroupBox)
        self.comfyPathLabel.setObjectName(u"comfyPathLabel")
        self.comfyPathLabel.setGeometry(QRect(10, 192, 91, 20))
        self.comfyPathLabel.setStyleSheet(u"background-color: transparent;\n"
"font-size: 12px;\n"
"color: #6b7288;\n"
"font-family: \"Cascadia Code\", \"Consolas\", monospace;\n"
"    border: none;\n"
"    background-color: transparent;")
        self.comfyModelPathEdit = QLineEdit(self.ComfygroupBox)
        self.comfyModelPathEdit.setObjectName(u"comfyModelPathEdit")
        self.comfyModelPathEdit.setGeometry(QRect(10, 214, 331, 41))
        sizePolicy5.setHeightForWidth(self.comfyModelPathEdit.sizePolicy().hasHeightForWidth())
        self.comfyModelPathEdit.setSizePolicy(sizePolicy5)
        self.comfyModelPathEdit.setMinimumSize(QSize(0, 32))
        self.comfyModelPathEdit.setStyleSheet(u"QLineEdit {\n"
"    background-color: #12141c;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 10px 16px;\n"
"    font-family: \"Cascadia Code\", \"Consolas\", monospace;\n"
"    font-size: 14px;\n"
"    color: #cdd2e0;\n"
"    selection-background-color: #7c6cff;\n"
"    selection-color: #ffffff;\n"
"}\n"
"QLineEdit:hover { border-color: #3d4356; }\n"
"QLineEdit:focus { border-color: #7c6cff; background-color: #14161f; }")
        self.comfyStatusLabel = QLabel(self.ComfygroupBox)
        self.comfyStatusLabel.setObjectName(u"comfyStatusLabel")
        self.comfyStatusLabel.setGeometry(QRect(227, 46, 121, 31))
        self.comfyStatusLabel.setStyleSheet(u"QLabel {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    padding: 4px 14px 4px 10px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    color: #e8eaf0;\n"
"}\n"
"QLabel[text*=\"\uc5f0\uacb0 \uc131\uacf5\"] { color: #4ade80; }\n"
"QLabel[text*=\"\uc5f0\uacb0 \uc2e4\ud328\"] { color: #fb7185; }")
        self.comfyTitleLabel = QLabel(self.ComfygroupBox)
        self.comfyTitleLabel.setObjectName(u"comfyTitleLabel")
        self.comfyTitleLabel.setGeometry(QRect(100, 20, 121, 31))
        font2 = QFont()
        font2.setFamilies([u"Cascadia Code"])
        font2.setBold(True)
        self.comfyTitleLabel.setFont(font2)
        self.comfyTitleLabel.setStyleSheet(u"background-color: transparent;\n"
"font-size: 16px;\n"
"color: #ffffff;\n"
"font-family: \"Cascadia Code\", \"Consolas\", monospace;\n"
"    border: none;\n"
"    background-color: transparent;")
        self.comfyTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.comfyCheckButton = QPushButton(self.ComfygroupBox)
        self.comfyCheckButton.setObjectName(u"comfyCheckButton")
        self.comfyCheckButton.setGeometry(QRect(240, 78, 101, 41))
        self.comfyCheckButton.setMinimumSize(QSize(80, 32))
        self.comfyCheckButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    color: #cdd2e0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 8px;\n"
"    padding: 6px 16px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton:hover { background-color: #262b3a; border-color: #7c6cff; color: #f4f5f8; }\n"
"QPushButton:pressed { background-color: #14161f; }\n"
"QPushButton:disabled { background-color: #14161f; color: #565d72; border-color: #202430; }")
        self.modelPathStatusLabel = QLabel(self.ComfygroupBox)
        self.modelPathStatusLabel.setObjectName(u"modelPathStatusLabel")
        self.modelPathStatusLabel.setGeometry(QRect(10, 262, 100, 16))
        self.modelPathStatusLabel.setStyleSheet(u"background-color: transparent;\n"
"font-size: 12px;\n"
"color: #6b7288;\n"
"font-family: \"Cascadia Code\", \"Consolas\", monospace;\n"
"    border: none;\n"
"    background-color: transparent;")
        self.browseModelFolderButton = QPushButton(self.ComfygroupBox)
        self.browseModelFolderButton.setObjectName(u"browseModelFolderButton")
        self.browseModelFolderButton.setGeometry(QRect(253, 262, 86, 32))
        self.browseModelFolderButton.setMinimumSize(QSize(80, 32))
        self.browseModelFolderButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    color: #cdd2e0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 8px;\n"
"    padding: 6px 16px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton:hover { background-color: #262b3a; border-color: #7c6cff; color: #f4f5f8; }\n"
"QPushButton:pressed { background-color: #14161f; }\n"
"QPushButton:disabled { background-color: #14161f; color: #565d72; border-color: #202430; }")
        self.comfyModelLabel = QLabel(self.ComfygroupBox)
        self.comfyModelLabel.setObjectName(u"comfyModelLabel")
        self.comfyModelLabel.setGeometry(QRect(10, 123, 78, 16))
        self.comfyModelLabel.setStyleSheet(u"background-color: transparent;\n"
"font-size: 12px;\n"
"color: #6b7288;\n"
"font-family: \"Cascadia Code\", \"Consolas\", monospace;\n"
"    border: none;\n"
"    background-color: transparent;")
        self.comfyModelCombo = QComboBox(self.ComfygroupBox)
        self.comfyModelCombo.setObjectName(u"comfyModelCombo")
        self.comfyModelCombo.setGeometry(QRect(10, 150, 104, 42))
        self.comfyModelCombo.setMinimumSize(QSize(0, 42))
        self.comfyModelCombo.setStyleSheet(u"QComboBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 8px 14px;\n"
"    min-height: 24px;\n"
"}\n"
"QComboBox:hover { border-color: #3d4356; }\n"
"QComboBox:focus { border-color: #7c6cff; }\n"
"QComboBox::drop-down { border: none; width: 30px; background: transparent; }\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"    width: 0;\n"
"    height: 0;\n"
"    border-left: 6px solid transparent;\n"
"    border-right: 6px solid transparent;\n"
"    border-top: 6px solid #9aa2b8;\n"
"    margin: 0px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1d212c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #3d4356;\n"
"    border-radius: 10px;\n"
"    padding: 4px;\n"
"    outline: none;\n"
"    selection-background-color: #2a2440;\n"
"    selection-color: #cdc4ff;\n"
"}\n"
"QComboBox QAbstractItemView::item { padding: 6px 8px; border-radius: 6px; }\n"
"QComboBox QAbstractItemView::item:hover { ba"
                        "ckground-color: #262b3a; }")
        self.comfyAddressLabel.raise_()
        self.comfyPathLabel.raise_()
        self.comfyModelPathEdit.raise_()
        self.comfyStatusLabel.raise_()
        self.comfyTitleLabel.raise_()
        self.comfyUrlEdit.raise_()
        self.comfyCheckButton.raise_()
        self.generationPanel = QGroupBox(self.centralWidget)
        self.generationPanel.setObjectName(u"generationPanel")
        self.generationPanel.setGeometry(QRect(1060, 850, 441, 281))
        self.generationPanel.setStyleSheet(u"QGroupBox {\n"
"    background-color: #171a23;\n"
"    border: 1px solid #262b3a;\n"
"    border-radius: 16px;\n"
"    margin-top: 8px;\n"
"    padding: 16px 20px 20px 20px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 16px;\n"
"    padding: 0 8px;\n"
"    background-color: #171a23;\n"
"    color: #f4f5f8;\n"
"    font-size: 20px;\n"
"    font-weight: 600;\n"
"}")
        self.layoutWidget = QWidget(self.generationPanel)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 192, 414, 51))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.preset_512x512 = QPushButton(self.layoutWidget)
        self.preset_512x512.setObjectName(u"preset_512x512")
        sizePolicy2.setHeightForWidth(self.preset_512x512.sizePolicy().hasHeightForWidth())
        self.preset_512x512.setSizePolicy(sizePolicy2)
        self.preset_512x512.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 6px;\n"
"    padding: 4px 10px;\n"
"    font-size: 12px;\n"
"    font-weight: 500;\n"
"    color: #9aa2b8;\n"
"}\n"
"QPushButton:hover { background-color: #221e3d; border-color: #7c6cff; color: #f4f5f8; }")

        self.horizontalLayout_3.addWidget(self.preset_512x512)

        self.preset_768x768 = QPushButton(self.layoutWidget)
        self.preset_768x768.setObjectName(u"preset_768x768")
        sizePolicy2.setHeightForWidth(self.preset_768x768.sizePolicy().hasHeightForWidth())
        self.preset_768x768.setSizePolicy(sizePolicy2)
        self.preset_768x768.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 6px;\n"
"    padding: 4px 10px;\n"
"    font-size: 12px;\n"
"    font-weight: 500;\n"
"    color: #9aa2b8;\n"
"}\n"
"QPushButton:hover { background-color: #221e3d; border-color: #7c6cff; color: #f4f5f8; }")

        self.horizontalLayout_3.addWidget(self.preset_768x768)

        self.preset_1024x1024 = QPushButton(self.layoutWidget)
        self.preset_1024x1024.setObjectName(u"preset_1024x1024")
        sizePolicy2.setHeightForWidth(self.preset_1024x1024.sizePolicy().hasHeightForWidth())
        self.preset_1024x1024.setSizePolicy(sizePolicy2)
        self.preset_1024x1024.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 6px;\n"
"    padding: 4px 10px;\n"
"    font-size: 12px;\n"
"    font-weight: 500;\n"
"    color: #9aa2b8;\n"
"}\n"
"QPushButton:hover { background-color: #221e3d; border-color: #7c6cff; color: #f4f5f8; }")

        self.horizontalLayout_3.addWidget(self.preset_1024x1024)

        self.preset_832x1216 = QPushButton(self.layoutWidget)
        self.preset_832x1216.setObjectName(u"preset_832x1216")
        sizePolicy2.setHeightForWidth(self.preset_832x1216.sizePolicy().hasHeightForWidth())
        self.preset_832x1216.setSizePolicy(sizePolicy2)
        self.preset_832x1216.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 6px;\n"
"    padding: 4px 10px;\n"
"    font-size: 12px;\n"
"    font-weight: 500;\n"
"    color: #9aa2b8;\n"
"}\n"
"QPushButton:hover { background-color: #221e3d; border-color: #7c6cff; color: #f4f5f8; }")

        self.horizontalLayout_3.addWidget(self.preset_832x1216)

        self.preset_1216x832 = QPushButton(self.layoutWidget)
        self.preset_1216x832.setObjectName(u"preset_1216x832")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.preset_1216x832.sizePolicy().hasHeightForWidth())
        self.preset_1216x832.setSizePolicy(sizePolicy6)
        self.preset_1216x832.setStyleSheet(u"QPushButton {\n"
"    background-color: #1d212c;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 6px;\n"
"    padding: 4px 10px;\n"
"    font-size: 12px;\n"
"    font-weight: 500;\n"
"    color: #9aa2b8;\n"
"}\n"
"QPushButton:hover { background-color: #221e3d; border-color: #7c6cff; color: #f4f5f8; }")

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
        self.widthLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.widthLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.widthLabel)

        self.widthSpinBox = QSpinBox(self.layoutWidget1)
        self.widthSpinBox.setObjectName(u"widthSpinBox")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.widthSpinBox.sizePolicy().hasHeightForWidth())
        self.widthSpinBox.setSizePolicy(sizePolicy7)
        self.widthSpinBox.setMaximumSize(QSize(71, 40))
        self.widthSpinBox.setStyleSheet(u"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 20px;\n"
"}\n"
"QSpinBox:hover, QDoubleSpinBox:hover { border-color: #3d4356; }\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border-color: #7c6cff; }\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"    width: 16px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-bottom: 5px solid #9aa2b8;\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #9aa2b8;\n"
"}")
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
        self.heightLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.heightLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.heightLabel)

        self.heightSpinBox = QSpinBox(self.layoutWidget1)
        self.heightSpinBox.setObjectName(u"heightSpinBox")
        sizePolicy7.setHeightForWidth(self.heightSpinBox.sizePolicy().hasHeightForWidth())
        self.heightSpinBox.setSizePolicy(sizePolicy7)
        self.heightSpinBox.setMaximumSize(QSize(71, 40))
        self.heightSpinBox.setStyleSheet(u"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 20px;\n"
"}\n"
"QSpinBox:hover, QDoubleSpinBox:hover { border-color: #3d4356; }\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border-color: #7c6cff; }\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"    width: 16px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-bottom: 5px solid #9aa2b8;\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #9aa2b8;\n"
"}")
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
        self.stepsLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.stepsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.stepsLabel)

        self.stepsSpinBox = QSpinBox(self.layoutWidget1)
        self.stepsSpinBox.setObjectName(u"stepsSpinBox")
        sizePolicy7.setHeightForWidth(self.stepsSpinBox.sizePolicy().hasHeightForWidth())
        self.stepsSpinBox.setSizePolicy(sizePolicy7)
        self.stepsSpinBox.setMaximumSize(QSize(51, 40))
        self.stepsSpinBox.setStyleSheet(u"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 20px;\n"
"}\n"
"QSpinBox:hover, QDoubleSpinBox:hover { border-color: #3d4356; }\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border-color: #7c6cff; }\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"    width: 16px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-bottom: 5px solid #9aa2b8;\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #9aa2b8;\n"
"}")
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
        self.cfgLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.cfgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.cfgLabel)

        self.cfgSpinBox = QDoubleSpinBox(self.layoutWidget1)
        self.cfgSpinBox.setObjectName(u"cfgSpinBox")
        sizePolicy7.setHeightForWidth(self.cfgSpinBox.sizePolicy().hasHeightForWidth())
        self.cfgSpinBox.setSizePolicy(sizePolicy7)
        self.cfgSpinBox.setMaximumSize(QSize(51, 40))
        self.cfgSpinBox.setStyleSheet(u"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 20px;\n"
"}\n"
"QSpinBox:hover, QDoubleSpinBox:hover { border-color: #3d4356; }\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border-color: #7c6cff; }\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"    width: 16px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-bottom: 5px solid #9aa2b8;\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #9aa2b8;\n"
"}")
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
        self.seedLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.seedLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.seedLabel)

        self.seedSpinBox = QSpinBox(self.layoutWidget1)
        self.seedSpinBox.setObjectName(u"seedSpinBox")
        sizePolicy7.setHeightForWidth(self.seedSpinBox.sizePolicy().hasHeightForWidth())
        self.seedSpinBox.setSizePolicy(sizePolicy7)
        self.seedSpinBox.setMaximumSize(QSize(81, 40))
        self.seedSpinBox.setStyleSheet(u"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 20px;\n"
"}\n"
"QSpinBox:hover, QDoubleSpinBox:hover { border-color: #3d4356; }\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border-color: #7c6cff; }\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"    width: 16px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-bottom: 5px solid #9aa2b8;\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #9aa2b8;\n"
"}")
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
        self.denoiseLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.denoiseLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_8.addWidget(self.denoiseLabel)

        self.denoiseSpinBox = QDoubleSpinBox(self.layoutWidget1)
        self.denoiseSpinBox.setObjectName(u"denoiseSpinBox")
        sizePolicy7.setHeightForWidth(self.denoiseSpinBox.sizePolicy().hasHeightForWidth())
        self.denoiseSpinBox.setSizePolicy(sizePolicy7)
        self.denoiseSpinBox.setMaximumSize(QSize(51, 40))
        self.denoiseSpinBox.setStyleSheet(u"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 20px;\n"
"}\n"
"QSpinBox:hover, QDoubleSpinBox:hover { border-color: #3d4356; }\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border-color: #7c6cff; }\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"    width: 16px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-bottom: 5px solid #9aa2b8;\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #9aa2b8;\n"
"}")
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
        self.samplerLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.samplerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.samplerLabel)

        self.samplerComboBox = QComboBox(self.layoutWidget2)
        self.samplerComboBox.setObjectName(u"samplerComboBox")
        sizePolicy3.setHeightForWidth(self.samplerComboBox.sizePolicy().hasHeightForWidth())
        self.samplerComboBox.setSizePolicy(sizePolicy3)
        self.samplerComboBox.setMaximumSize(QSize(16777215, 16777215))
        self.samplerComboBox.setStyleSheet(u"QComboBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 8px 14px;\n"
"    min-height: 24px;\n"
"}\n"
"QComboBox:hover { border-color: #3d4356; }\n"
"QComboBox:focus { border-color: #7c6cff; }\n"
"QComboBox::drop-down { border: none; width: 30px; background: transparent; }\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"    width: 0;\n"
"    height: 0;\n"
"    border-left: 6px solid transparent;\n"
"    border-right: 6px solid transparent;\n"
"    border-top: 6px solid #9aa2b8;\n"
"    margin: 0px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1d212c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #3d4356;\n"
"    border-radius: 10px;\n"
"    padding: 4px;\n"
"    outline: none;\n"
"    selection-background-color: #2a2440;\n"
"    selection-color: #cdc4ff;\n"
"}\n"
"QComboBox QAbstractItemView::item { padding: 6px 8px; border-radius: 6px; }\n"
"QComboBox QAbstractItemView::item:hover { ba"
                        "ckground-color: #262b3a; }")

        self.verticalLayout_9.addWidget(self.samplerComboBox)


        self.horizontalLayout_4.addLayout(self.verticalLayout_9)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.schedulerLabel = QLabel(self.layoutWidget2)
        self.schedulerLabel.setObjectName(u"schedulerLabel")
        self.schedulerLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.schedulerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_10.addWidget(self.schedulerLabel)

        self.schedulerComboBox = QComboBox(self.layoutWidget2)
        self.schedulerComboBox.setObjectName(u"schedulerComboBox")
        sizePolicy3.setHeightForWidth(self.schedulerComboBox.sizePolicy().hasHeightForWidth())
        self.schedulerComboBox.setSizePolicy(sizePolicy3)
        self.schedulerComboBox.setMaximumSize(QSize(16777215, 16777215))
        self.schedulerComboBox.setStyleSheet(u"QComboBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 8px 14px;\n"
"    min-height: 24px;\n"
"}\n"
"QComboBox:hover { border-color: #3d4356; }\n"
"QComboBox:focus { border-color: #7c6cff; }\n"
"QComboBox::drop-down { border: none; width: 30px; background: transparent; }\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"    width: 0;\n"
"    height: 0;\n"
"    border-left: 6px solid transparent;\n"
"    border-right: 6px solid transparent;\n"
"    border-top: 6px solid #9aa2b8;\n"
"    margin: 0px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1d212c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #3d4356;\n"
"    border-radius: 10px;\n"
"    padding: 4px;\n"
"    outline: none;\n"
"    selection-background-color: #2a2440;\n"
"    selection-color: #cdc4ff;\n"
"}\n"
"QComboBox QAbstractItemView::item { padding: 6px 8px; border-radius: 6px; }\n"
"QComboBox QAbstractItemView::item:hover { ba"
                        "ckground-color: #262b3a; }")

        self.verticalLayout_10.addWidget(self.schedulerComboBox)


        self.horizontalLayout_4.addLayout(self.verticalLayout_10)

        self.facedetailerGroupBox = QGroupBox(self.centralWidget)
        self.facedetailerGroupBox.setObjectName(u"facedetailerGroupBox")
        self.facedetailerGroupBox.setGeometry(QRect(960, 700, 561, 130))
        self.facedetailerGroupBox.setStyleSheet(u"QGroupBox {\n"
"    background-color: #1d212c;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 16px;\n"
"    margin-top: 8px;\n"
"    padding: 18px 20px 20px 20px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 16px;\n"
"    padding: 0 8px;\n"
"    background-color: #1d212c;\n"
"    color: #f4f5f8;\n"
"    font-size: 20px;\n"
"    font-weight: 600;\n"
"}")
        self.facedetailerCheckBox = QCheckBox(self.facedetailerGroupBox)
        self.facedetailerCheckBox.setObjectName(u"facedetailerCheckBox")
        self.facedetailerCheckBox.setGeometry(QRect(20, 60, 34, 26))
        self.facedetailerCheckBox.setStyleSheet(u"QCheckBox::indicator { width: 22px; height: 22px; border-radius: 5px; }\n"
"QCheckBox::indicator:unchecked { background-color: #1d212c; border: 2px solid #3d4356; image: none; }\n"
"QCheckBox::indicator:unchecked:hover { background-color: #262b3a; border-color: #565d72; }\n"
"QCheckBox::indicator:checked { background-color: #7c6cff; border: 2px solid #6a58f5; image: url(assets/icons/facedetailer_check.svg); }\n"
"QCheckBox::indicator:checked:hover { background-color: #8f81ff; border-color: #6a58f5; }")
        self.layoutWidget3 = QWidget(self.facedetailerGroupBox)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(50, 40, 496, 70))
        self.horizontalLayout_5 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.facedetailerDenoiseLabel = QLabel(self.layoutWidget3)
        self.facedetailerDenoiseLabel.setObjectName(u"facedetailerDenoiseLabel")
        self.facedetailerDenoiseLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.facedetailerDenoiseLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_11.addWidget(self.facedetailerDenoiseLabel)

        self.facedetailerDenoiseSpinBox = QDoubleSpinBox(self.layoutWidget3)
        self.facedetailerDenoiseSpinBox.setObjectName(u"facedetailerDenoiseSpinBox")
        self.facedetailerDenoiseSpinBox.setStyleSheet(u"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 20px;\n"
"}\n"
"QSpinBox:hover, QDoubleSpinBox:hover { border-color: #3d4356; }\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border-color: #7c6cff; }\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"    width: 16px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-bottom: 5px solid #9aa2b8;\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #9aa2b8;\n"
"}")
        self.facedetailerDenoiseSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerDenoiseSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerDenoiseSpinBox.setMinimum(0.000000000000000)
        self.facedetailerDenoiseSpinBox.setMaximum(1.000000000000000)
        self.facedetailerDenoiseSpinBox.setSingleStep(0.050000000000000)
        self.facedetailerDenoiseSpinBox.setValue(0.400000000000000)

        self.verticalLayout_11.addWidget(self.facedetailerDenoiseSpinBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_11)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.facedetailerStepsLabel = QLabel(self.layoutWidget3)
        self.facedetailerStepsLabel.setObjectName(u"facedetailerStepsLabel")
        self.facedetailerStepsLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.facedetailerStepsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_12.addWidget(self.facedetailerStepsLabel)

        self.facedetailerStepsSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerStepsSpinBox.setObjectName(u"facedetailerStepsSpinBox")
        self.facedetailerStepsSpinBox.setStyleSheet(u"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 20px;\n"
"}\n"
"QSpinBox:hover, QDoubleSpinBox:hover { border-color: #3d4356; }\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border-color: #7c6cff; }\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"    width: 16px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-bottom: 5px solid #9aa2b8;\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #9aa2b8;\n"
"}")
        self.facedetailerStepsSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerStepsSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerStepsSpinBox.setMinimum(1)
        self.facedetailerStepsSpinBox.setMaximum(50)
        self.facedetailerStepsSpinBox.setValue(20)

        self.verticalLayout_12.addWidget(self.facedetailerStepsSpinBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_12)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.facedetailerCfgLabel = QLabel(self.layoutWidget3)
        self.facedetailerCfgLabel.setObjectName(u"facedetailerCfgLabel")
        self.facedetailerCfgLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.facedetailerCfgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_13.addWidget(self.facedetailerCfgLabel)

        self.facedetailerCfgSpinBox = QDoubleSpinBox(self.layoutWidget3)
        self.facedetailerCfgSpinBox.setObjectName(u"facedetailerCfgSpinBox")
        self.facedetailerCfgSpinBox.setStyleSheet(u"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 20px;\n"
"}\n"
"QSpinBox:hover, QDoubleSpinBox:hover { border-color: #3d4356; }\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border-color: #7c6cff; }\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"    width: 16px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-bottom: 5px solid #9aa2b8;\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #9aa2b8;\n"
"}")
        self.facedetailerCfgSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerCfgSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerCfgSpinBox.setMinimum(0.000000000000000)
        self.facedetailerCfgSpinBox.setMaximum(20.000000000000000)
        self.facedetailerCfgSpinBox.setSingleStep(0.500000000000000)
        self.facedetailerCfgSpinBox.setValue(4.000000000000000)

        self.verticalLayout_13.addWidget(self.facedetailerCfgSpinBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_13)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.facedetailerGuideSizeLabel = QLabel(self.layoutWidget3)
        self.facedetailerGuideSizeLabel.setObjectName(u"facedetailerGuideSizeLabel")
        self.facedetailerGuideSizeLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.facedetailerGuideSizeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_14.addWidget(self.facedetailerGuideSizeLabel)

        self.facedetailerGuideSizeSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerGuideSizeSpinBox.setObjectName(u"facedetailerGuideSizeSpinBox")
        self.facedetailerGuideSizeSpinBox.setStyleSheet(u"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 20px;\n"
"}\n"
"QSpinBox:hover, QDoubleSpinBox:hover { border-color: #3d4356; }\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border-color: #7c6cff; }\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"    width: 16px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-bottom: 5px solid #9aa2b8;\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #9aa2b8;\n"
"}")
        self.facedetailerGuideSizeSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerGuideSizeSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerGuideSizeSpinBox.setMinimum(64)
        self.facedetailerGuideSizeSpinBox.setMaximum(1024)
        self.facedetailerGuideSizeSpinBox.setValue(256)

        self.verticalLayout_14.addWidget(self.facedetailerGuideSizeSpinBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_14)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.facedetailerMaxSizeLabel = QLabel(self.layoutWidget3)
        self.facedetailerMaxSizeLabel.setObjectName(u"facedetailerMaxSizeLabel")
        self.facedetailerMaxSizeLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.facedetailerMaxSizeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_15.addWidget(self.facedetailerMaxSizeLabel)

        self.facedetailerMaxSizeSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerMaxSizeSpinBox.setObjectName(u"facedetailerMaxSizeSpinBox")
        self.facedetailerMaxSizeSpinBox.setStyleSheet(u"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 20px;\n"
"}\n"
"QSpinBox:hover, QDoubleSpinBox:hover { border-color: #3d4356; }\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border-color: #7c6cff; }\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"    width: 16px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-bottom: 5px solid #9aa2b8;\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #9aa2b8;\n"
"}")
        self.facedetailerMaxSizeSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerMaxSizeSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerMaxSizeSpinBox.setMinimum(128)
        self.facedetailerMaxSizeSpinBox.setMaximum(2048)
        self.facedetailerMaxSizeSpinBox.setValue(768)

        self.verticalLayout_15.addWidget(self.facedetailerMaxSizeSpinBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_15)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.facedetailerFeatherLabel = QLabel(self.layoutWidget3)
        self.facedetailerFeatherLabel.setObjectName(u"facedetailerFeatherLabel")
        self.facedetailerFeatherLabel.setStyleSheet(u"background-color: transparent;\n"
"color: #e8eaf0;")
        self.facedetailerFeatherLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_16.addWidget(self.facedetailerFeatherLabel)

        self.facedetailerFeatherSpinBox = QSpinBox(self.layoutWidget3)
        self.facedetailerFeatherSpinBox.setObjectName(u"facedetailerFeatherSpinBox")
        self.facedetailerFeatherSpinBox.setStyleSheet(u"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #12141c;\n"
"    color: #e8eaf0;\n"
"    border: 1px solid #2a2f3d;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 20px;\n"
"}\n"
"QSpinBox:hover, QDoubleSpinBox:hover { border-color: #3d4356; }\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border-color: #7c6cff; }\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"    width: 16px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-bottom: 5px solid #9aa2b8;\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"    image: none; width: 0; height: 0;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #9aa2b8;\n"
"}")
        self.facedetailerFeatherSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.facedetailerFeatherSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.facedetailerFeatherSpinBox.setMinimum(0)
        self.facedetailerFeatherSpinBox.setMaximum(20)
        self.facedetailerFeatherSpinBox.setValue(5)

        self.verticalLayout_16.addWidget(self.facedetailerFeatherSpinBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_16)

        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)

        self.mainModeTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ComfyUI + LMStudio Generator v0.3", None))
        self.mainModeTabWidget.setTabText(self.mainModeTabWidget.indexOf(self.settingsTabPage), QCoreApplication.translate("MainWindow", u"\u2699\ufe0f \uc124\uc815", None))
        self.mainModeTabWidget.setTabText(self.mainModeTabWidget.indexOf(self.generationTabPage), QCoreApplication.translate("MainWindow", u"\u2753 \ub3c4\uc6c0\ub9d0", None))
        self.resultPanel.setTitle(QCoreApplication.translate("MainWindow", u"\U0001f5bc\U0000fe0f Image preview", None))
        self.previewLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f5bc\U0000fe0f", None))
        self.openOutputFolderButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c2 Open", None))
        self.saveImageButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4be Save", None))
        self.executionPanel.setTitle(QCoreApplication.translate("MainWindow", u"\u25b6\ufe0f Launch", None))
        self.progressStatusLabel.setText(QCoreApplication.translate("MainWindow", u"\uc900\ube44 \uc644\ub8cc", None))
        self.elapsedLabel.setText(QCoreApplication.translate("MainWindow", u"0\ucd08", None))
        self.progressPercentLabel.setText(QCoreApplication.translate("MainWindow", u"0%", None))
        self.generateButton.setText(QCoreApplication.translate("MainWindow", u"\uc774\ubbf8\uc9c0 \uc0dd\uc131 \uc2dc\uc791", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc9c0", None))
        self.exitButton.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.logGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\U0001f4cb View live logs", None))
        self.logTextEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\ub85c\uadf8\uac00 \uc5ec\uae30\uc5d0 \ud45c\uc2dc\ub429\ub2c8\ub2e4...", None))
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f5d1\U0000fe0f Clear", None))
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
        self.restoreDefaultsButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f504\U0000ae30\U0000bcf8\U0000ac12 \U0000bcf5\U0000c6d0", None))
        self.loadConfigButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c2 \U0000c124\U0000c815 \U0000bd88\U0000b7ec\U0000c624\U0000ae30", None))
        self.saveConfigButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4be \U0000c124\U0000c815 \U0000c800\U0000c7a5", None))
        self.pushButton.setText("")
        self.connectionPanel.setTitle(QCoreApplication.translate("MainWindow", u"\U0001f310 Api Server Connection", None))
        self.lmgroupBox.setTitle("")
        self.lmAddressLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f4e1 \U0000c11c\U0000bc84 \U0000c8fc\U0000c18c", None))
        self.lmUrlEdit.setText(QCoreApplication.translate("MainWindow", u"http://127.0.0.1:1729", None))
        self.lmTitleLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f9e0 LM Studio", None))
        self.lmStatusLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f4e1\U0000c5f0\U0000acb0 \U0000d655\U0000c778 \U0000c911...", None))
        self.lmCheckButton.setText(QCoreApplication.translate("MainWindow", u"\uc5f0\uacb0 \ud655\uc778", None))
        self.lmModelLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f4e6 \U0000baa8\U0000b378 \U0000c120\U0000d0dd", None))
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
        self.samplerComboBox.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>SAMPLER_OPTIONS</p><p>(&quot;dpmpp_2m_sde&quot;, &quot;SDE \uae30\ubc18\uc73c\ub85c \ub514\ud14c\uc77c\uc774 \ub6f0\uc5b4\ub098\uba70, \ubd80\ub4dc\ub7ec\uc6b4 \uacb0\uacfc\ubb3c\uc744 \uc0dd\uc131\ud569\ub2c8\ub2e4.&quot;),</p><p>(&quot;dpmpp_2m&quot;, &quot;\uac00\uc7a5 \ubcf4\ud3b8\uc801\uc73c\ub85c \uc0ac\uc6a9\ub418\uba70 \uc18d\ub3c4\uc640 \ud488\uc9c8\uc758 \uade0\ud615\uc774 \ud6cc\ub96d\ud569\ub2c8\ub2e4.&quot;),</p><p>(&quot;euler&quot;, &quot;\ube60\ub974\uace0 \uc548\uc815\uc801\uc774\uba70 \uae54\ub054\ud55c \uacb0\uacfc\ubb3c\uc744 \uc6d0\ud560 \ub54c \uc801\ud569\ud569\ub2c8\ub2e4.&quot;),</p><p>(&quot;euler_ancestral&quot;, &quot;\ub9e4 \uc2a4\ud15d\ub9c8\ub2e4 \ub178\uc774\uc988\ub97c \ucd94\uac00\ud558\uc5ec \ub2e4\uc591\ud55c \ubcc0\ud615\uc744 \uc2dc\ub3c4\ud569\ub2c8\ub2e4.&quot;),</p><p>(&quot;lcm&quot;, &quot;\uc801\uc740 \uc2a4\ud15d(4~8)\uc73c\ub85c\ub3c4 \ube60\ub974\uac8c \uc0dd\uc131\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.&quot;),</p><p>(&quot;ddim&quot;, &quot;"
                        "\uc77c\uad00\uc131\uc774 \ub192\uace0 \uc548\uc815\uc801\uc778 \uc0dd\uc131\uc744 \ubcf4\uc7a5\ud569\ub2c8\ub2e4.&quot;),</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.schedulerLabel.setText(QCoreApplication.translate("MainWindow", u"Scheduler", None))
#if QT_CONFIG(tooltip)
        self.schedulerComboBox.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>SCHEDULER_OPTIONS </p><p>    (&quot;normal&quot;, &quot;\uac00\uc7a5 \ubb34\ub09c\ud558\uace0 \uae30\ubcf8\uc801\uc778 \ub178\uc774\uc988 \uc2a4\ucf00\uc904\uc785\ub2c8\ub2e4.&quot;),</p><p>    (&quot;karras&quot;, &quot;\uace0\ud654\uc9c8 \uc774\ubbf8\uc9c0 \uc0dd\uc131\uc5d0 \uac15\ud558\uba70 \ub514\ud14c\uc77c\uc744 \uc0b4\ub9ac\ub294 \ub370 \ud6a8\uacfc\uc801\uc785\ub2c8\ub2e4.&quot;),</p><p>    (&quot;exponential&quot;, &quot;\uc9c0\uc218\uc801\uc73c\ub85c \ubcc0\ud654\ud558\uba70 \ubd80\ub4dc\ub7ec\uc6b4 \uac10\uc1e0\ub97c \uc81c\uacf5\ud569\ub2c8\ub2e4.&quot;),</p><p>    (&quot;sgm_uniform&quot;, &quot;SGM \ub178\uc774\uc988 \uc2a4\ucf00\uc904\uc744 \uc0ac\uc6a9\ud558\uba70 \uc77c\uc815\ud55c \uac04\uaca9\uc744 \uac00\uc9d1\ub2c8\ub2e4.&quot;),</p><p>    (&quot;simple&quot;, &quot;\ubcf5\uc7a1\ud55c \uacc4\uc0b0 \uc5c6\uc774 \ub2e8\uc21c\ud55c \uc120\ud615 \uc2a4\ucf00\uc904\uc785\ub2c8\ub2e4.&quot;),</p><p>    (&quot;ddim_uniform&quot;, &quot;DDIM\uc758 \uade0\uc77c\ud55c \ub178\uc774"
                        "\uc988 \uc2a4\ucf00\uc904\uc744 \ub530\ub985\ub2c8\ub2e4.&quot;),</p><p>    (&quot;beta&quot;, &quot;\ubca0\ud0c0 \ubd84\ud3ec\ub97c \ub530\ub974\ub294 \ub178\uc774\uc988 \uc2a4\ucf00\uc904\uc785\ub2c8\ub2e4.&quot;),</p><p>    (&quot;linear_quadratic&quot;, &quot;\uc120\ud615\uacfc \uc774\ucc28 \ud568\uc218\uac00 \ud63c\ud569\ub41c \ub3c5\ud2b9\ud55c \uc2a4\ucf00\uc904\uc785\ub2c8\ub2e4.&quot;),</p><p>    (&quot;kl_optimal&quot;, &quot;KL \ubc1c\uc0b0\uc744 \ucd5c\uc801\ud654\ud558\uc5ec \uc218\ub834 \uc18d\ub3c4\ub97c \ub192\uc785\ub2c8\ub2e4.&quot;),</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerGroupBox.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><b>FaceDetailer</b>\ub294 ComfyUI Impact Pack\uc758 \ub178\ub4dc\ub85c, \uc0dd\uc131\ub41c \uc774\ubbf8\uc9c0\uc5d0\uc11c \uc5bc\uad74\uc744 \uac10\uc9c0\ud558\uc5ec<br/>\ubcc4\ub3c4\uc758 \ud30c\ub77c\ubbf8\ud130\ub85c<b>\uc5bc\uad74 \uc601\uc5ed\ub9cc</b> \uc7ac\uc0dd\uc131\ud558\uc5ec \ub514\ud14c\uc77c\uc744 \ubcf4\uc815\ud569\ub2c8\ub2e4.</p><p><b>\uae30\uc874 \uc0dd\uc131 \uc635\uc158(CFG, Steps \ub4f1)\uacfc \ubcc4\ub3c4</b>\ub85c \ub3d9\uc791\ud558\uba70, \uc5bc\uad74 \uc601\uc5ed\ub9cc<br/>\ub354 \uc12c\uc138\ud558\uac8c/\uac15\ud558\uac8c \ubcf4\uc815\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.</p><p><b>\ud544\uc218 \uc870\uac74</b>: ComfyUI\uc5d0 <b>Impact Pack</b> \uc124\uce58 \ud544\uc694<br/>(FaceDetailer, UltralyticsDetectorProvider \ub178\ub4dc \ud3ec\ud568)</p></body></html>\n"
"        ", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\U0001f464 FaceDetailer (\U0000c5bc\U0000ad74 \U0000bcf4\U0000c815)", None))
#if QT_CONFIG(tooltip)
        self.facedetailerCheckBox.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>FaceDetailer \uc5bc\uad74 \ubcf4\uc815 \uae30\ub2a5 \ucf1c\uae30/\ub044\uae30<br/>\uccb4\ud06c \uc2dc: \uc804\uccb4 \uc774\ubbf8\uc9c0\uc0dd\uc131 \ud6c4 \uc5bc\uad74 \uc601\uc5ed\ub9cc \ubcc4\ub3c4\ub85c \ubcf4\uc815<br/>\ud574\uc81c \uc2dc: \ubcf4\uc815 \uc5c6\uc774, \uc77c\ubc18 \uc774\ubbf8\uc9c0\uc0dd\uc131\ub9cc \uc218\ud589 <br/><span style=\" font-weight:700;\">\ud544\uc218</span>: ComfyUI Impact Pack \uc124\uce58 \ud544\uc694 </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerCheckBox.setText("")
#if QT_CONFIG(tooltip)
        self.facedetailerDenoiseLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc7ac\uc0dd\uc131 \uc2dc \uc6d0\ubcf8 \uc720\uc9c0 \uac15\ub3c4 (0.0~1.0)<br/><b>\ub0ae\uc744\uc218\ub85d</b> \uc6d0\ubcf8 \uc5bc\uad74 \ud615\ud0dc \uc720\uc9c0, <b>\ub192\uc744\uc218\ub85d</b> \ud504\ub86c\ud504\ud2b8 \ubc18\uc601 \uac15\ud568<br/><b>\uae30\ubcf8 0.4</b>: \uc6d0\ubcf8 \uc5bc\uad74 \uc720\uc9c0\ud558\uba74\uc11c \ub514\ud14c\uc77c \ubcf4\uac15<br/><i>\u203b \uc804\uccb4 \uc0dd\uc131\uc758 Denoise\uc640 \ubcc4\ub3c4 \ub3d9\uc791</i>\n"
"        ", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerDenoiseLabel.setText(QCoreApplication.translate("MainWindow", u"Denoise", None))
#if QT_CONFIG(tooltip)
        self.facedetailerDenoiseSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc7ac\uc0dd\uc131 \uc2dc \uc6d0\ubcf8 \uc720\uc9c0 \uac15\ub3c4 (0.0~1.0)<br/><b>\ub0ae\uc744\uc218\ub85d</b> \uc6d0\ubcf8 \uc5bc\uad74 \ud615\ud0dc \uc720\uc9c0, <b>\ub192\uc744\uc218\ub85d</b> \ud504\ub86c\ud504\ud2b8 \ubc18\uc601 \uac15\ud568<br/><b>\uae30\ubcf8 0.4</b>: \uc6d0\ubcf8 \uc5bc\uad74 \uc720\uc9c0\ud558\uba74\uc11c \ub514\ud14c\uc77c \ubcf4\uac15<br/><i>\u203b \uc804\uccb4 \uc0dd\uc131\uc758 Denoise\uc640 \ubcc4\ub3c4 \ub3d9\uc791</i>\n"
"        ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerStepsLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc7ac\uc0dd\uc131 \ubc18\ubcf5 \ud69f\uc218 (1~50)<br/><b>\ub192\uc744\uc218\ub85d</b> \ub514\ud14c\uc77c \ud5a5\uc0c1, \uc0dd\uc131 \uc2dc\uac04 \uc99d\uac00<br/><b>\uae30\ubcf8 20</b>: \uc801\uc808\ud55c \ud488\uc9c8/\uc18d\ub3c4 \uade0\ud615<br/><i>\u203b \uc804\uccb4 \uc0dd\uc131\uc758 Steps\uc640 \ubcc4\ub3c4 \ub3d9\uc791</i>\n"
"        ", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerStepsLabel.setText(QCoreApplication.translate("MainWindow", u"Steps", None))
#if QT_CONFIG(tooltip)
        self.facedetailerStepsSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc7ac\uc0dd\uc131 \ubc18\ubcf5 \ud69f\uc218 (1~50)<br/><b>\ub192\uc744\uc218\ub85d</b> \ub514\ud14c\uc77c \ud5a5\uc0c1, \uc0dd\uc131 \uc2dc\uac04 \uc99d\uac00<br/><b>\uae30\ubcf8 20</b>: \uc801\uc808\ud55c \ud488\uc9c8/\uc18d\ub3c4 \uade0\ud615<br/><i>\u203b \uc804\uccb4 \uc0dd\uc131\uc758 Steps\uc640 \ubcc4\ub3c4 \ub3d9\uc791</i>\n"
"        ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerCfgLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc7ac\uc0dd\uc131 \uc2dc \ud504\ub86c\ud504\ud2b8 \uc900\uc218\ub3c4 (0~20)<br/><b>\ub192\uc744\uc218\ub85d</b> \ud504\ub86c\ud504\ud2b8 \uac15\ub825 \ubc18\uc601, <b>\ub0ae\uc744\uc218\ub85d</b> \uc790\uc720\ub85c\uc6b4 \uc0dd\uc131<br/><b>\uae30\ubcf8 4.0</b>: \uc790\uc5f0\uc2a4\ub7ec\uc6b4 \uc5bc\uad74 \ubcf4\uc815<br/><i>\u203b \uc804\uccb4 \uc0dd\uc131\uc758 CFG\uc640 \ubcc4\ub3c4 \ub3d9\uc791</i>\n"
"        ", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerCfgLabel.setText(QCoreApplication.translate("MainWindow", u"CFG", None))
#if QT_CONFIG(tooltip)
        self.facedetailerCfgSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \uc7ac\uc0dd\uc131 \uc2dc \ud504\ub86c\ud504\ud2b8 \uc900\uc218\ub3c4 (0~20)<br/><b>\ub192\uc744\uc218\ub85d</b> \ud504\ub86c\ud504\ud2b8 \uac15\ub825 \ubc18\uc601, <b>\ub0ae\uc744\uc218\ub85d</b> \uc790\uc720\ub85c\uc6b4 \uc0dd\uc131<br/><b>\uae30\ubcf8 4.0</b>: \uc790\uc5f0\uc2a4\ub7ec\uc6b4 \uc5bc\uad74 \ubcf4\uc815<br/><i>\u203b \uc804\uccb4 \uc0dd\uc131\uc758 CFG\uc640 \ubcc4\ub3c4 \ub3d9\uc791</i>\n"
"        ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerGuideSizeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"<b>FaceDetailer \uc804\uc6a9</b>: \uc5bc\uad74 \ud06c\ub86d\uc744 \uc5c5\uc2a4\ucf00\uc77c\ud560 \ud0c0\uac9f \ud574\uc0c1\ub3c4<br/>\uc5bc\uad74 \uc601\uc5ed\uc744 \uc774 \ud06c\uae30\ub85c \ud0a4\uc6cc\uc11c \ub514\ud14c\uc77c\ud558\uac8c \uc7ac\uc0dd\uc131 \ud6c4 \uc6d0\ubcf8\uc5d0 \ud569\uc131<br/><b>\uae30\ubcf8 256</b>: 256x256\uc73c\ub85c \uc5c5\uc2a4\ucf00\uc77c\ud558\uc5ec \uc138\ubc00 \ubcf4\uc815<br/><i>\u203b \uc804\uccb4 \uc774\ubbf8\uc9c0 \ud574\uc0c1\ub3c4(\uac00\ub85c/\uc138\ub85c)\uc640 \ubb34\uad00</i>\n"
"        ", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerGuideSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Guide Size", None))
#if QT_CONFIG(tooltip)
        self.facedetailerGuideSizeSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"<b>FaceDetailer \uc804\uc6a9</b>: \uc5bc\uad74 \ud06c\ub86d\uc744 \uc5c5\uc2a4\ucf00\uc77c\ud560 \ud0c0\uac9f \ud574\uc0c1\ub3c4<br/>\uc5bc\uad74 \uc601\uc5ed\uc744 \uc774 \ud06c\uae30\ub85c \ud0a4\uc6cc\uc11c \ub514\ud14c\uc77c\ud558\uac8c \uc7ac\uc0dd\uc131 \ud6c4 \uc6d0\ubcf8\uc5d0 \ud569\uc131<br/><b>\uae30\ubcf8 256</b>: 256x256\uc73c\ub85c \uc5c5\uc2a4\ucf00\uc77c\ud558\uc5ec \uc138\ubc00 \ubcf4\uc815<br/><i>\u203b \uc804\uccb4 \uc774\ubbf8\uc9c0 \ud574\uc0c1\ub3c4(\uac00\ub85c/\uc138\ub85c)\uc640 \ubb34\uad00</i>\n"
"        ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.facedetailerMaxSizeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"<b>FaceDetailer \uc804\uc6a9</b>: \uc5bc\uad74 \ud06c\ub86d \ucd5c\ub300 \ud06c\uae30 \uc81c\ud55c (VRAM \uc808\uc57d)<br/>\ub108\ubb34 \ud070 \uc5bc\uad74 \ud06c\ub86d \ubc29\uc9c0\ub85c \uba54\ubaa8\ub9ac \ubd80\uc871 \ubc29\uc9c0<br/><b>\uae30\ubcf8 768</b>: 768px \ucd08\uacfc \uc5bc\uad74\uc740 \ub2e4\uc6b4\uc2a4\ucf00\uc77c \ud6c4 \ucc98\ub9ac<br/><i>\u203b \uc804\uccb4 \uc774\ubbf8\uc9c0 \ud574\uc0c1\ub3c4\uc640 \ubb34\uad00</i>\n"
"        ", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerMaxSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Max Size", None))
#if QT_CONFIG(tooltip)
        self.facedetailerFeatherLabel.setToolTip(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74 \ud569\uc131 \uacbd\uacc4\uc120 \ube14\ub7ec \ucc98\ub9ac (0~20)<br/><b>\ub192\uc744\uc218\ub85d</b> \uacbd\uacc4 \uc790\uc5f0\uc2a4\ub7ec\uc6c0, <b>\ub0ae\uc744\uc218\ub85d</b> \uc120\uba85<br/><b>\uae30\ubcf8 5</b>: \uc790\uc5f0\uc2a4\ub7ec\uc6b4 \ud569\uc131<br/><i>\u203b \uc5bc\uad74 \ub9c8\uc2a4\ud06c \uacbd\uacc4 \ubd80\ub4dc\ub7fd\uac8c \ucc98\ub9ac</i>\n"
"        ", None))
#endif // QT_CONFIG(tooltip)
        self.facedetailerFeatherLabel.setText(QCoreApplication.translate("MainWindow", u"Feather", None))
    # retranslateUi

