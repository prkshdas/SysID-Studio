from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import QRectF, Qt
from .port import Port


class BlockItem(QGraphicsItem):
    def __init__(self, block_type="Block", parent=None):
        super().__init__(parent)

        self.block_type = block_type
        self.width = 100
        self.height = 50
        self.port_count = 2 # 1 input, 1 output by default

        # Enable interaction
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        
        # create ports
        self.input_ports = [Port(self, "input", 0)]
        self.output_ports = [Port(self, "output", 0)]
        
        self.addToGroup(self.input_ports[0])
        self.addToGroup(self.output_ports[0])
        

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter: QPainter, option, widget):
        # Background
        color = QColor(60, 60, 60)
        if self.isSelected():
            color = QColor(100, 150, 255)

        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.black, 2))
        painter.drawRect(self.boundingRect())

        # Draw text (block name)
        painter.setPen(Qt.white)
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self.block_type)
        
    def get_input_ports(self):
        # get all input ports
        return self.input_ports
    
    def get_output_ports(self):
        # get all output ports
        return self.output_ports
    
    def get_all_ports(self):
        # get all ports
        return self.input_ports + self.output_ports