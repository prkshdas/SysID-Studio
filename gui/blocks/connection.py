from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPointF, QRectF


class Connection(QGraphicsItem):
    def __init__(self, source_port, target_port=None):
        super().__init__()

        self.source_port = source_port
        self.target_port = target_port
        self.is_temporary = target_port is None
        self.temp_end_pos = QPointF(0, 0)

        if source_port:
            source_port.add_connection(self)
        if target_port:
            target_port.add_connection(self)

        self.setZValue(-1)

    def set_target(self, target_port):
        if self.target_port:
            self.target_port.remove_connection(self)

        self.target_port = target_port
        self.is_temporary = False

        if target_port:
            target_port.add_connection(self)

        self.prepareGeometryChange()
        self.update()

    def set_end_pos(self, pos):
        self.temp_end_pos = QPointF(pos)
        self.prepareGeometryChange()
        self.update()

    def _endpoints(self):
        start = self.source_port.get_center_pos()
        if self.is_temporary:
            end = self.temp_end_pos
        else:
            end = self.target_port.get_center_pos()
        return start, end

    def boundingRect(self):
        start, end = self._endpoints()

        # QRectF(QPointF, QPointF) gives a rect spanning the two points; normalize handles any direction.
        rect = QRectF(start, end).normalized()

        # pad for pen width + easier picking
        pad = 6.0
        rect.adjust(-pad, -pad, pad, pad)
        return rect

    def paint(self, painter: QPainter, option, widget):
        start, end = self._endpoints()

        if self.is_temporary:
            pen = QPen(QColor(120, 120, 255), 2, Qt.DashLine)
        else:
            pen = QPen(QColor(100, 200, 100), 2)

        painter.setPen(pen)
        painter.drawLine(start, end)

    def disconnect(self):
        if self.source_port:
            self.source_port.remove_connection(self)
        if self.target_port:
            self.target_port.remove_connection(self)