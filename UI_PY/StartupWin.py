from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QMessageBox, QApplication

import db_storage
from UI_PY.mainExpWin import ExpenseTracker
from UI_PY.signUp import SignUp

from consts import fnts
from widgets.customMsgBox import MsgBox


class StartupWin(QMainWindow):
    def __init__(self):
        super().__init__()

        db_storage.storage_db().create_tables()

        self.app = QApplication.instance()
        self.main_win = None
        self.signUp_win = None

        self.setObjectName("Form")
        self.setWindowTitle("Expense App")
        self.setFixedSize(400, 300)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.setFont(font)

        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 10, 380, 30))
        self.label.setFont(fnts.font(ptSize=14))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("Welcome To The Expense App")
        self.label.setObjectName("label")

        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 380, 110))
        self.label_2.setFont(fnts.font(weight=0))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setText("Expense App is an app that helps keeps track of Expense and show you the details of what you "
                             "spent on which date and on which category")
        self.label_2.setObjectName("label_2")

        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(10, 180, 150, 30))
        self.label_3.setFont(fnts.font(weight=0, ptSize=10))
        self.label_3.setWordWrap(True)
        self.label_3.setText("Username")
        self.label_3.setObjectName("label_3")

        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(10, 220, 150, 30))
        self.label_4.setFont(fnts.font(weight=0, ptSize=10))
        self.label_4.setWordWrap(True)
        self.label_4.setText("Password")
        self.label_4.setObjectName("label_4")

        self.lineedit = QLineEdit(self)
        self.lineedit.setGeometry(QtCore.QRect(220, 180, 170, 30))
        self.lineedit.setObjectName("lineEdit")

        self.lineedit_2 = QLineEdit(self)
        self.lineedit_2.setGeometry(QtCore.QRect(220, 220, 170, 30))
        self.lineedit_2.setEchoMode(QLineEdit.Password)
        self.lineedit_2.returnPressed.connect(self.login)
        self.lineedit_2.setObjectName("lineEdit_2")

        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(220, 260, 170, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Login")
        self.pushButton.clicked.connect(self.login)

        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 260, 170, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Sign Up")
        self.pushButton_2.clicked.connect(self.signUpWin)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.apply_theme()

    def signUpWin(self):
        self.signUp_win = SignUp()
        self.setDisabled(True)
        self.signUp_win.win_close.connect(self.disable)
        self.signUp_win.show()

    def show_main_win(self):
        self.main_win = ExpenseTracker()
        self.main_win.show()
        self.close()

    def disable(self):
        self.setDisabled(False)

    def apply_theme(self):
        db_storage.storage_db().apply_theme(self.app)

    def login(self):
        username = self.lineedit.text()
        password = self.lineedit_2.text()

        text = db_storage.storage_db().get_user_info(username, password)

        if text:
            self.show_main_win()
        else:
            MsgBox(QMessageBox.Information, "Invalid Credentials", "Invalid or Wrong Credentials entered Or "
                   "There are no User registered")
