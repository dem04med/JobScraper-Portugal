"""
JobScraper-Portugal Core Module

Este módulo contém as classes e funções principais do JobScraper.
"""

from .scraper import JobScraper
from .parser import JobParser
from .utils import save_to_csv

__all__ = ['JobScraper', 'JobParser', 'save_to_csv']
__version__ = '1.0.0'