from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from gui.blocks.block_item import BlockItem
from gui.blocks.connection import Connection
from gui.blocks.port import Port



class CanvasScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 800, 600)
        
        # Connection management
        self.current_connection = None  # Connection being drawn
        self.connections = []  # All connections on canvas
        
        # Background color
        self.setBackgroundBrush(QColor(40, 40, 40))
        
    def dragEnterEvent(self, event):
        event.accept()
        
    def dragMoveEvent(self, event):
        event.accept() 
        
    def dropEvent(self, event):
        pos = event.scenePos()
          
        block_type = event.mimeData().text()
        
        block = BlockItem(block_type)
        block.setPos(pos)
        
        self.addItem(block)
        
        event.accept()   
        
        
    def mousePressEvent(self, event):
        # Handle mouse press - start connection if on port
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        
        if isinstance(item, Port):
            # Only allow starting connection from output ports
            if item.port_type == "output":
                self.current_connection = Connection(item)
                self.addItem(self.current_connection)
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        # Handle mouse move - update temporary connection line
        if self.current_connection and self.current_connection.is_temporary:
            self.current_connection.set_end_pos(event.scenePos())
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        # Handle mouse release - complete connection if over input port
        if self.current_connection and self.current_connection.is_temporary:
            item = self.itemAt(event.scenePos(), self.views()[0].transform())
            
            # Check if dropped on an input port
            if isinstance(item, Port) and item.port_type == "input":
                # Avoid self-connection
                if item.parent_block != self.current_connection.source_port.parent_block:
                    self.current_connection.set_target(item)
                else:
                    # Cancel connection
                    self.current_connection.disconnect()
                    self.removeItem(self.current_connection)
                    self.current_connection = None
            else:
                # Cancel connection - no valid target
                self.current_connection.disconnect()
                self.removeItem(self.current_connection)
                self.current_connection = None
        
        super().mouseReleaseEvent(event)
    
    def add_connection(self, connection):
        # Register a connection
        if connection not in self.connections:
            self.connections.append(connection)
    
    def remove_connection(self, connection):
        # Unregister and remove a connection
        if connection in self.connections:
            self.connections.remove(connection)
            connection.disconnect()
            self.removeItem(connection)
    
    def get_all_connections(self):
        # Get all connections on canvas
        return self.connections.copy()
    
    def clear_scene(self):
        # Clear all items and connections
        # Remove all connections
        for conn in self.connections.copy():
            self.remove_connection(conn)
        
        self.current_connection = None
        self.connections.clear()
        
        super().clear()