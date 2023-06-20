from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QDateEdit, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, QRegExp

from UI_PY.newCtg import NewCtg

import db_storage
from widgets import customMsgBox
from consts import fnts


class AddExp(QWidget):
    win_close = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.newCtg = None
        self.setObjectName("NewExp")
        self.setFixedSize(400, 300)
        self.setWindowTitle("New Expense")

        self.header = QLabel("Add New Expense", self)
        self.header.setGeometry(QtCore.QRect(10, 10, 380, 30))
        self.header.setFont(fnts.font(ptSize=14))
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("label")

        self.Id = QLabel("Id", self)
        self.Id.setGeometry(QtCore.QRect(10, 60, 150, 30))
        self.Id.setFont(fnts.font(weight=0))
        self.Id.setObjectName("label_2")

        self.category = QLabel("Category", self)
        self.category.setGeometry(QtCore.QRect(10, 100, 150, 30))
        self.category.setFont(fnts.font(weight=0))
        self.category.setObjectName("category")

        self.spend = QLabel("Spend(PKR)", self)
        self.spend.setGeometry(QtCore.QRect(10, 140, 150, 30))
        self.spend.setFont(fnts.font(weight=0))
        self.spend.setObjectName("spend")

        self.spendDate = QLabel("Spend Date", self)
        self.spendDate.setGeometry(QtCore.QRect(10, 180, 150, 30))
        self.spendDate.setFont(fnts.font(weight=0))
        self.spendDate.setObjectName("spendDate")

        regexp = QRegExp("[0-9]*")

        self.IdEdit = QLineEdit(self)
        self.IdEdit.setGeometry(QtCore.QRect(230, 60, 160, 30))
        self.IdEdit.setObjectName("IdEdit")
        validator = QRegExpValidator(regexp, self.IdEdit)
        self.IdEdit.setValidator(validator)

        self.ctg_select = QComboBox(self)
        self.ctg_select.setGeometry(QtCore.QRect(230, 100, 160, 30))
        self.ctg_select.setObjectName("ctg_select")

        ctgs = db_storage.storage_db().get_ctgs()
        for ctg in ctgs:
            self.ctg_select.addItem(ctg[0])

        self.spendEdit = QLineEdit(self)
        self.spendEdit.setGeometry(QtCore.QRect(230, 140, 160, 30))
        validator = QtGui.QRegExpValidator(regexp, self.spendEdit)
        self.spendEdit.setValidator(validator)
        self.spendEdit.setObjectName("spendEdit")

        self.spendDateEdit = QDateEdit(QtCore.QDate.currentDate(), self)
        self.spendDateEdit.setCalendarPopup(True)
        self.spendDateEdit.setDisplayFormat("yyyy/MM/dd")
        self.spendDateEdit.setGeometry(QtCore.QRect(230, 180, 160, 30))
        self.spendDateEdit.setObjectName("spendDateEdit")

        self.cancel_btn = QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(QtCore.QRect(10, 260, 120, 30))
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.close)

        self.new_ctg_btn = QPushButton("New Category", self)
        self.new_ctg_btn.setGeometry(QtCore.QRect(140, 260, 120, 30))
        self.new_ctg_btn.setObjectName("new_ctg_btn")
        self.new_ctg_btn.clicked.connect(self.OpenNewCtg)

        self.add_exp_btn = QPushButton("Add Expense", self)
        self.add_exp_btn.setGeometry(QtCore.QRect(270, 260, 120, 30))
        self.add_exp_btn.setObjectName("add_exp_btn")
        self.add_exp_btn.clicked.connect(self.insert)

        QtCore.QMetaObject.connectSlotsByName(self)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.win_close.emit()
        self.close()

    def OpenNewCtg(self):
        self.newCtg = NewCtg()
        self.setDisabled(True)
        self.newCtg.win_close.connect(self.disable)
        self.newCtg.show()

    def reload(self):
        self.ctg_select.clear()
        ctgs = db_storage.storage_db().get_ctgs()
        for ctg in ctgs:
            self.ctg_select.addItem(ctg[0])

    def disable(self):
        self.reload()
        self.setDisabled(False)

    def insert(self):
        Id = self.IdEdit.text()
        ctg = self.ctg_select.currentText()
        spend = self.spendEdit.text()
        spenddate = self.spendDateEdit.date()

        ids = db_storage.storage_db().check_exist_exp(Id)

        if (Id is None or Id == "") or (ctg is None or ctg == "") or (spend is None or spend == ""):
            customMsgBox.MsgBox(QMessageBox.Information, "No Data Entered",
                                "Please Insert The Data in the Fields")
        elif ids is not None:
            customMsgBox.MsgBox(QMessageBox.Information, "Id Exists",
                                "The Id already exists.")
        else:
            db_storage.storage_db().insert_exp(Id, ctg, spend, spenddate)

            self.close()
