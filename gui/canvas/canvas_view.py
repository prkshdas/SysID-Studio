from PyQt5.QtWidgets import QGraphicsView, QFrame
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QDrag, QDropEvent
from .canvas_scene import CanvasScene
import logging

class CanvasView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configure the view
        self._configure()
        
        # Set up scene
        self.scene = CanvasScene(self)
        self.setScene(self.scene)
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.info("CanvasView initialized")

    def _configure(self):
        """Set up the configuration and styling of the view."""
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        self.setAcceptDrops(True)

    def wheelEvent(self, event):
        """Zoom in or out on the canvas with the mouse wheel."""
        zoom_factor = 1.15
        if event.angleDelta().y() < 0:
            zoom_factor = 1.0 / zoom_factor
            
        self.scale(zoom_factor, zoom_factor)
        self.logger.info(f"Canvas zoomed with factor: {zoom_factor:.2f}")

    def keyPressEvent(self, event):
        """Handle key presses on the canvas."""
        if event.key() == Qt.Key_Delete:
            self.scene.delete_selected_items()
            self.logger.info("Delete key pressed, selected items removed")
        elif event.key() == Qt.Key_Space:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """Reset drag mode when spacebar is released."""
        if event.key() == Qt.Key_Space:
            self.setDragMode(QGraphicsView.RubberBandDrag)
        else:
            super().keyReleaseEvent(event)
            
    # --- Drag and Drop Events ---
    
    def dragEnterEvent(self, event):
        """Accept drag events if they have the correct MIME type."""
        if event.mimeData().hasFormat('application/x-block-item'):
            event.acceptProposedAction()
            self.logger.debug("Drag enter event accepted")
        else:
            event.ignore()
            self.logger.debug("Drag enter event ignored (invalid MIME type)")

    def dragMoveEvent(self, event):
        """Accept drag move events."""
        if event.mimeData().hasFormat('application/x-block-item'):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Handle dropping an item onto the canvas."""
        if event.mimeData().hasFormat('application/x-block-item'):
            # The position where the item is dropped
            drop_pos = event.pos()
            
            # Convert view coordinates to scene coordinates
            scene_pos = self.mapToScene(drop_pos)
            
            # Pass the scene position and MIME data to the scene's drop handler
            self.scene.handle_drop(scene_pos, event.mimeData())
            
            event.acceptProposedAction()
            self.logger.info(f"Block dropped at scene position: {scene_pos}")
        else:
            event.ignore()
            self.logger.warning("Drop event ignored (invalid MIME type)")
