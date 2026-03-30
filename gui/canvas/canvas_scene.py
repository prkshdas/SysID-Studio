from PyQt5.QtWidgets import QGraphicsScene, QMessageBox
from PyQt5.QtCore import Qt
from ..blocks.block_item import BlockItem
from ..blocks.connection import Connection
import logging

class CanvasScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Scene settings
        self.setBackgroundBrush(Qt.gray)
        
        # Store connections
        self.connections = []
        
        # For drawing new connections
        self.is_connecting = False
        self.temp_connection = None
        self.start_port = None
        
        # Logging
        self.logger = logging.getLogger(__name__)
        self.logger.info("CanvasScene initialized")

    def handle_drop(self, scene_pos, mime_data):
        """
        Handles a drop event by creating and placing a new block on the canvas.
        
        Args:
            scene_pos: The position in scene coordinates where the drop occurred.
            mime_data: The MIME data from the drop event, containing block info.
        """
        if mime_data.hasFormat('application/x-block-item'):
            block_type_data = mime_data.data('application/x-block-item')
            block_type = str(block_type_data, encoding='utf-8')
            
            # Create a new block at the drop position
            new_block = BlockItem(block_type)
            new_block.setPos(scene_pos)
            self.addItem(new_block)
            
            self.logger.info(f"Created new block '{block_type}' at {scene_pos}")
            self.update()

    def delete_selected_items(self):
        """Deletes all selected items (blocks and connections) from the scene."""
        selected_items = self.selectedItems()
        if not selected_items:
            return

        reply = QMessageBox.question(
            None,
            "Delete Items",
            f"Are you sure you want to delete {len(selected_items)} selected item(s)?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for item in selected_items:
                if isinstance(item, BlockItem):
                    # Remove the block and any connected connections
                    self.remove_block(item)
                elif isinstance(item, Connection):
                    # Disconnect and remove the connection
                    self.remove_connection(item)
            self.logger.info(f"Deleted {len(selected_items)} items")

    def remove_block(self, block: BlockItem):
        """Removes a block and all its connections."""
        for port in block.get_all_ports():
            # Create a copy of the connections list to iterate over
            for conn in list(port.connections):
                self.remove_connection(conn)
        self.removeItem(block)

    def remove_connection(self, connection: Connection):
        """Disconnects and removes a single connection from the scene."""
        if connection in self.connections:
            connection.disconnect()
            self.removeItem(connection)
            self.connections.remove(connection)

    def clear_scene(self):
        """Clears all items from the canvas."""
        for item in self.items():
            self.removeItem(item)
        self.connections.clear()
        self.logger.info("Canvas cleared")
        self.update()
