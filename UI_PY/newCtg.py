
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QFrame, QTextEdit, QMessageBox

import db_storage
from widgets import customMsgBox
from consts import fnts


class NewCtg(QWidget):
    win_close = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("Form")
        self.setFixedSize(400, 300)
        self.setWindowTitle("Create Category")

        self.header = QLabel("Add New Category", self)
        self.header.setGeometry(QtCore.QRect(10, 10, 380, 30))
        self.header.setFont(fnts.font(ptSize=14))
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("label")

        self.preCtgs = QLabel("Previous Categories", self)
        self.preCtgs.setGeometry(QtCore.QRect(10, 50, 150, 30))
        self.preCtgs.setFont(fnts.font(weight=0))
        self.preCtgs.setObjectName("label_2")

        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(230, 50, 160, 30))
        self.comboBox.setObjectName("comboBox")

        ctgs = db_storage.storage_db().get_ctgs()
        for ctg in ctgs:
            self.comboBox.addItem(ctg[0])

        self.line = QFrame(self)
        self.line.setGeometry(QtCore.QRect(10, 90, 380, 10))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        self.newCtg = QLabel("Category Name", self)
        self.newCtg.setGeometry(QtCore.QRect(10, 110, 150, 30))
        self.newCtg.setFont(fnts.font(weight=0))
        self.newCtg.setObjectName("label_3")

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(230, 110, 160, 30))
        self.lineEdit.setObjectName("lineEdit")

        self.newCtgDes = QLabel("Category Description", self)
        self.newCtgDes.setGeometry(QtCore.QRect(10, 150, 150, 30))
        self.newCtgDes.setFont(fnts.font(weight=0))
        self.newCtgDes.setObjectName("label_4")

        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(230, 150, 160, 80))
        self.textEdit.setObjectName("textEdit")

        self.cancel_btn = QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(QtCore.QRect(10, 260, 140, 30))
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.close)

        self.add_ctg_btn = QPushButton("Add Category", self)
        self.add_ctg_btn.setGeometry(QtCore.QRect(250, 260, 140, 30))
        self.add_ctg_btn.setObjectName("add_ctg_btn")
        self.add_ctg_btn.clicked.connect(self.insert)

        QtCore.QMetaObject.connectSlotsByName(self)

    def insert(self):
        ctg_name = self.lineEdit.text().title()
        ctg_des = self.textEdit.toPlainText().capitalize()

        ctgs = db_storage.storage_db().check_exist_ctg(ctg_name, ctg_des)

        if (ctg_name is None or ctg_name == "") or (ctg_des is None or ctg_des == ""):
            customMsgBox.MsgBox(QMessageBox.Information, "No Data Entered",
                                "Please Insert The Data in the Fields")
        elif ctgs is not None:
            customMsgBox.MsgBox(QMessageBox.Information, "Category Exists",
                                "The Category already exists.")
        else:
            db_storage.storage_db().insert_ctg(ctg_name, ctg_des)
            self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.win_close.emit()
        self.close()
