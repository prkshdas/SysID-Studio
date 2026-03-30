from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import pyqtSignal, Qt
from ..blocks.block_item import BlockItem
from ..blocks.connection import Connection
from ..blocks.port import Port
import logging

logger = logging.getLogger(__name__)


class CanvasScene(QGraphicsScene):
    """The canvas scene where blocks and connections are drawn"""

    itemAdded = pyqtSignal(QGraphicsItem)
    itemRemoved = pyqtSignal(QGraphicsItem)

    MIME_TYPE = "application/x-block-item"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackgroundBrush(Qt.darkGray)

        self.connections = []
        self.pending_connection = None

        logger.info("CanvasScene initialized")

    def add_block(self, block_type, position):
        block = BlockItem(block_type)
        block.setPos(position)
        self.addItem(block)
        self.itemAdded.emit(block)
        return block

    def handle_drop(self, scene_pos, mime):
        block_type = None

        if mime.hasFormat(self.MIME_TYPE):
            try:
                block_type = bytes(mime.data(self.MIME_TYPE)).decode("utf-8")
            except Exception:
                block_type = None

        if not block_type and mime.hasText():
            block_type = mime.text()

        if not block_type:
            logger.warning("Drop ignored: could not determine block type")
            return

        self.add_block(block_type, scene_pos)
        logger.info("Added block from drop: %s", block_type)

    def delete_selected_items(self):
        selected_items = self.selectedItems()
        for item in selected_items:
            if isinstance(item, BlockItem):
                for port in item.get_all_ports():
                    for conn in list(port.connections):
                        self.remove_connection(conn)

            if isinstance(item, Connection):
                self.remove_connection(item)
                continue

            self.removeItem(item)
            self.itemRemoved.emit(item)

    def clear_scene(self):
        # cancel pending connection safely
        if self.pending_connection:
            try:
                self.removeItem(self.pending_connection)
            except Exception:
                pass
            try:
                self.pending_connection.disconnect()
            except Exception:
                pass
            self.pending_connection = None

        for item in list(self.items()):
            self.removeItem(item)
            self.itemRemoved.emit(item)

        self.connections.clear()

    def remove_connection(self, connection: Connection):
        if not connection:
            return

        try:
            connection.disconnect()
        except Exception:
            pass

        if connection in self.connections:
            self.connections.remove(connection)

        self.removeItem(connection)
        self.itemRemoved.emit(connection)

    # ---- Connection mouse interaction ----

    def _top_item_at(self, scene_pos):
        """
        Robust hit-test without device transforms (avoids crashes/segfaults).
        Returns the topmost item at scene_pos, or None.
        """
        items = self.items(scene_pos)
        return items[0] if items else None

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            super().mousePressEvent(event)
            return

        clicked = self._top_item_at(event.scenePos())

        # If we are currently drawing a connection:
        if self.pending_connection is not None:
            # If clicked an input port, finalize
            if isinstance(clicked, Port) and clicked.port_type == "input":
                self.pending_connection.set_target(clicked)
                self.connections.append(self.pending_connection)
                self.pending_connection = None
                event.accept()
                return

            # Otherwise cancel pending connection on any other left click
            self.removeItem(self.pending_connection)
            self.pending_connection.disconnect()
            self.pending_connection = None
            event.accept()
            return

        # Start connection only if clicking an OUTPUT port
        if isinstance(clicked, Port) and clicked.port_type == "output":
            conn = Connection(source_port=clicked, target_port=None)
            conn.set_end_pos(event.scenePos())  # IMPORTANT: initialize end pos
            self.addItem(conn)
            self.pending_connection = conn
            event.accept()
            return

        # default behavior (selection/move)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.pending_connection is not None:
            self.pending_connection.set_end_pos(event.scenePos())
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)