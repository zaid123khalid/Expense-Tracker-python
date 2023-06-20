import sqlite3

import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self, month="", year=""):
        super().__init__()
        self.setWindowTitle('Pie Chart')
        self.resize(640, 480)
        self.setMinimumSize(450, 350)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas)

        spent = []
        incomes = []
        ctg_name = []

        dbConn = sqlite3.connect("expense.db")
        connCur = dbConn.cursor()
        income = connCur.execute("""SELECT SUM(Income) AS total_income from incomes WHERE strftime('%m', SpendDate) = 
        ? AND strftime('%Y', SpendDate) = ?""", (month,year))

        for r in income:
            if r[0] is not None:
                incomes.append(r[0])

        connCur.close()

        dbConn = sqlite3.connect("expense.db")
        connCur = dbConn.cursor()
        spend = connCur.execute("""SELECT Category, SUM(Spend) AS total_spent from expenses 
                WHERE strftime('%m', SpendDate) = ? AND strftime('%Y', SpendDate) = ? GROUP BY Category""",
                                (month, year))

        for row in spend:
            ctg_name.append(row[0])
            spent.append(row[1])

        connCur.close()

        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Graph representation for the Expense")
        self.ax.axis('off')

        self.ax.pie(spent, labels=ctg_name, autopct='%1.1f%%')

        sum_spent = sum(spent)
        sum_income = sum(incomes)
        self.ax.text(-2.3, -1.4, 'Expense(PKR): ' + str(sum_spent), fontsize=12, fontweight='bold', ha='left')
        self.ax.text(-2.3, -1.15, 'Income(PKR): ' + str(sum_income), fontsize=12, fontweight='bold', ha='left')

        layout = QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
