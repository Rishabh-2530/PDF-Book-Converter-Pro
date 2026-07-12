"""
Preview Widget Module

Contains the scrollable, zoomable PDF page preview widget.
"""

import logging
from typing import Optional

from PySide6.QtWidgets import QScrollArea, QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, Signal, QSize, QEvent

logger = logging.getLogger(__name__)


class PreviewWidget(QScrollArea):
    """
    Scrollable preview widget for displaying PDF pages.
    
    Features:
        - Smooth scrolling
        - Mouse wheel zoom support
        - High-quality image rendering
        - Lazy loading with caching
    
    Signals:
        mouse_wheel_zoom: Emitted when mouse wheel is used for zooming.
    """
    
    mouse_wheel_zoom = Signal(int)  # Delta value
    
    def __init__(self) -> None:
        """
        Initialize the Preview Widget.
        """
        super().__init__()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #f0f0f0;")
        
        self.setWidget(self.image_label)
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea { background-color: #e0e0e0; }")
        
        # Enable mouse tracking for smooth interactions
        self.setMouseTracking(True)
        
        logger.info("PreviewWidget initialized")
    
    def set_image(self, image_bytes: bytes, zoom_level: float = 100.0) -> bool:
        """
        Set the image to display.
        
        Args:
            image_bytes (bytes): PNG/JPEG image bytes.
            zoom_level (float): Zoom level as percentage.
        
        Returns:
            bool: True if image was set successfully, False otherwise.
        """
        try:
            qimage = QImage()
            if not qimage.loadFromData(image_bytes):
                logger.error("Failed to load image data")
                return False
            
            # Apply zoom scaling
            scale_factor = zoom_level / 100.0
            scaled_size = QSize(
                int(qimage.width() * scale_factor),
                int(qimage.height() * scale_factor)
            )
            
            scaled_image = qimage.scaled(
                scaled_size,
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            )
            
            pixmap = QPixmap.fromImage(scaled_image)
            self.image_label.setPixmap(pixmap)
            
            logger.debug(f"Image set with zoom level {zoom_level}%")
            return True
            
        except Exception as e:
            logger.error(f"Error setting image: {e}", exc_info=True)
            return False
    
    def wheelEvent(self, event) -> None:
        """
        Handle mouse wheel events for zooming.
        
        Args:
            event: The wheel event.
        """
        if event.modifiers() == Qt.ControlModifier:
            # Ctrl + Mouse wheel for zoom
            delta = event.angleDelta().y()
            self.mouse_wheel_zoom.emit(delta)
            event.accept()
        else:
            # Normal scrolling
            super().wheelEvent(event)
    
    def clear(self) -> None:
        """
        Clear the preview widget.
        """
        self.image_label.clear()
        logger.debug("Preview widget cleared")
