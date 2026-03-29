import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(1000, 600)
    window.show()

    sys.exit(app.exec_())