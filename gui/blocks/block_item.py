from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import QRectF, Qt
from .port import Port


class BlockItem(QGraphicsItem):
    def __init__(self, block_type="Block", parent=None):
        super().__init__(parent)

        self.block_type = block_type
        self.width = 120
        self.height = 60

        # Enable interaction
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        # Ports (children of this item, so they move with the block)
        self.input_ports = [Port(self, "input", 0)]
        self.output_ports = [Port(self, "output", 0)]

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter: QPainter, option, widget):
        # Background
        color = QColor(60, 60, 60)
        if self.isSelected():
            color = QColor(100, 150, 255)

        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.black, 2))
        painter.drawRoundedRect(self.boundingRect(), 6, 6)

        # Draw text (block name)
        painter.setPen(Qt.white)
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self.block_type)

    def get_input_ports(self):
        return self.input_ports

    def get_output_ports(self):
        return self.output_ports

    def get_all_ports(self):
        return self.input_ports + self.output_ports

    def itemChange(self, change, value):
        # Ensure connections update when the block moves
        if change == QGraphicsItem.ItemPositionHasChanged:
            for port in self.get_all_ports():
                for conn in list(port.connections):
                    conn.update()
        return super().itemChange(change, value)