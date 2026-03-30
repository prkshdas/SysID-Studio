from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import QRectF, Qt, QPointF


class Port(QGraphicsItem):
    PORT_RADIUS = 6

    def __init__(self, parent_block, port_type, port_index=0):
        super().__init__(parent_block)

        self.parent_block = parent_block
        self.port_type = port_type  # "input" or "output"
        self.port_index = port_index
        self.connections = []

        # Make ports clickable
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setAcceptHoverEvents(True)

        self._update_position()

    def _update_position(self):
        block_height = self.parent_block.height
        # spacing for multiple ports (future-proof)
        port_spacing = block_height / max(2, (1 + 1 + 1))  # (ports + padding)
        y_offset = port_spacing * (self.port_index + 1)

        if self.port_type == "input":
            x_offset = 0 - self.PORT_RADIUS
        else:
            x_offset = self.parent_block.width - self.PORT_RADIUS

        self.setPos(x_offset, y_offset)

    def boundingRect(self):
        r = self.PORT_RADIUS
        return QRectF(-r, -r, 2 * r, 2 * r)

    def paint(self, painter: QPainter, option, widget):
        connected = len(self.connections) > 0
        if connected:
            fill = QColor(100, 200, 100)
        else:
            fill = QColor(160, 160, 160)

        painter.setBrush(QBrush(fill))
        painter.setPen(QPen(Qt.darkGray, 1))
        r = self.PORT_RADIUS
        painter.drawEllipse(-r, -r, 2 * r, 2 * r)

    def get_center_pos(self):
        # Center of the port in scene coords
        return self.mapToScene(QPointF(0, 0))

    def add_connection(self, connection):
        if connection not in self.connections:
            self.connections.append(connection)
            self.update()

    def remove_connection(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)
            self.update()