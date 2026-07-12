"""
Main Window Module

Contains the primary application window with Adobe Acrobat-style interface.
"""

import logging
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QSplitter, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QKeySequence, QAction

from engine.pdf_manager import PDFManager
from engine.zoom_manager import ZoomManager
from engine.cache_manager import CacheManager
from ui.toolbar import ToolBar
from ui.statusbar import StatusBar
from ui.preview_widget import PreviewWidget

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window for PDF Book Converter Pro.
    
    Features:
        - PDF viewer with navigation
        - Zoom controls (fit width, fit page, custom zoom)
        - Toolbar with file operations
        - Status bar with page and zoom information
        - Scrollable preview with mouse wheel zoom
    """
    
    # Signals
    pdf_loaded = Signal(str)  # Emits PDF path when loaded
    page_changed = Signal(int)  # Emits current page number
    zoom_changed = Signal(float)  # Emits zoom level
    
    def __init__(self) -> None:
        """
        Initialize the Main Window.
        """
        super().__init__()
        self.pdf_manager = PDFManager()
        self.zoom_manager = ZoomManager()
        self.cache_manager = CacheManager.get_instance()
        
        self.current_page: int = 0
        
        self._setup_ui()
        self._setup_connections()
        self._setup_keyboard_shortcuts()
        
        logger.info("MainWindow initialized")
    
    def _setup_ui(self) -> None:
        """
        Set up the user interface components.
        """
        self.setWindowTitle("PDF Book Converter Pro v2.0")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create toolbar
        self.toolbar = ToolBar()
        self.addToolBar(self.toolbar)
        
        # Create preview widget (scrollable PDF view)
        self.preview_widget = PreviewWidget()
        main_layout.addWidget(self.preview_widget, 1)
        
        # Create status bar
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)
        
        logger.info("UI components created")
    
    def _setup_connections(self) -> None:
        """
        Set up signal-slot connections.
        """
        # Toolbar connections
        self.toolbar.open_pdf_clicked.connect(self.open_pdf)
        self.toolbar.previous_clicked.connect(self.previous_page)
        self.toolbar.next_clicked.connect(self.next_page)
        self.toolbar.first_clicked.connect(self.first_page)
        self.toolbar.last_clicked.connect(self.last_page)
        self.toolbar.zoom_in_clicked.connect(self.zoom_in)
        self.toolbar.zoom_out_clicked.connect(self.zoom_out)
        self.toolbar.fit_width_clicked.connect(self.fit_width)
        self.toolbar.fit_page_clicked.connect(self.fit_page)
        
        # Preview widget connections
        self.preview_widget.mouse_wheel_zoom.connect(self.on_mouse_wheel_zoom)
        
        logger.info("Signal connections established")
    
    def _setup_keyboard_shortcuts(self) -> None:
        """
        Set up keyboard shortcuts.
        """
        shortcuts = [
            ("Ctrl+O", self.open_pdf, "Open PDF"),
            ("Ctrl+S", self.save_pdf, "Save PDF"),
            ("Ctrl++", self.zoom_in, "Zoom In"),
            ("Ctrl+-", self.zoom_out, "Zoom Out"),
            ("Left", self.previous_page, "Previous Page"),
            ("Right", self.next_page, "Next Page"),
            ("Home", self.first_page, "First Page"),
            ("End", self.last_page, "Last Page"),
        ]
        
        for shortcut, slot, description in shortcuts:
            action = QAction(description, self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(slot)
            self.addAction(action)
        
        logger.info(f"Added {len(shortcuts)} keyboard shortcuts")
    
    def open_pdf(self) -> None:
        """
        Open a PDF file dialog and load the selected PDF.
        """
        from PySide6.QtWidgets import QFileDialog
        
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            if self.pdf_manager.open_pdf(file_path):
                self.cache_manager.clear_cache()
                self.current_page = 0
                self.pdf_loaded.emit(file_path)
                self.update_preview()
                self.toolbar.update_total_pages(self.pdf_manager.total_pages)
                logger.info(f"PDF loaded: {file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to open PDF file.")
    
    def save_pdf(self) -> None:
        """
        Save current PDF (placeholder for future functionality).
        """
        logger.info("Save PDF called")
        QMessageBox.information(self, "Info", "Save functionality coming soon.")
    
    def next_page(self) -> None:
        """
        Navigate to the next page.
        """
        if self.pdf_manager.is_pdf_loaded():
            if self.current_page < self.pdf_manager.total_pages - 1:
                self.current_page += 1
                self.update_preview()
                self.page_changed.emit(self.current_page)
    
    def previous_page(self) -> None:
        """
        Navigate to the previous page.
        """
        if self.pdf_manager.is_pdf_loaded():
            if self.current_page > 0:
                self.current_page -= 1
                self.update_preview()
                self.page_changed.emit(self.current_page)
    
    def first_page(self) -> None:
        """
        Navigate to the first page.
        """
        if self.pdf_manager.is_pdf_loaded():
            self.current_page = 0
            self.update_preview()
            self.page_changed.emit(self.current_page)
    
    def last_page(self) -> None:
        """
        Navigate to the last page.
        """
        if self.pdf_manager.is_pdf_loaded():
            self.current_page = self.pdf_manager.total_pages - 1
            self.update_preview()
            self.page_changed.emit(self.current_page)
    
    def zoom_in(self) -> None:
        """
        Increase zoom level.
        """
        self.zoom_manager.zoom_in()
        self.update_preview()
        self.zoom_changed.emit(self.zoom_manager.get_zoom())
    
    def zoom_out(self) -> None:
        """
        Decrease zoom level.
        """
        self.zoom_manager.zoom_out()
        self.update_preview()
        self.zoom_changed.emit(self.zoom_manager.get_zoom())
    
    def fit_width(self) -> None:
        """
        Fit page width to window width.
        """
        if self.pdf_manager.is_pdf_loaded():
            page = self.pdf_manager.get_page(self.current_page)
            if page:
                page_width = page.rect.width
                view_width = self.preview_widget.width()
                self.zoom_manager.fit_width(page_width, view_width)
                self.update_preview()
                self.zoom_changed.emit(self.zoom_manager.get_zoom())
    
    def fit_page(self) -> None:
        """
        Fit entire page to window.
        """
        if self.pdf_manager.is_pdf_loaded():
            page = self.pdf_manager.get_page(self.current_page)
            if page:
                page_width = page.rect.width
                page_height = page.rect.height
                view_width = self.preview_widget.width()
                view_height = self.preview_widget.height()
                self.zoom_manager.fit_page(page_width, page_height, view_width, view_height)
                self.update_preview()
                self.zoom_changed.emit(self.zoom_manager.get_zoom())
    
    def on_mouse_wheel_zoom(self, delta: int) -> None:
        """
        Handle mouse wheel zoom.
        
        Args:
            delta (int): Mouse wheel delta (positive = zoom in, negative = zoom out).
        """
        if delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
    
    def update_preview(self) -> None:
        """
        Update the preview widget with the current page.
        """
        if not self.pdf_manager.is_pdf_loaded():
            return
        
        # Check cache first
        cached_image = self.cache_manager.get_cached_page(self.current_page)
        if cached_image:
            self.preview_widget.set_image(cached_image, self.zoom_manager.get_zoom())
            logger.debug(f"Displayed cached page {self.current_page}")
        else:
            # Render page
            zoom_factor = self.zoom_manager.get_zoom() / 100.0
            image_bytes = self.pdf_manager.get_page_image(self.current_page, zoom=zoom_factor)
            if image_bytes:
                self.cache_manager.cache_page(self.current_page, image_bytes)
                self.preview_widget.set_image(image_bytes, self.zoom_manager.get_zoom())
                logger.debug(f"Rendered and displayed page {self.current_page}")
        
        # Update status bar
        self.status_bar.set_page_info(self.current_page + 1, self.pdf_manager.total_pages)
        self.status_bar.set_zoom_level(self.zoom_manager.get_zoom())
    
    def closeEvent(self, event) -> None:
        """
        Handle application close event.
        """
        self.pdf_manager.close_pdf()
        self.cache_manager.clear_temp_directory()
        logger.info("Application closed")
        event.accept()
