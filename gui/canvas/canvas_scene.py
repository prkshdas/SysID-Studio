from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from gui.blocks.block_item import BlockItem
from gui.blocks.connection import Connection
from gui.blocks.port import Port
import logging

logger = logging.getLogger(__name__)


class CanvasSceneSignals(QObject):
    """Signals for canvas scene events"""
    itemAdded = pyqtSignal()
    itemRemoved = pyqtSignal()
    connectionAdded = pyqtSignal()
    connectionRemoved = pyqtSignal()


class CanvasScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 1000, 700)
        
        # Set background
        self.setBackgroundBrush(QColor(40, 40, 40))
        
        # Connection management
        self.current_connection = None  # Connection being drawn
        self.connections = []  # All connections on canvas
        
        # Signals
        self.signals = CanvasSceneSignals()
        self.itemAdded = self.signals.itemAdded
        self.itemRemoved = self.signals.itemRemoved
        self.connectionAdded = self.signals.connectionAdded
        self.connectionRemoved = self.signals.connectionRemoved
        
        logger.info("CanvasScene initialized")
        
    def dragEnterEvent(self, event):
        """Handle drag enter event"""
        event.accept()
        
    def dragMoveEvent(self, event):
        """Handle drag move event"""
        event.accept() 
        
    def dropEvent(self, event):
        """Handle drop event - create new block"""
        pos = event.scenePos()
        block_type = event.mimeData().text()
        
        # Create block
        block = BlockItem(block_type)
        block.setPos(pos)
        
        self.addItem(block)
        logger.info(f"Block added: {block_type} at ({pos.x():.0f}, {pos.y():.0f})")
        
        self.itemAdded.emit()
        event.accept()
    
    def mousePressEvent(self, event):
        """Handle mouse press - start connection if on port"""
        item = self.itemAt(event.scenePos(), self.views()[0].transform() if self.views() else None)
        
        if isinstance(item, Port):
            # Only allow starting connection from output ports
            if item.port_type == "output":
                self.current_connection = Connection(item)
                self.addItem(self.current_connection)
                logger.debug(f"Connection started from output port of {item.parent_block.block_type}")
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move - update temporary connection line"""
        if self.current_connection and self.current_connection.is_temporary:
            self.current_connection.set_end_pos(event.scenePos())
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release - complete connection if over input port"""
        if self.current_connection and self.current_connection.is_temporary:
            item = self.itemAt(event.scenePos(), self.views()[0].transform() if self.views() else None)
            
            # Check if dropped on an input port
            if isinstance(item, Port) and item.port_type == "input":
                # Avoid self-connection
                if item.parent_block != self.current_connection.source_port.parent_block:
                    self.current_connection.set_target(item)
                    self.connections.append(self.current_connection)
                    
                    source_block = self.current_connection.source_port.parent_block.block_type
                    target_block = item.parent_block.block_type
                    logger.info(f"Connection created: {source_block} → {target_block}")
                    
                    self.connectionAdded.emit()
                    self.current_connection = None
                else:
                    # Cancel connection - self connection
                    logger.debug("Self-connection attempted and blocked")
                    self.current_connection.disconnect()
                    self.removeItem(self.current_connection)
                    self.current_connection = None
            else:
                # Cancel connection - no valid target
                logger.debug("Connection cancelled - no valid target")
                self.current_connection.disconnect()
                self.removeItem(self.current_connection)
                self.current_connection = None
        
        super().mouseReleaseEvent(event)
    
    def get_all_connections(self):
        """Get all connections on canvas"""
        return self.connections.copy()
    
    def remove_connection(self, connection):
        """Remove a connection"""
        if connection in self.connections:
            self.connections.remove(connection)
            connection.disconnect()
            self.removeItem(connection)
            logger.info("Connection removed")
            self.connectionRemoved.emit()
    
    def clear_scene(self):
        """Clear all items and connections"""
        # Remove all connections
        for conn in self.connections.copy():
            self.remove_connection(conn)
        
        self.current_connection = None
        self.connections.clear()
        
        # Clear all items
        super().clear()
        logger.info("Canvas cleared")