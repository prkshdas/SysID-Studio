from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem
from gui.blocks.block_item import BlockItem
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
          
        block_type = event.mimeData().text()
        
        block = BlockItem(block_type)
        block.setPos(pos)
        
        self.addItem(block)
        
        event.accept()   