from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag


class LibraryPanel(QListWidget):
    def __init__(self):
        super().__init__()
        
        self.addItem("Gain Block")
        self.addItem("Constant Block")
        self.addItem("Scope")
        
        
        # enable drag
        self.setDragEnabled(True)
        
    def startDrag(self, supportedActions):
        item = self.currentItem()
        
        if not item:
            return
        
        drag = QDrag(self)
        mime = QMimeData()
        
        mime.setText(item.text())
        drag.setMimeData(mime)
        
        drag.exec_(Qt.CopyAction)