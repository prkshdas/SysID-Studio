from PyQt5.QtWidgets import QGraphicsView
from .canvas_scene import CanvasScene

class CanvasView(QGraphicsView):
    def __init__(self):
        super().__init__()
        
        self.scene = CanvasScene()
        self.setScene(self.scene)
        
        self.setRenderHints(self.renderHints())
        self.setAcceptDrops(True)
        
        self.setDragMode(QGraphicsView.RubberBandDrag)