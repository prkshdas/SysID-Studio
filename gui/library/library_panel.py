from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import Qt, QMimeData, QByteArray


class LibraryPanel(QListWidget):
    """
    Drag source for blocks. We export a custom MIME type so the canvas can
    reliably detect drops and parse the block type.
    """

    MIME_TYPE = "application/x-block-item"

    def __init__(self):
        super().__init__()

        self.addItem("Gain Block")
        self.addItem("Constant Block")
        self.addItem("Scope")

        self.setDragEnabled(True)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if not item:
            return

        block_type = item.text()

        mime = QMimeData()
        # Custom format used by CanvasView/CanvasScene
        mime.setData(self.MIME_TYPE, QByteArray(block_type.encode("utf-8")))
        # Keep text too (handy for debugging / fallback)
        mime.setText(block_type)

        drag = self._create_drag(mime)
        drag.exec_(Qt.CopyAction)

    def _create_drag(self, mime: QMimeData):
        # Local import avoids unused import warnings if you lint
        from PyQt5.QtGui import QDrag

        drag = QDrag(self)
        drag.setMimeData(mime)
        return drag