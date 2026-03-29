from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from .canvas.canvas_view import CanvasView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("SysID Studio - Canvas")
        
        self.canvas = CanvasView()
        
        layout = QHBoxLayout()
        layout.addWidget(self.canvas)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)
        