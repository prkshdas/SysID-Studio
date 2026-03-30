from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import pyqtSignal, Qt
from ..blocks.block_item import BlockItem
from ..blocks.connection import Connection
import logging

logger = logging.getLogger(__name__)

class CanvasScene(QGraphicsScene):
    """The canvas scene where blocks and connections are drawn"""

    # Define custom signals
    itemAdded = pyqtSignal(QGraphicsItem)
    itemRemoved = pyqtSignal(QGraphicsItem)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackgroundBrush(Qt.darkGray)
        self.connections = []
        self.pending_connection = None
        logger.info("CanvasScene initialized")

    def add_block(self, block_type, position):
        """Adds a new block to the scene at the given position"""
        block = BlockItem(block_type)
        block.setPos(position)
        self.addItem(block)
        self.itemAdded.emit(block) # Emit signal
        logger.info(f"Added block '{block_type}' at {position}")
        return block

    def clear_scene(self):
        """Removes all items from the scene"""
        # Create a copy of the list of items to iterate over
        items_to_remove = self.items()
        for item in items_to_remove:
            self.removeItem(item)
            self.itemRemoved.emit(item) # Emit signal for each removed item
        self.connections.clear()
        logger.info("Canvas cleared")

    def keyPressEvent(self, event):
        """Handle key presses (e.g., Delete key to remove items)"""
        if event.key() == Qt.Key_Delete:
            selected_items = self.selectedItems()
            for item in selected_items:
                # If it's a block, remove its connections first
                if isinstance(item, BlockItem):
                    for port in item.get_all_ports():
                        for conn in list(port.connections):
                            self.remove_connection(conn)
                # Remove the item itself
                self.removeItem(item)
                self.itemRemoved.emit(item) # Emit signal
        else:
            super().keyPressEvent(event)
            
    def remove_connection(self, connection):
        """Safely removes a connection from the scene and ports"""
        connection.disconnect()
        if connection in self.connections:
            self.connections.remove(connection)
        self.removeItem(connection)
        self.itemRemoved.emit(connection) # Emit signal
        