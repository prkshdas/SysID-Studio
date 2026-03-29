from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt


class CanvasScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 800, 600)
        
        
    def dragEnterEvent(self, event):
        event.accept()
        
    def dragMoveEvent(self, event):
        event.accept() 
        
    def dropEvent(self, event):
        pos = event.scenePos()
        
        
        # create a block
        
        block = QGraphicsRectItem(0, 0, 100, 50) 
        block.setFlag(QGraphicsRectItem.ItemIsMovable)
        block.setFlag(QGraphicsRectItem.ItemIsSelectable)
        
        block.setPos(pos)
        self.addItem(block)
        
        event.accept()   