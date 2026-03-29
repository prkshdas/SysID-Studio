from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import QRectF, Qt


class BlockItem(QGraphicsItem):
    def __init__(self, block_type="Block"):
        super().__init__()

        self.block_type = block_type
        self.width = 100
        self.height = 50

        # Enable interaction
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter: QPainter, option, widget):
        # Background
        color = QColor(60, 60, 60)
        if self.isSelected():
            color = QColor(100, 150, 255)

        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.black))
        painter.drawRect(self.boundingRect())

        # Draw text (block name)
        painter.setPen(Qt.white)
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self.block_type)