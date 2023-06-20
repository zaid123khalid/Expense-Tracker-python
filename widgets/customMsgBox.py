from PyQt5.QtWidgets import QMessageBox


class MsgBox(QMessageBox):
    def __init__(self, icon: QMessageBox.Icon, win_title: str, text: str):
        super(MsgBox, self).__init__()
        self.setIcon(icon)
        self.setWindowTitle(win_title)
        self.setText(text)
        self.setStyleSheet("""QPushButton {
                min-width: 100px;
                min-height: 30px;
                max-width: 100px;
                max-height: 30px;
            }""")
        self.exec_()
