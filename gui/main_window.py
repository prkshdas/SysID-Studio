from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from .canvas.canvas_view import CanvasView
from .library.library_panel import LibraryPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("SysID Studio - Canvas")
        
        self.canvas = CanvasView()
        self.library = LibraryPanel()
        
        self.library.setFixedWidth(200)
        
        layout = QHBoxLayout()
        layout.addWidget(self.library)
        layout.addWidget(self.canvas)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)
        