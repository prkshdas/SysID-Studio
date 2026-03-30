from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QMessageBox, QStatusBar, QToolBar
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QColor
from .canvas.canvas_view import CanvasView
from .library.library_panel import LibraryPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize UI
        self._init_ui()
        self._setup_toolbar()
        self._setup_status_bar()
        self._connect_signals()
        
    def _init_ui(self):
        """Initialize the main user interface"""
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Create left panel (Library)
        left_panel = self._create_left_panel()
        
        # Create center panel (Canvas with controls)
        center_panel = self._create_center_panel()
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(center_panel, 1)  # Canvas takes remaining space
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Set central widget
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Store references
        self.canvas = self.canvas_view
        self.library = self.library_panel
        
    def _create_left_panel(self):
        """Create the left library panel"""
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("Block Library")
        title.setStyleSheet("font-weight: bold; font-size: 12px; padding: 5px;")
        left_layout.addWidget(title)
        
        # Library panel
        self.library_panel = LibraryPanel()
        self.library_panel.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
            QListWidget::item:selected {
                background-color: #0d47a1;
                color: white;
            }
        """)
        left_layout.addWidget(self.library_panel)
        
        # Instructions
        instructions = QLabel(
            "Drag blocks to canvas\nConnect input→output\nPress Delete to remove\nScroll to zoom"
        )
        instructions.setStyleSheet("font-size: 9px; color: #aaa; padding: 5px;")
        left_layout.addWidget(instructions)
        
        left_panel.setLayout(left_layout)
        left_panel.setFixedWidth(220)
        left_panel.setStyleSheet("background-color: #1e1e1e; border-right: 1px solid #444;")
        
        return left_panel
    
    def _create_center_panel(self):
        """Create the center canvas panel"""
        center_panel = QWidget()
        center_layout = QVBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        
        # Canvas view
        self.canvas_view = CanvasView()
        center_layout.addWidget(self.canvas_view)
        
        center_panel.setLayout(center_layout)
        return center_panel
    
    def _setup_toolbar(self):
        """Set up the toolbar with control buttons"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #2b2b2b;
                border-bottom: 1px solid #444;
                spacing: 5px;
                padding: 5px;
            }
            QToolButton {
                background-color: #3d3d3d;
                color: white;
                border: 1px solid #555;
                padding: 4px;
                border-radius: 3px;
                font-size: 10px;
            }
            QToolButton:hover {
                background-color: #4d4d4d;
            }
            QToolButton:pressed {
                background-color: #2d2d2d;
            }
        """)
        
        # Add buttons to toolbar
        self.clear_btn = toolbar.addAction("Clear Canvas")
        self.clear_btn.triggered.connect(self._clear_canvas)
        
        toolbar.addSeparator()
        
        self.zoom_in_btn = toolbar.addAction("Zoom In")
        self.zoom_in_btn.triggered.connect(self._zoom_in)
        
        self.zoom_out_btn = toolbar.addAction("Zoom Out")
        self.zoom_out_btn.triggered.connect(self._zoom_out)
        
        self.fit_view_btn = toolbar.addAction("Fit to View")
        self.fit_view_btn.triggered.connect(self._fit_to_view)
        
        toolbar.addSeparator()
        
        self.info_btn = toolbar.addAction("Show Info")
        self.info_btn.triggered.connect(self._show_info)
        
        self.addToolBar(toolbar)
    
    def _setup_status_bar(self):
        """Set up the status bar"""
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #aaa; padding: 5px;")
        self.statusBar().addWidget(self.status_label)
        
        # Connection info label
        self.connection_label = QLabel("Connections: 0 | Blocks: 0")
        self.connection_label.setStyleSheet("color: #aaa; padding: 5px;")
        self.statusBar().addPermanentWidget(self.connection_label)
    
    def _connect_signals(self):
        """Connect custom signals"""
        # Update status bar when canvas changes
        self.canvas_view.scene.itemAdded.connect(self._update_canvas_info)
        self.canvas_view.scene.itemRemoved.connect(self._update_canvas_info)
    
    def _update_canvas_info(self):
        """Update canvas information in status bar"""
        scene = self.canvas_view.scene
        
        # Count blocks and connections
        blocks = [item for item in scene.items() if hasattr(item, 'get_all_ports')]
        connections = len(scene.connections)
        
        self.connection_label.setText(f"Connections: {connections} | Blocks: {len(blocks)}")
        self.status_label.setText(f"Canvas updated")
    
    def _clear_canvas(self):
        """Clear all items from canvas"""
        reply = QMessageBox.question(
            self, 
            "Clear Canvas", 
            "Are you sure you want to clear the entire canvas?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.canvas_view.scene.clear_scene()
            self.status_label.setText("Canvas cleared")
            self._update_canvas_info()
    
    def _zoom_in(self):
        """Zoom in the canvas"""
        self.canvas_view.scale(1.1, 1.1)
        self.status_label.setText("Zoomed in")
    
    def _zoom_out(self):
        """Zoom out the canvas"""
        self.canvas_view.scale(0.9, 0.9)
        self.status_label.setText("Zoomed out")
    
    def _fit_to_view(self):
        """Fit all items to view"""
        rect = self.canvas_view.scene.itemsBoundingRect()
        if rect.isValid():
            self.canvas_view.fitInView(rect, Qt.KeepAspectRatio)
            self.canvas_view.scale(0.95, 0.95)  # Add 5% padding
            self.status_label.setText("Fitted to view")
    
    def _show_info(self):
        """Show information about the current canvas"""
        scene = self.canvas_view.scene
        blocks = [item for item in scene.items() if hasattr(item, 'get_all_ports')]
        connections = scene.connections
        
        info_text = f"""
SysID Studio - Canvas Information

Blocks: {len(blocks)}
Connections: {len(connections)}

Block Types:
"""
        
        block_types = {}
        for block in blocks:
            block_type = block.block_type
            block_types[block_type] = block_types.get(block_type, 0) + 1
        
        for block_type, count in sorted(block_types.items()):
            info_text += f"  • {block_type}: {count}\n"
        
        info_text += f"\nShortcuts:\n"
        info_text += f"  • Delete Key: Remove selected items\n"
        info_text += f"  • Mouse Wheel: Zoom in/out\n"
        info_text += f"  • Drag: Move blocks or select multiple\n"
        info_text += f"  • Click Output→Input: Create connection\n"
        
        QMessageBox.information(self, "Canvas Information", info_text)