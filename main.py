"""
PDF Book Converter Pro v2.0 - Main Entry Point

A Windows desktop application built with Python + PySide6, designed to convert 
scanned and digital PDF books into editable formats while preserving layout, 
formulas, diagrams, and images.

Author: Rishabh-2530
Version: 2.0
License: MIT
"""

import sys
import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from ui.main_window import MainWindow
from engine.cache_manager import CacheManager

# Configure logging
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main() -> None:
    """
    Initialize and run the PDF Book Converter Pro application.
    
    Sets up the QApplication, initializes the main window, and starts the event loop.
    """
    try:
        logger.info("Starting PDF Book Converter Pro v2.0")
        
        app = QApplication(sys.argv)
        
        # Set application metadata
        app.setApplicationName("PDF Book Converter Pro")
        app.setApplicationVersion("2.0")
        app.setApplicationDisplayName("PDF Book Converter Pro v2.0")
        
        # Initialize cache manager
        CacheManager.initialize()
        logger.info("Cache manager initialized")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        logger.info("Application window displayed")
        
        # Run application event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logger.critical(f"Fatal error during application startup: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
