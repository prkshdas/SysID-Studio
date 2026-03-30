from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import QLineF, Qt

class Connection(QGraphicsItem):
    # draw a line between connecting ports
    
    def __init__(self, source_port, target_port=None):
        super().__init__()
        
        self.source_port = source_port
        self.target_port = target_port
        self.is_temporary = target_port is None   # for drawing while connecting
        
        # add to source port's connections
        if source_port:
            source_port.add_connection(self)
            
        # add to target port's connections if exists
        if target_port:
            target_port.add_connection(self)
            
        self.setZValue(-1)  # draw behind blocks
        
    
    def set_target(self, target_port):
        # set or update the target port
        if self.target_port:
            self.target_port.remove_connection(self)
            
        self.target_port = target_port
        self.is_temporary = False
        
        if target_port:
            target_port.add_connection(self)
            
        self.update()
        
    def set_end_pos(self, pos):
        # Set temporary end position (for drawing while connecting)
        self.temp_end_pos = pos
        self.update()
    
    def boundingRect(self):
        # Calculate bounding rectangle for the connection line
        if self.is_temporary:
            start = self.source_port.get_center_pos()
            end = self.temp_end_pos
        else:
            start = self.source_port.get_center_pos()
            end = self.target_port.get_center_pos()
        
        line = QLineF(start, end)
        rect = line.boundingRect()
        rect.adjust(-2, -2, 2, 2)  # Add padding for pen width
        return rect
    
    def paint(self, painter: QPainter, option, widget):
        # Draw the connection line
        if self.is_temporary:
            start = self.source_port.get_center_pos()
            end = self.temp_end_pos
        else:
            start = self.source_port.get_center_pos()
            end = self.target_port.get_center_pos()
        
        # Line styling
        if self.is_temporary:
            pen = QPen(QColor(100, 100, 255), 2, Qt.DashLine)  # Blue dashed while connecting
        else:
            pen = QPen(QColor(100, 200, 100), 2)  # Green solid when connected
        
        painter.setPen(pen)
        painter.drawLine(start, end)
    
    def disconnect(self):
        # Disconnect this connection
        if self.source_port:
            self.source_port.remove_connection(self)
        if self.target_port:
            self.target_port.remove_connection(self)