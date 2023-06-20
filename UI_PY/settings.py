from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QSlider, QCheckBox

import db_storage
from consts import fnts


class Settings(QWidget):
    win_close = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setObjectName("Form")
        self.setFixedSize(400, 300)

        self.theme_lbl = QLabel("Change Theme", self)
        self.theme_lbl.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.theme_lbl.setFont(fnts.font(weight=0))
        self.theme_lbl.setObjectName("theme_lbl")

        self.label = QLabel("Dark", self)
        self.label.setGeometry(QtCore.QRect(360, 10, 30, 20))
        self.label.setObjectName("label")

        self.label_2 = QLabel("Light", self)
        self.label_2.setGeometry(QtCore.QRect(210, 10, 30, 20))
        self.label_2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")

        self.label_3 = QLabel("Reset Data", self)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 150, 30))
        self.label_3.setFont(fnts.font(weight=0))
        self.label_3.setObjectName("label_3")

        self.horizontalSlider = QSlider(self)
        self.horizontalSlider.setGeometry(QtCore.QRect(250, 10, 90, 20))
        self.horizontalSlider.setMaximum(1)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.sliderPressed.connect(self.set_value)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setStyleSheet("""QSlider::groove:horizontal {
                border-radius: 8px;
                height: 8px;
                background-color: #CCCCCC;}
                QSlider::handle:horizontal {
                border-radius: 8px;
                width: 18px;
                background-color: #00A6FF;
                margin: -5px 0;}
                QSlider::handle:horizontal:hover {
                background-color: #DDDDDD;}
                QSlider::handle:horizontal:pressed {
                background-color: #AAAAAA;}
                QSlider{height: 20px;}""")

        self.checkBox = QCheckBox(self)
        self.checkBox.setText("reset's data if checked")
        self.checkBox.setGeometry(QtCore.QRect(210, 50, 150, 30))
        self.checkBox.stateChanged.connect(self.reset)
        self.checkBox.setObjectName("checkBox")

        self.apply_btn = QPushButton("Apply", self)
        self.apply_btn.setGeometry(QtCore.QRect(240, 260, 150, 30))
        self.apply_btn.setObjectName("apply_btn")
        self.apply_btn.clicked.connect(self.apply_settings)

        self.cancel_btn = QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(QtCore.QRect(10, 260, 150, 30))
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.close)

        QtCore.QMetaObject.connectSlotsByName(self)

    def apply_settings(self):
        text = ""
        if self.horizontalSlider.value() == 0:
            text = "Light"
        elif self.horizontalSlider.value() == 1:
            text = "Dark"
        db_storage.storage_db().apply_settings(text)

        self.close()

    def set_value(self):
        self.horizontalSlider.setValue(
            0 if self.horizontalSlider.value() == 1 else 1)

    def reset(self):
        if self.checkBox.isChecked():
            print("CHECkED")
            db_storage.storage_db().reset_data()
        else:
            print("UNCHECKED")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.win_close.emit()
        self.close()
