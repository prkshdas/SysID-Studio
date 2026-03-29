import sys
import pandas as pd
import numpy as np
from scipy.signal import detrend

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QFileDialog, QVBoxLayout, QWidget, QLabel, QCheckBox
)

import pyqtgraph as pg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SysID Studio - Data Viewer")

        self.df = None
        self.u = None
        self.y = None
        self.t = None

        # Widgets
        self.load_btn = QPushButton("Load CSV")
        self.plot_btn = QPushButton("Plot u & y")
        self.plot_btn.setEnabled(False)

        self.dc_checkbox = QCheckBox("Remove DC (mean)")
        self.detrend_checkbox = QCheckBox("Detrend (remove slope)")

        self.status_label = QLabel("No file loaded")

        self.plot = pg.PlotWidget()
        self.plot.addLegend()
        self.plot.setLabel('bottom', 'Time')
        self.plot.setLabel('left', 'Signal')

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.load_btn)
        layout.addWidget(self.dc_checkbox)
        layout.addWidget(self.detrend_checkbox)
        layout.addWidget(self.plot_btn)
        layout.addWidget(self.status_label)
        layout.addWidget(self.plot)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Signals
        self.load_btn.clicked.connect(self.load_csv)
        self.plot_btn.clicked.connect(self.plot_data)

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        self.df = pd.read_csv(file_path)

        # Check required columns
        if 'u' not in self.df.columns or 'y' not in self.df.columns:
            self.status_label.setText("CSV must contain 'u' and 'y' columns")
            return

        self.u = self.df['u'].values
        self.y = self.df['y'].values

        # Generate time index
        self.t = np.arange(len(self.u))

        self.plot_btn.setEnabled(True)

        self.status_label.setText(f"Loaded: {file_path}")
        self.plot.clear()

    def plot_data(self):
        if self.u is None or self.y is None:
            return

        u = self.u.copy()
        y = self.y.copy()

        operations = []

        # Remove DC
        if self.dc_checkbox.isChecked():
            u = u - np.mean(u)
            y = y - np.mean(y)
            operations.append("DC Removed")

        # Detrend
        if self.detrend_checkbox.isChecked():
            u = detrend(u)
            y = detrend(y)
            operations.append("Detrended")

        self.plot.clear()

        self.plot.plot(self.t, u, pen='b', name="u (input)")
        self.plot.plot(self.t, y, pen='r', name="y (output)")

        if operations:
            mode = " + ".join(operations)
        else:
            mode = "Raw"

        self.status_label.setText(f"Plotted ({mode}) data")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Optional: Fix high DPI scaling (Windows)
    try:
        from PyQt5.QtCore import Qt
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    except:
        pass

    window = MainWindow()
    window.resize(900, 600)
    window.show()
    sys.exit(app.exec_())