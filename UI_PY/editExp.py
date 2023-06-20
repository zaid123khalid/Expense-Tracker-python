from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QDate, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QFrame, QMessageBox

import db_storage
from consts import fnts
from widgets import customMsgBox


class EditExp(QWidget):
    win_close = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("Form")
        self.setFixedSize(400, 300)
        self.setWindowTitle("Update Expense")

        self.header = QLabel("Update Existing Expense", self)
        self.header.setGeometry(QtCore.QRect(10, 10, 380, 30))
        self.header.setFont(fnts.font(ptSize=14))
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("label")

        self.IdSelect = QLabel("Select Id", self)
        self.IdSelect.setGeometry(QtCore.QRect(10, 50, 150, 30))
        self.IdSelect.setFont(fnts.font(weight=0))
        self.IdSelect.setObjectName("label_2")

        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(230, 50, 160, 30))
        self.comboBox.setObjectName("comboBox")

        ids = db_storage.storage_db().get_data_main()
        for id in ids:
            self.comboBox.addItem(str(id[0]))

        self.comboBox.currentTextChanged.connect(self.get_data)

        self.line = QFrame(self)
        self.line.setGeometry(QtCore.QRect(10, 90, 380, 10))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.category = QLabel("Category", self)
        self.category.setGeometry(QtCore.QRect(10, 110, 150, 30))
        self.category.setFont(fnts.font(weight=0))
        self.category.setObjectName("category")

        self.spend = QLabel("Spend(PKR)", self)
        self.spend.setGeometry(QtCore.QRect(10, 150, 150, 30))
        self.spend.setFont(fnts.font(weight=0))
        self.spend.setObjectName("spend")

        self.spendDate = QLabel("Spend Date", self)
        self.spendDate.setGeometry(QtCore.QRect(10, 190, 150, 30))
        self.spendDate.setFont(fnts.font(weight=0))
        self.spendDate.setObjectName("spendDate")

        self.CtgEdit = QLineEdit(self)
        self.CtgEdit.setGeometry(QtCore.QRect(230, 110, 160, 30))
        self.CtgEdit.setObjectName("lineEdit")
        self.CtgEdit.setDisabled(True)

        regexp = QRegExp("[0-9]*")
        self.spendEdit = QLineEdit(self)
        self.spendEdit.setGeometry(QtCore.QRect(230, 150, 160, 30))
        validator = QRegExpValidator(regexp, self.spendEdit)
        self.spendEdit.setValidator(validator)
        self.spendEdit.setObjectName("spendEdit")

        self.spendDateEdit = QDateEdit(self)
        self.spendDateEdit.setGeometry(QtCore.QRect(230, 190, 160, 30))
        self.spendDateEdit.setObjectName("spendDateEdit")
        self.spendDateEdit.setCalendarPopup(True)
        self.spendDateEdit.setDisplayFormat("yyyy/MM/dd")

        self.cancel_btn = QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(QtCore.QRect(10, 260, 120, 30))
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.close)

        self.upd_exp_btn = QPushButton("Update Expense", self)
        self.upd_exp_btn.setGeometry(QtCore.QRect(270, 260, 120, 30))
        self.upd_exp_btn.setObjectName("upd_exp_btn")
        self.upd_exp_btn.clicked.connect(self.upd_data)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.get_data()

    def get_data(self):
        data = db_storage.storage_db().get_exp_info(self.comboBox.currentText())

        for item in data:
            self.CtgEdit.setText(item[1])
            self.spendEdit.setText(str(item[2]))
            date = QDate.fromString(item[3], "yyyy-MM-dd")
            self.spendDateEdit.setDate(date)

    def upd_data(self):
        Id = self.comboBox.currentText()
        spend = self.spendEdit.text()
        spenddate = self.spendDateEdit.date()
        if spend is None or spend == "":
            customMsgBox.custom_msg_box(QMessageBox.Information, "No Data Entered",
                                        "Please Insert The Data in the Fields")
        else:
            db_storage.storage_db().upd_exp(spend, spenddate, Id)

            self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.win_close.emit()
        self.close()
