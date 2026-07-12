"""
Cache Manager Module

Handles caching of rendered pages and temporary files to improve performance.
"""

import logging
import shutil
from pathlib import Path
from typing import Optional, Dict
from functools import lru_cache

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Manages application cache for rendered pages and temporary files.
    
    Attributes:
        cache_dir (Path): Directory for cache storage.
        max_cache_size (int): Maximum number of pages to cache in memory.
    """
    
    cache_dir = Path("temp/cache")
    max_cache_size: int = 50  # Number of pages to cache
    _instance: Optional['CacheManager'] = None
    
    def __init__(self) -> None:
        """
        Initialize the Cache Manager.
        """
        self.page_cache: Dict[int, bytes] = {}
        logger.info("CacheManager initialized")
    
    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the cache directory and singleton instance.
        """
        cls.cache_dir.mkdir(parents=True, exist_ok=True)
        cls._instance = cls()
        logger.info(f"Cache directory initialized at {cls.cache_dir}")
    
    @classmethod
    def get_instance(cls) -> 'CacheManager':
        """
        Get the singleton instance of CacheManager.
        
        Returns:
            CacheManager: The singleton instance.
        """
        if cls._instance is None:
            cls.initialize()
        return cls._instance
    
    def cache_page(self, page_num: int, image_bytes: bytes) -> bool:
        """
        Cache a rendered page image.
        
        Args:
            page_num (int): Page number (0-indexed).
            image_bytes (bytes): Rendered page image bytes.
        
        Returns:
            bool: True if cached successfully, False otherwise.
        """
        try:
            # If cache is full, remove oldest entry
            if len(self.page_cache) >= self.max_cache_size:
                oldest_key = next(iter(self.page_cache))
                del self.page_cache[oldest_key]
                logger.debug(f"Removed page {oldest_key} from cache")
            
            self.page_cache[page_num] = image_bytes
            logger.debug(f"Cached page {page_num}")
            return True
            
        except Exception as e:
            logger.error(f"Error caching page {page_num}: {e}", exc_info=True)
            return False
    
    def get_cached_page(self, page_num: int) -> Optional[bytes]:
        """
        Retrieve a cached page image.
        
        Args:
            page_num (int): Page number (0-indexed).
        
        Returns:
            Optional[bytes]: Cached image bytes or None if not found.
        """
        return self.page_cache.get(page_num)
    
    def clear_cache(self) -> None:
        """
        Clear all cached pages.
        """
        self.page_cache.clear()
        logger.info("Page cache cleared")
    
    def clear_temp_directory(self) -> bool:
        """
        Clear all temporary files.
        
        Returns:
            bool: True if cleared successfully, False otherwise.
        """
        try:
            temp_dir = Path("temp")
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
                temp_dir.mkdir(exist_ok=True)
                logger.info("Temporary directory cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing temp directory: {e}", exc_info=True)
            return False
    
    def get_cache_info(self) -> dict:
        """
        Get information about the current cache state.
        
        Returns:
            dict: Cache statistics.
        """
        return {
            'cached_pages': len(self.page_cache),
            'max_cache_size': self.max_cache_size,
            'cache_directory': str(self.cache_dir),
            'cache_full': len(self.page_cache) >= self.max_cache_size
        }
