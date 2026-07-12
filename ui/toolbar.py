"""
Toolbar Module

Contains the main toolbar with file and view control buttons.
"""

import logging
from typing import Optional

from PySide6.QtWidgets import QToolBar, QComboBox, QSpinBox, QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction, QIcon

logger = logging.getLogger(__name__)


class ToolBar(QToolBar):
    """
    Main toolbar with file operations and view controls.
    
    Signals:
        open_pdf_clicked: Emitted when Open PDF button is clicked.
        previous_clicked: Emitted when Previous button is clicked.
        next_clicked: Emitted when Next button is clicked.
        first_clicked: Emitted when First Page button is clicked.
        last_clicked: Emitted when Last Page button is clicked.
        zoom_in_clicked: Emitted when Zoom In button is clicked.
        zoom_out_clicked: Emitted when Zoom Out button is clicked.
        fit_width_clicked: Emitted when Fit Width button is clicked.
        fit_page_clicked: Emitted when Fit Page button is clicked.
    """
    
    open_pdf_clicked = Signal()
    previous_clicked = Signal()
    next_clicked = Signal()
    first_clicked = Signal()
    last_clicked = Signal()
    zoom_in_clicked = Signal()
    zoom_out_clicked = Signal()
    fit_width_clicked = Signal()
    fit_page_clicked = Signal()
    
    def __init__(self) -> None:
        """
        Initialize the Toolbar.
        """
        super().__init__("Main Toolbar")
        self.setMovable(False)
        
        self._setup_file_operations()
        self.addSeparator()
        self._setup_navigation()
        self.addSeparator()
        self._setup_zoom_controls()
        
        logger.info("Toolbar initialized")
    
    def _setup_file_operations(self) -> None:
        """
        Set up file operation buttons (Open, Save, Export).
        """
        open_action = self.addAction("📁 Open")
        open_action.triggered.connect(self.open_pdf_clicked.emit)
        
        save_action = self.addAction("💾 Save")
        save_action.triggered.connect(lambda: logger.info("Save clicked"))
        
        export_action = self.addAction("📤 Export")
        export_action.triggered.connect(lambda: logger.info("Export clicked"))
        
        logger.info("File operation buttons added")
    
    def _setup_navigation(self) -> None:
        """
        Set up navigation buttons (Previous, Next, First, Last).
        """
        first_action = self.addAction("⏮ First")
        first_action.triggered.connect(self.first_clicked.emit)
        
        prev_action = self.addAction("◀ Prev")
        prev_action.triggered.connect(self.previous_clicked.emit)
        
        # Page counter
        self.addSeparator()
        self.page_label = QLabel("Page: 0 / 0")
        self.addWidget(self.page_label)
        self.addSeparator()
        
        next_action = self.addAction("Next ▶")
        next_action.triggered.connect(self.next_clicked.emit)
        
        last_action = self.addAction("Last ⏭")
        last_action.triggered.connect(self.last_clicked.emit)
        
        logger.info("Navigation buttons added")
    
    def _setup_zoom_controls(self) -> None:
        """
        Set up zoom control buttons and dropdowns.
        """
        fit_width_action = self.addAction("Fit Width")
        fit_width_action.triggered.connect(self.fit_width_clicked.emit)
        
        fit_page_action = self.addAction("Fit Page")
        fit_page_action.triggered.connect(self.fit_page_clicked.emit)
        
        zoom_out_action = self.addAction("🔍−")
        zoom_out_action.triggered.connect(self.zoom_out_clicked.emit)
        
        # Zoom level display
        self.zoom_label = QLabel("100%")
        self.addWidget(self.zoom_label)
        
        zoom_in_action = self.addAction("🔍+")
        zoom_in_action.triggered.connect(self.zoom_in_clicked.emit)
        
        logger.info("Zoom control buttons added")
    
    def update_total_pages(self, total_pages: int) -> None:
        """
        Update the page counter display.
        
        Args:
            total_pages (int): Total number of pages.
        """
        self.page_label.setText(f"Page: 0 / {total_pages}")
    
    def update_page_display(self, current_page: int, total_pages: int) -> None:
        """
        Update the page display.
        
        Args:
            current_page (int): Current page number (1-indexed for display).
            total_pages (int): Total number of pages.
        """
        self.page_label.setText(f"Page: {current_page} / {total_pages}")
    
    def update_zoom_display(self, zoom_level: float) -> None:
        """
        Update the zoom level display.
        
        Args:
            zoom_level (float): Current zoom level as percentage.
        """
        self.zoom_label.setText(f"{zoom_level:.0f}%")
