"""
Status Bar Module

Contains the status bar displaying page info, zoom level, and file size.
"""

import logging
from PySide6.QtWidgets import QStatusBar, QLabel
from PySide6.QtCore import Qt

logger = logging.getLogger(__name__)


class StatusBar(QStatusBar):
    """
    Custom status bar for displaying application status information.
    
    Displays:
        - Current page and total pages
        - Zoom level
        - File size
        - General status messages
    """
    
    def __init__(self) -> None:
        """
        Initialize the Status Bar.
        """
        super().__init__()
        
        # Page info label
        self.page_label = QLabel("Ready")
        self.page_label.setStyleSheet("margin: 0 10px;")
        self.addWidget(self.page_label, 1)
        
        # Zoom level label
        self.zoom_label = QLabel("Zoom: 100%")
        self.zoom_label.setStyleSheet("margin: 0 10px;")
        self.addPermanentWidget(self.zoom_label)
        
        # File size label
        self.size_label = QLabel("Size: -")
        self.size_label.setStyleSheet("margin: 0 10px;")
        self.addPermanentWidget(self.size_label)
        
        logger.info("StatusBar initialized")
    
    def set_page_info(self, current_page: int, total_pages: int) -> None:
        """
        Set page information.
        
        Args:
            current_page (int): Current page number (1-indexed).
            total_pages (int): Total number of pages.
        """
        self.page_label.setText(f"Page: {current_page} / {total_pages}")
    
    def set_zoom_level(self, zoom_level: float) -> None:
        """
        Set zoom level display.
        
        Args:
            zoom_level (float): Current zoom level as percentage.
        """
        self.zoom_label.setText(f"Zoom: {zoom_level:.0f}%")
    
    def set_file_size(self, size_bytes: int) -> None:
        """
        Set file size display.
        
        Args:
            size_bytes (int): File size in bytes.
        """
        if size_bytes == 0:
            self.size_label.setText("Size: -")
        else:
            # Convert bytes to human-readable format
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024:
                    self.size_label.setText(f"Size: {size_bytes:.2f} {unit}")
                    break
                size_bytes /= 1024
    
    def set_status(self, message: str) -> None:
        """
        Set general status message.
        
        Args:
            message (str): Status message to display.
        """
        self.showMessage(message, 5000)  # Display for 5 seconds
        logger.info(f"Status: {message}")
