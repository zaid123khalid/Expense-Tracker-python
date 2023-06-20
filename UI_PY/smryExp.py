from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget, QHeaderView, \
    QTableWidgetItem

import db_storage
from UI_PY.graph_viewer import PlotWidget
from consts import mnths, fnts


class ExpenseSummary(QWidget):

    def __init__(self):
        super().__init__()
        self.showGraph = None
        self.setObjectName("Form")
        self.setFixedSize(400, 450)
        self.setWindowTitle("Expense Summary")

        self.label = QLabel("Summary", self)
        self.label.setGeometry(QtCore.QRect(10, 10, 380, 30))
        self.label.setFont(fnts.font(ptSize=14))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(230, 50, 160, 30))
        self.comboBox.addItems(mnths.months_name)
        self.comboBox.currentTextChanged.connect(self.get_data)
        self.comboBox.setObjectName("comboBox")

        self.label_2 = QLabel("Select Month", self)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 150, 30))
        self.label_2.setFont(fnts.font(weight=0))
        self.label_2.setObjectName("label_2")

        self.label_3 = QLabel("Spent Total (PKR)", self)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 150, 30))
        self.label_3.setFont(fnts.font(weight=0))
        self.label_3.setObjectName("label_3")

        self.label_4 = QLabel("Select Year", self)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 150, 30))
        self.label_4.setFont(fnts.font(weight=0))
        self.label_4.setObjectName("label_4")

        self.label_5 = QLabel("Total Income (PKR)", self)
        self.label_5.setGeometry(QtCore.QRect(10, 170, 150, 30))
        self.label_5.setFont(fnts.font(weight=0))
        self.label_5.setObjectName("label_5")

        self.label_6 = QLabel("Rem. Income (PKR)", self)
        self.label_6.setGeometry(QtCore.QRect(10, 210, 150, 30))
        self.label_6.setFont(fnts.font(weight=0))
        self.label_6.setObjectName("label_6")

        self.comboBox_2 = QComboBox(self)
        self.comboBox_2.setGeometry(QtCore.QRect(230, 90, 160, 30))
        self.comboBox_2.setObjectName("comboBox_2")

        yrss = db_storage.storage_db().get_years_for_smry()

        self.comboBox_2.addItems(yrss)

        self.comboBox_2.currentTextChanged.connect(self.get_data)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(230, 130, 160, 30))
        self.lineEdit.setFont(fnts.font(bold=True, weight=75))
        self.lineEdit.setDisabled(True)
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(230, 170, 160, 30))
        self.lineEdit_2.setFont(fnts.font(bold=True, weight=75))
        self.lineEdit_2.setDisabled(True)
        self.lineEdit_2.setObjectName("lineEdit")

        self.lineEdit_3 = QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(230, 210, 160, 30))
        self.lineEdit_3.setFont(fnts.font(bold=True, weight=75))
        self.lineEdit_3.setDisabled(True)
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(10, 250, 380, 150))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["Category", "Spent"])
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        self.cancel_btn = QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(QtCore.QRect(10, 410, 120, 30))
        self.cancel_btn.setObjectName("pushButton")
        self.cancel_btn.clicked.connect(self.close)

        self.show_graph_btn = QPushButton("Show Visualized Data", self)
        self.show_graph_btn.setGeometry(QtCore.QRect(270, 410, 120, 30))
        self.show_graph_btn.setObjectName("pushButton")
        self.show_graph_btn.clicked.connect(self.show_graph)

        QtCore.QMetaObject.connectSlotsByName(self)

    def get_data(self):
        r = 0
        month = self.comboBox.currentIndex()
        year = self.comboBox_2.currentText()

        spent, income, rem_income, spend = db_storage.storage_db().get_data_for_smry(month, year)

        self.lineEdit.setText(str(spent))
        self.lineEdit_2.setText(str(income))
        self.lineEdit_3.setText(str(rem_income))

        self.label.setText(
            f"Summary for the month: {self.comboBox.currentText()}, {year}")

        self.tableWidget.setRowCount(0)

        for row in spend:
            self.tableWidget.insertRow(r)
            self.tableWidget.setItem(r, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(r, 1, QTableWidgetItem(str(row[1])))
            r += 1

    def show_graph(self):
        self.showGraph = PlotWidget(
            mnths.months[self.comboBox.currentIndex()], self.comboBox_2.currentText())
        self.showGraph.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close()
