"""
Zoom Manager Module

Handles zoom operations including zoom in/out, fit to width, and fit to page.
"""

import logging
from enum import Enum
from typing import Tuple

logger = logging.getLogger(__name__)


class ZoomMode(Enum):
    """
    Enumeration of zoom modes.
    """
    CUSTOM = "custom"
    FIT_WIDTH = "fit_width"
    FIT_PAGE = "fit_page"


class ZoomManager:
    """
    Manages zoom levels and zoom modes for PDF viewing.
    
    Attributes:
        current_zoom (float): Current zoom level as a percentage (25-500).
        zoom_mode (ZoomMode): Current zoom mode.
        min_zoom (float): Minimum zoom level.
        max_zoom (float): Maximum zoom level.
    """
    
    MIN_ZOOM = 25.0
    MAX_ZOOM = 500.0
    DEFAULT_ZOOM = 100.0
    ZOOM_STEP = 10.0  # Zoom in/out by 10%
    
    def __init__(self) -> None:
        """
        Initialize the Zoom Manager with default zoom level.
        """
        self.current_zoom: float = self.DEFAULT_ZOOM
        self.zoom_mode: ZoomMode = ZoomMode.CUSTOM
        logger.info(f"ZoomManager initialized with default zoom: {self.DEFAULT_ZOOM}%")
    
    def zoom_in(self) -> float:
        """
        Increase zoom level by the zoom step.
        
        Returns:
            float: New zoom level.
        """
        new_zoom = min(self.current_zoom + self.ZOOM_STEP, self.MAX_ZOOM)
        self.set_zoom(new_zoom)
        logger.debug(f"Zoomed in to {new_zoom}%")
        return self.current_zoom
    
    def zoom_out(self) -> float:
        """
        Decrease zoom level by the zoom step.
        
        Returns:
            float: New zoom level.
        """
        new_zoom = max(self.current_zoom - self.ZOOM_STEP, self.MIN_ZOOM)
        self.set_zoom(new_zoom)
        logger.debug(f"Zoomed out to {new_zoom}%")
        return self.current_zoom
    
    def set_zoom(self, zoom_level: float) -> bool:
        """
        Set zoom to a specific level.
        
        Args:
            zoom_level (float): Desired zoom level (25-500).
        
        Returns:
            bool: True if zoom was set successfully, False otherwise.
        """
        if zoom_level < self.MIN_ZOOM or zoom_level > self.MAX_ZOOM:
            logger.warning(f"Zoom level out of range: {zoom_level}%")
            return False
        
        self.current_zoom = zoom_level
        self.zoom_mode = ZoomMode.CUSTOM
        logger.debug(f"Zoom set to {zoom_level}%")
        return True
    
    def fit_width(self, page_width: float, view_width: float) -> float:
        """
        Calculate zoom level to fit page width to view width.
        
        Args:
            page_width (float): Width of the PDF page.
            view_width (float): Width of the view area.
        
        Returns:
            float: Calculated zoom level.
        """
        if view_width <= 0 or page_width <= 0:
            logger.warning("Invalid dimensions for fit_width calculation")
            return self.current_zoom
        
        zoom_level = (view_width / page_width) * 100
        zoom_level = max(self.MIN_ZOOM, min(zoom_level, self.MAX_ZOOM))
        self.current_zoom = zoom_level
        self.zoom_mode = ZoomMode.FIT_WIDTH
        logger.debug(f"Fit width zoom set to {zoom_level}%")
        return self.current_zoom
    
    def fit_page(self, page_width: float, page_height: float, 
                 view_width: float, view_height: float) -> float:
        """
        Calculate zoom level to fit entire page in view.
        
        Args:
            page_width (float): Width of the PDF page.
            page_height (float): Height of the PDF page.
            view_width (float): Width of the view area.
            view_height (float): Height of the view area.
        
        Returns:
            float: Calculated zoom level.
        """
        if any(dim <= 0 for dim in [page_width, page_height, view_width, view_height]):
            logger.warning("Invalid dimensions for fit_page calculation")
            return self.current_zoom
        
        width_zoom = (view_width / page_width) * 100
        height_zoom = (view_height / page_height) * 100
        zoom_level = min(width_zoom, height_zoom)
        zoom_level = max(self.MIN_ZOOM, min(zoom_level, self.MAX_ZOOM))
        self.current_zoom = zoom_level
        self.zoom_mode = ZoomMode.FIT_PAGE
        logger.debug(f"Fit page zoom set to {zoom_level}%")
        return self.current_zoom
    
    def get_zoom(self) -> float:
        """
        Get the current zoom level.
        
        Returns:
            float: Current zoom level as percentage.
        """
        return self.current_zoom
    
    def get_zoom_mode(self) -> ZoomMode:
        """
        Get the current zoom mode.
        
        Returns:
            ZoomMode: Current zoom mode.
        """
        return self.zoom_mode
    
    def reset_zoom(self) -> float:
        """
        Reset zoom to default level.
        
        Returns:
            float: Default zoom level.
        """
        self.current_zoom = self.DEFAULT_ZOOM
        self.zoom_mode = ZoomMode.CUSTOM
        logger.debug("Zoom reset to default")
        return self.current_zoom
