import datetime

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QToolBar, QWidget, QApplication, \
    QAction, QHeaderView, QTableWidgetItem, QMessageBox, QVBoxLayout, QComboBox, QLabel, QGridLayout, \
    QPushButton, QLineEdit
from PyQt5.QtCore import Qt

import db_storage

from UI_PY.addExp import AddExp
from UI_PY.addInc import AddIncome
from UI_PY.editExp import EditExp
from UI_PY.settings import Settings
from UI_PY.smryExp import ExpenseSummary

from consts import mnths, fnts
from widgets import customMsgBox


class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = QApplication.instance()

        self.item = None
        self.yrss = None

        self.cur_month_income = None
        self.prvs_income = None
        self.rem_income = None

        gridLayout = QGridLayout()
        gridLayout.setAlignment(Qt.AlignLeft)
        layout = QVBoxLayout()

        self.setObjectName("MainWindow")
        self.setMinimumSize(600, 500)
        self.setWindowTitle("Expense Tracker")

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QLabel("Select Month", self)
        self.label.setFont(fnts.font(weight=0))
        self.label.setObjectName("label")

        self.label_2 = QLabel("Select Year", self)
        self.label_2.setFont(fnts.font(weight=0))
        self.label_2.setObjectName("label_2")

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(mnths.months_name)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setFixedSize(160, 30)

        self.comboBox_2 = QComboBox(self)
        self.comboBox_2.addItems(
            self.yrss if self.yrss is not None else db_storage.storage_db().get_years_for_smry())
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.setFixedSize(160, 30)

        self.set_default_btn = QPushButton("Set Default", self)
        self.set_default_btn.setObjectName("pushButton")
        self.set_default_btn.clicked.connect(self.load_data)
        self.set_default_btn.setFixedSize(160, 30)

        self.set_validate_btn = QPushButton("Update Data", self)
        self.set_validate_btn.setObjectName("pushButton")
        self.set_validate_btn.clicked.connect(self.load_data)
        self.set_validate_btn.setFixedSize(160, 30)

        self.prvs_income_lbl = QLabel("Income(All Time)", self)
        self.prvs_income_lbl.setFont(fnts.font(weight=0))
        self.prvs_income_lbl.setObjectName("prvs_income_lbl")
        self.prvs_income_lbl.setFixedSize(150, 30)

        self.prvs_income_edit = QLineEdit(self)
        self.prvs_income_edit.setDisabled(True)
        self.prvs_income_edit.setFont(fnts.font(weight=0))
        self.prvs_income_edit.setObjectName("prvs_income_edit")
        self.prvs_income_edit.setFixedSize(150, 30)

        self.prvs_income_lbl_2 = QLabel(f"Income({datetime.date.today().strftime('%B')})", self)
        self.prvs_income_lbl_2.setFont(fnts.font(weight=0))
        self.prvs_income_lbl_2.setObjectName("prvs_income_lbl_2")
        self.prvs_income_lbl_2.setFixedSize(150, 30)

        self.prvs_income_edit_2 = QLineEdit(self)
        self.prvs_income_edit_2.setDisabled(True)
        self.prvs_income_edit_2.setFont(fnts.font(weight=0))
        self.prvs_income_edit_2.setObjectName("prvs_income_edit_2")
        self.prvs_income_edit_2.setFixedSize(150, 30)

        self.rem_income_lbl = QLabel("Rem. Income", self)
        self.rem_income_lbl.setFont(fnts.font(weight=0))
        self.rem_income_lbl.setObjectName("prvs_income_lbl_2")
        self.rem_income_lbl.setFixedSize(150, 30)

        self.rem_income_edit = QLineEdit(self)
        self.rem_income_edit.setDisabled(True)
        self.rem_income_edit.setFont(fnts.font(weight=0))
        self.rem_income_edit.setObjectName("prvs_income_edit_2")
        self.rem_income_edit.setFixedSize(150, 30)

        self.tableWidget = QTableWidget(0, 5, self)
        self.tableWidget.setGeometry(QtCore.QRect(10, 80, 580, 400))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setHorizontalHeaderLabels(
            ["Id", "category", "Spent", "Date Spent", "Date Added"])
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.cellClicked.connect(self.handle_cell_clicked)

        self.setCentralWidget(self.centralwidget)

        self.newAction = QAction(
            QIcon("Imgs/icons8-add-new-64.png"), "New Expense", self)
        self.newAction.triggered.connect(self.openWindow)

        self.editAction = QAction(
            QIcon("Imgs/icons8-edit-48.png"), "Edit Expense", self)
        self.editAction.triggered.connect(self.openWindow)

        self.addIncomeAction = QAction(
            QIcon("Imgs/icons8-us-dollar-circled-96.png"), "Add Income", self)
        self.addIncomeAction.triggered.connect(self.openWindow)

        self.summaryAction = QAction(
            QIcon("Imgs/icons8-summary-list-50.png"), "Expense Summary", self)
        self.summaryAction.triggered.connect(self.OpenShowSummary)

        self.delAction = QAction(
            QIcon("Imgs/icons8-delete-48.png"), "Delete Expense", self)
        self.delAction.triggered.connect(self.delete_item)

        self.reloadAction = QAction(
            QIcon("Imgs/icons8-reset-50.png"), "Reload", self)
        self.reloadAction.triggered.connect(self.load_data)

        self.settingsAction = QAction(
            QIcon("Imgs/icons8-settings-64.png"), "Settings", self)
        self.settingsAction.triggered.connect(self.openWindow)

        self.toolBar = QToolBar(self)
        self.toolBar.setMovable(False)
        self.toolBar.addAction(self.newAction)
        self.toolBar.addAction(self.editAction)
        self.toolBar.addAction(self.addIncomeAction)
        self.toolBar.addAction(self.summaryAction)
        self.toolBar.addAction(self.reloadAction)
        self.toolBar.addAction(self.delAction)
        self.toolBar.addAction(self.settingsAction)

        self.toolBar.setObjectName("toolBar")
        self.toolBar.setWindowTitle("toolBar")

        self.addToolBar(Qt.TopToolBarArea, self.toolBar)

        gridLayout.addWidget(self.label, 0, 0)
        gridLayout.addWidget(self.comboBox, 0, 1)
        gridLayout.addWidget(self.label_2, 1, 0)
        gridLayout.addWidget(self.comboBox_2, 1, 1)
        gridLayout.addWidget(self.set_default_btn, 2, 0)
        gridLayout.addWidget(self.set_validate_btn, 2, 1)
        gridLayout.addWidget(self.prvs_income_lbl, 0, 2)
        gridLayout.addWidget(self.prvs_income_edit, 0, 3)
        gridLayout.addWidget(self.prvs_income_lbl_2, 1, 2)
        gridLayout.addWidget(self.prvs_income_edit_2, 1, 3)
        gridLayout.addWidget(self.rem_income_lbl, 2, 2)
        gridLayout.addWidget(self.rem_income_edit, 2, 3)

        layout.addLayout(gridLayout)
        layout.addWidget(self.tableWidget)

        self.centralwidget.setLayout(layout)
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

        db_storage.storage_db().create_tables()

        db_storage.storage_db().apply_theme(self.app)
        self.load_data()

    def OpenShowSummary(self):
        self.smryExp = ExpenseSummary()
        self.smryExp.show()

    def openWindow(self):
        self.win = None
        sender = self.sender()
        if isinstance(sender, QAction):
            if sender.text() == "New Expense":
                self.win = AddExp()
            elif sender.text() == "Edit Expense":
                self.win = EditExp()
            elif sender.text() == "Add Income":
                self.win = AddIncome()
            elif sender.text() == "Settings":
                self.win = Settings()
        self.setDisabled(True)
        self.win.win_close.connect(self.disable)
        self.win.show()

    def disable(self):
        self.load_data()
        db_storage.storage_db().apply_theme(self.app)
        self.setDisabled(False)

    def load_data(self):
        r = 0

        month = self.comboBox.currentIndex()
        year = self.comboBox_2.currentText()
        self.tableWidget.setRowCount(0)

        sender = self.sender()
        data = db_storage.storage_db().get_data_main()
        try:
            if sender.text() == "Set Default":
                data = db_storage.storage_db().get_data_main()
            elif sender.text() == "Update Data":
                data = db_storage.storage_db().get_data_for_main(month, year)
        except Exception as e:
            data = db_storage.storage_db().get_data_main()

        for row in data:
            self.tableWidget.insertRow(r)
            self.tableWidget.setItem(r, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(r, 1, QTableWidgetItem(str(row[1])))
            self.tableWidget.setItem(r, 2, QTableWidgetItem(str(row[2])))
            self.tableWidget.setItem(r, 3, QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(r, 4, QTableWidgetItem(str(row[4])))
            r += 1

        self.yrss = db_storage.storage_db().get_years_for_smry()
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.yrss)

        today = datetime.date.today()
        month = today.month-1

        rem_income = db_storage.storage_db().get_data_for_smry(month, today.year)[2]
        income, cur_month_inc = db_storage.storage_db().get_income(month, today.year)

        for cur_mnth_income in cur_month_inc:
            self.prvs_income_edit_2.setText(
                str(cur_mnth_income) if cur_mnth_income is not None else str("00"))

        self.rem_income_edit.setText(str(rem_income) if rem_income is not None else str("00"))

        for inc in income:
            self.prvs_income_edit.setText(
                str(inc) if inc is not None else str("00"))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        for window in QApplication.topLevelWidgets():
            window.close()
        self.close()

    def delete_item(self):
        if self.item is None:
            customMsgBox.MsgBox(QMessageBox.Information, "No Item Selected",
                                "No item selected. Please select an item to delete")
        else:
            db_storage.storage_db().delete_expense(self.item)
            self.item = None
        self.load_data()

    def handle_cell_clicked(self, row, column):
        self.tableWidget.selectRow(row)
        item = self.tableWidget.item(row, 0)
        self.item = int(item.text())
