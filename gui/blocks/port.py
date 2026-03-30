from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import QRectF, Qt, QPointF


class Port(QGraphicsItem):
    # add input and output ports on block
    
    PORT_RADIUS = 5
    PORT_TYPES = {"input": 0, "output": 1}
    
    def __init__(self, parent_block, port_type, port_index=0):
        super().__init__(parent_block)
        
        self.parent_block = parent_block
        self.port_type = port_type # input or output
        self.port_index = port_index
        self.connections = []  # connected connection objects
        
        # calculate porition based on port type and index
        self._update_position()
        
    def _update_position(self):
        # calculate the port position on the block
        block_height = self.parent_block.height
        port_spacing = block_height / (max(2, self.parent_block.port_count + 1))
        y_offset = port_spacing * (self.port_index + 1)
        
        if self.port_type == "input":
            x_offset = -self.PORT_RADIUS
        else:
            x_offset = self.parent_block.width - self.PORT_RADIUS
            
        self.setPos(x_offset, y_offset - self.PORT_RADIUS)
        
    def boundingRect(self):
        return QRectF(-self.PORT_RADIUS, -self.PORT_RADIUS, self.PORT_RADIUS * 2, self.PORT_RADIUS * 2)
    
    def paint(self, painter: QPainter, option, widget):
        #port color based on connection state
        if len(self.connections) > 0:
            color = QColor(100, 200, 100) # green when connected
        else:
            color = QColor(150, 150, 150) # Gray when not connected
        
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.drawEllipse(-self.PORT_RADIUS, -self.PORT_RADIUS, self.PORT_RADIUS * 2, self.PORT_RADIUS * 2)
        
    def get_center_pos(self):
        # get center position of the port
        return self.mapToScene(QPointF(self.PORT_RADIUS, self.PORT_RADIUS))
    
    def add_connection(self, connection):
        # add connection to the block
        if connection not in self.connections:
            self.connections.append(connection)
            self.update()
            
    def remove_connection(self, connection):
        # remove connection from block
        if connection in self.connections:
            self.connections.remove(connection)
            self.update()