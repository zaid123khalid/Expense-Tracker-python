from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFrame, QTextEdit, QMessageBox, QDateEdit
from PyQt5.QtCore import pyqtSignal, QRegExp

import datetime

import db_storage
from widgets import customMsgBox
from consts import fnts, mnths


class AddIncome(QWidget):
    win_close = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("Form")
        self.resize(400, 310)
        self.setWindowTitle("Add Income")

        self.Header = QLabel("ADD INCOME", self)
        self.Header.setGeometry(QtCore.QRect(10, 10, 380, 30))
        self.Header.setFont(fnts.font(ptSize=14))
        self.Header.setAlignment(QtCore.Qt.AlignCenter)
        self.Header.setObjectName("add_income_lbl_2")

        self.prvs_income_lbl = QLabel("Total Income(All Time)", self)
        self.prvs_income_lbl.setGeometry(QtCore.QRect(10, 50, 170, 30))
        self.prvs_income_lbl.setFont(fnts.font(weight=0))
        self.prvs_income_lbl.setObjectName("prvs_income_lbl")

        self.prvs_income_edit = QLineEdit(self)
        self.prvs_income_edit.setGeometry(QtCore.QRect(230, 50, 160, 30))
        self.prvs_income_edit.setFont(fnts.font(weight=0))
        self.prvs_income_edit.setDisabled(True)
        self.prvs_income_edit.setObjectName("prvs_income_edit")

        today = datetime.date.today()

        month = today.month - 1

        income, cur_month_inc = db_storage.storage_db().get_income(month, today.year)

        for inc in income:
            self.prvs_income_edit.setText(
                str(inc) if inc is not None else str("00"))

        self.prvs_income_lbl_2 = QLabel(f"Total Income({today.strftime('%B')})", self)
        self.prvs_income_lbl_2.setGeometry(QtCore.QRect(10, 90, 200, 30))
        self.prvs_income_lbl_2.setFont(fnts.font(weight=0))
        self.prvs_income_lbl_2.setObjectName("prvs_income_lbl_2")

        self.prvs_income_edit_2 = QLineEdit(self)
        self.prvs_income_edit_2.setGeometry(QtCore.QRect(230, 90, 160, 30))
        self.prvs_income_edit_2.setFont(fnts.font(weight=0))
        self.prvs_income_edit_2.setDisabled(True)
        self.prvs_income_edit_2.setObjectName("prvs_income_edit_2")

        for cur_mnth_income in cur_month_inc:
            self.prvs_income_edit_2.setText(
                str(cur_mnth_income) if cur_mnth_income is not None else str("00"))

        self.line = QFrame(self)
        self.line.setGeometry(QtCore.QRect(7, 130, 380, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        self.add_income_lbl = QLabel("Add Income", self)
        self.add_income_lbl.setGeometry(QtCore.QRect(10, 150, 170, 30))
        self.add_income_lbl.setFont(fnts.font(weight=0))
        self.add_income_lbl.setObjectName("add_income_lbl")

        regexp = QRegExp("[0-9]*")

        self.add_income_edit = QLineEdit(self)
        self.add_income_edit.setGeometry(QtCore.QRect(230, 150, 160, 30))
        validator = QRegExpValidator(regexp, self.add_income_edit)
        self.add_income_edit.setValidator(validator)
        self.add_income_edit.setObjectName("add_income_edit")

        self.source_lbl = QLabel("Source", self)
        self.source_lbl.setGeometry(QtCore.QRect(10, 190, 170, 30))
        self.source_lbl.setFont(fnts.font(weight=0))
        self.source_lbl.setObjectName("source_lbl")

        self.source_edit = QLineEdit(self)
        self.source_edit.setGeometry(QtCore.QRect(230, 190, 160, 30))
        self.source_edit.setObjectName("source_edit")

        self.income_date_lbl = QLabel("Income Date", self)
        self.income_date_lbl.setGeometry(QtCore.QRect(10, 230, 170, 30))
        self.income_date_lbl.setFont(fnts.font(weight=0))
        self.income_date_lbl.setObjectName("income_date_lbl")

        self.income_date_edit = QDateEdit(QtCore.QDate.currentDate(), self)
        self.income_date_edit.setGeometry(QtCore.QRect(230, 230, 160, 30))
        self.income_date_edit.setCalendarPopup(True)
        self.income_date_edit.setDisplayFormat("yyyy/MM/dd")
        self.income_date_edit.setObjectName("income_date_edit")

        self.add_income_btn = QPushButton("Add Income", self)
        self.add_income_btn.setGeometry(QtCore.QRect(240, 270, 150, 30))
        self.add_income_btn.setObjectName("add_income_btn")
        self.add_income_btn.clicked.connect(self.add_income)

        self.cancel_btn = QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(QtCore.QRect(10, 270, 150, 30))
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.close)

        QtCore.QMetaObject.connectSlotsByName(self)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.win_close.emit()
        self.close()

    def add_income(self):
        add_inc = self.add_income_edit.text()
        source = self.source_edit.text()
        income_date = self.income_date_edit.date()

        if (add_inc is None or add_inc == "") or (source is None or source == ""):
            customMsgBox.MsgBox(QMessageBox.Information, "No Data Entered",
                                "Please Insert The Data in the Fields")
        else:
            db_storage.storage_db().insert_income(add_inc, source, income_date)

            self.close()
