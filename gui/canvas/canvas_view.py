from PyQt5.QtWidgets import QGraphicsView, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QDropEvent
from .canvas_scene import CanvasScene
import logging


class CanvasView(QGraphicsView):
    MIME_TYPE = "application/x-block-item"

    def __init__(self, parent=None):
        super().__init__(parent)

        self.logger = logging.getLogger(__name__)

        self._configure()

        self.scene = CanvasScene(self)
        self.setScene(self.scene)

        # Helpful so key events (Delete) go to the view
        self.setFocusPolicy(Qt.StrongFocus)

        self.logger.info("CanvasView initialized")

    def _configure(self):
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
        zoom_factor = 1.15
        if event.angleDelta().y() < 0:
            zoom_factor = 1.0 / zoom_factor
        self.scale(zoom_factor, zoom_factor)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            # Let the scene remove items safely
            self.scene.delete_selected_items()
            return
        elif event.key() == Qt.Key_Space:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            return
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.setDragMode(QGraphicsView.RubberBandDrag)
            return
        super().keyReleaseEvent(event)

    # --- Drag and Drop Events ---

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(self.MIME_TYPE) or event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat(self.MIME_TYPE) or event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasFormat(self.MIME_TYPE) or event.mimeData().hasText():
            scene_pos = self.mapToScene(event.pos())
            self.scene.handle_drop(scene_pos, event.mimeData())
            event.acceptProposedAction()
        else:
            event.ignore()