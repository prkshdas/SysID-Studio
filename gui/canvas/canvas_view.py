from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter
from .canvas_scene import CanvasScene
import logging

logger = logging.getLogger(__name__)


class CanvasView(QGraphicsView):
    def __init__(self):
        super().__init__()
        
        # Create and set scene
        self.scene = CanvasScene()
        self.setScene(self.scene)
        
        # Rendering setup - use QGraphicsView.RenderHint enum
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        
        # Drag and drop
        self.setAcceptDrops(True)
        
        # View mode
        self.setDragMode(QGraphicsView.RubberBandDrag)
        
        # Styling
        self.setStyleSheet("QGraphicsView { background-color: #282828; border: none; }")
        
        # Zoom tracking
        self.zoom_level = 1.0
        self.max_zoom = 3.0
        self.min_zoom = 0.3
        
        logger.info("CanvasView initialized")
    
    def keyPressEvent(self, event):
        """Handle key presses"""
        if event.key() == Qt.Key_Delete:
            # Delete selected items
            deleted_count = 0
            for item in self.scene.selectedItems():
                if hasattr(item, 'disconnect') and hasattr(item, 'source_port'):
                    # It's a connection
                    self.scene.remove_connection(item)
                    deleted_count += 1
                elif hasattr(item, 'get_all_ports'):
                    # It's a block - delete all its connections first
                    for port in item.get_all_ports():
                        for conn in port.connections.copy():
                            self.scene.remove_connection(conn)
                    
                    self.scene.removeItem(item)
                    deleted_count += 1
                    logger.info(f"Block deleted: {item.block_type}")
            
            if deleted_count > 0:
                logger.info(f"Deleted {deleted_count} item(s)")
        
        elif event.key() == Qt.Key_Escape:
            # Deselect all
            self.scene.clearSelection()
            logger.debug("All items deselected")
        
        elif event.key() == Qt.Key_A and event.modifiers() == Qt.ControlModifier:
            # Select all
            for item in self.scene.items():
                item.setSelected(True)
            logger.debug("All items selected")
        
        super().keyPressEvent(event)
    
    def wheelEvent(self, event):
        """Handle mouse wheel zoom"""
        # Calculate zoom factor
        zoom_in = event.angleDelta().y() > 0
        zoom_factor = 1.1 if zoom_in else 0.9
        
        # Calculate new zoom level
        new_zoom = self.zoom_level * zoom_factor
        
        # Clamp zoom level
        if self.min_zoom <= new_zoom <= self.max_zoom:
            self.scale(zoom_factor, zoom_factor)
            self.zoom_level = new_zoom
            logger.debug(f"Zoom level: {self.zoom_level:.2f}x")
        
        event.accept()
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        super().mouseReleaseEvent(event)
    
    def dragEnterEvent(self, event):
        """Handle drag enter"""
        event.accept()
    
    def dragMoveEvent(self, event):
        """Handle drag move"""
        event.accept()
    
    def dropEvent(self, event):
        """Handle drop"""
        # Map viewport coordinates to scene coordinates
        scene_pos = self.mapToScene(event.pos())
        
        # Create a new event at the scene position
        from PyQt5.QtGui import QDropEvent
        new_event = QDropEvent(
            event.pos(),
            event.possibleActions(),
            event.mimeData(),
            event.mouseButtons(),
            event.keyboardModifiers()
        )
        
        # Temporarily update scene position
        scene_pos_store = scene_pos
        self.scene.dropEvent(new_event)
        
        event.accept()