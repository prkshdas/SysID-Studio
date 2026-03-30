import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from gui.main_window import MainWindow


def setup_logging():
    """Set up logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


if __name__ == "__main__":
    # Initialize logging
    logger = setup_logging()
    logger.info("Starting SysID-Studio Application")
    
    # Create application
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and configure main window
    window = MainWindow()
    window.resize(1200, 700)
    window.setWindowTitle("SysID Studio - Block-Based System Identification & Real-Time Modeling")
    
    # Show window
    logger.info("Main window created and displayed")
    window.show()
    
    # Run application
    sys.exit(app.exec_())