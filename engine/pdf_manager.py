"""
PDF Manager Module

Handles PDF loading, page extraction, and PDF file operations.
"""

import logging
from pathlib import Path
from typing import Optional, List, Tuple

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


class PDFManager:
    """
    Manages PDF file operations including loading, page extraction, and metadata.
    
    Attributes:
        pdf_path (Optional[Path]): Path to the currently loaded PDF file.
        pdf_document (Optional[fitz.Document]): The PyMuPDF document object.
        total_pages (int): Total number of pages in the PDF.
    """
    
    def __init__(self) -> None:
        """
        Initialize the PDF Manager.
        """
        self.pdf_path: Optional[Path] = None
        self.pdf_document: Optional[fitz.Document] = None
        self.total_pages: int = 0
        logger.info("PDFManager initialized")
    
    def open_pdf(self, file_path: str) -> bool:
        """
        Open and load a PDF file.
        
        Args:
            file_path (str): Path to the PDF file.
        
        Returns:
            bool: True if PDF loaded successfully, False otherwise.
        """
        try:
            path = Path(file_path)
            if not path.exists():
                logger.error(f"PDF file not found: {file_path}")
                return False
            
            if path.suffix.lower() != '.pdf':
                logger.error(f"File is not a PDF: {file_path}")
                return False
            
            # Close existing PDF if open
            if self.pdf_document:
                self.close_pdf()
            
            self.pdf_document = fitz.open(str(path))
            self.pdf_path = path
            self.total_pages = len(self.pdf_document)
            
            logger.info(f"PDF opened successfully: {file_path} ({self.total_pages} pages)")
            return True
            
        except Exception as e:
            logger.error(f"Error opening PDF: {e}", exc_info=True)
            return False
    
    def close_pdf(self) -> None:
        """
        Close the currently loaded PDF file.
        """
        try:
            if self.pdf_document:
                self.pdf_document.close()
                self.pdf_document = None
                self.pdf_path = None
                self.total_pages = 0
                logger.info("PDF closed successfully")
        except Exception as e:
            logger.error(f"Error closing PDF: {e}", exc_info=True)
    
    def get_page(self, page_num: int) -> Optional[fitz.Page]:
        """
        Get a specific page from the PDF.
        
        Args:
            page_num (int): Page number (0-indexed).
        
        Returns:
            Optional[fitz.Page]: The requested page or None if invalid.
        """
        try:
            if not self.pdf_document:
                logger.warning("No PDF document loaded")
                return None
            
            if page_num < 0 or page_num >= self.total_pages:
                logger.warning(f"Page number out of range: {page_num}")
                return None
            
            return self.pdf_document[page_num]
            
        except Exception as e:
            logger.error(f"Error getting page {page_num}: {e}", exc_info=True)
            return None
    
    def get_page_image(self, page_num: int, zoom: float = 2.0) -> Optional[bytes]:
        """
        Render a page as a high-quality image.
        
        Args:
            page_num (int): Page number (0-indexed).
            zoom (float): Zoom factor for rendering quality. Default is 2.0.
        
        Returns:
            Optional[bytes]: PNG image bytes or None if failed.
        """
        try:
            page = self.get_page(page_num)
            if not page:
                return None
            
            # Create transformation matrix for zoom
            mat = fitz.Matrix(zoom, zoom)
            
            # Render page to image
            pix = page.get_pixmap(matrix=mat, alpha=False)
            return pix.tobytes(output="png")
            
        except Exception as e:
            logger.error(f"Error rendering page {page_num}: {e}", exc_info=True)
            return None
    
    def get_pdf_info(self) -> dict:
        """
        Get metadata information about the loaded PDF.
        
        Returns:
            dict: Dictionary containing PDF metadata.
        """
        if not self.pdf_document:
            logger.warning("No PDF document loaded")
            return {}
        
        try:
            metadata = self.pdf_document.metadata
            return {
                'title': metadata.get('title', 'Unknown'),
                'author': metadata.get('author', 'Unknown'),
                'subject': metadata.get('subject', 'Unknown'),
                'creator': metadata.get('creator', 'Unknown'),
                'producer': metadata.get('producer', 'Unknown'),
                'total_pages': self.total_pages,
                'file_path': str(self.pdf_path),
                'file_size': self.pdf_path.stat().st_size if self.pdf_path else 0
            }
        except Exception as e:
            logger.error(f"Error retrieving PDF info: {e}", exc_info=True)
            return {}
    
    def is_pdf_loaded(self) -> bool:
        """
        Check if a PDF is currently loaded.
        
        Returns:
            bool: True if PDF is loaded, False otherwise.
        """
        return self.pdf_document is not None and self.total_pages > 0
