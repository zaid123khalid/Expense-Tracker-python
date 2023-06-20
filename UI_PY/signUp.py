from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QApplication
from PyQt5 import QtGui

import db_storage
from UI_PY.mainExpWin import ExpenseTracker

from consts import fnts
from widgets.customMsgBox import MsgBox


class SignUp(QWidget):
    win_close = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.app = QApplication.instance()
        self.main_win = None

        self.setWindowTitle("Sign Up")
        self.setObjectName("Form")
        self.resize(400, 300)

        self.label = QLabel("Sign Up Form", self)
        self.label.setGeometry(QtCore.QRect(10, 10, 380, 30))
        self.label.setFont(fnts.font(ptSize=14, weight=75))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.label_2 = QLabel("Username", self)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 150, 30))
        self.label_2.setObjectName("label_2")

        self.label_3 = QLabel("Password", self)
        self.label_3.setGeometry(QtCore.QRect(10, 120, 150, 30))
        self.label_3.setObjectName("label_3")

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(220, 80, 170, 30))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(220, 120, 170, 30))
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.pushButton = QPushButton("Sign Up", self)
        self.pushButton.setGeometry(QtCore.QRect(10, 260, 380, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.sign_up)

        QtCore.QMetaObject.connectSlotsByName(self)

    def sign_up(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if username == "" or username is None:
            MsgBox(QMessageBox.Information, "Empty Credentials",
                   "Username must not be empty")
        elif password == "" or password is None:
            MsgBox(QMessageBox.Information, "Empty Credentials",
                   "Password must not be empty")
        else:
            db_storage.storage_db().create_profile(username, password)
            self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.win_close.emit()
