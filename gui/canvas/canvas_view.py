from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt
from .canvas_scene import CanvasScene

class CanvasView(QGraphicsView):
    def __init__(self):
        super().__init__()
        
        self.scene = CanvasScene()
        self.setScene(self.scene)
        
        self.setRenderHints(self.renderHints())
        self.setAcceptDrops(True)
        
         # Enable rubber band selection (Ctrl+Click)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        
        # Set dark background
        self.setStyleSheet("QGraphicsView { background-color: #282828; }")
        
        
    def keyPressEvent(self, event):
        # Handle key presses
        if event.key() == Qt.Key_Delete:
            # Delete selected items
            for item in self.scene.selectedItems():
                if hasattr(item, 'disconnect'):
                    # It's a connection
                    self.scene.remove_connection(item)
                elif hasattr(item, 'get_all_ports'):
                    # It's a block - delete all its connections first
                    for port in item.get_all_ports():
                        for conn in port.connections.copy():
                            self.scene.remove_connection(conn)
                    
                    self.scene.removeItem(item)
        
        super().keyPressEvent(event)
    
    def wheelEvent(self, event):
        # Handle mouse wheel zoom
        zoom_factor = 1.1
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.scale(1 / zoom_factor, 1 / zoom_factor)