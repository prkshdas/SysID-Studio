from PyQt5.QtWidgets import QGraphicsView


class CanvasView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)