from PyQt5 import QtGui


class font(QtGui.QFont):
    def __init__(self, ptSize=12, bold=False, weight=75):
        super(font, self).__init__()
        self.setPointSize(ptSize)
        self.setBold(bold)
        self.setWeight(weight)
