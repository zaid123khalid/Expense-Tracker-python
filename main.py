from PyQt5.QtWidgets import QApplication

from UI_PY.StartupWin import StartupWin

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = StartupWin()
    ui.show()
    sys.exit(app.exec_())
