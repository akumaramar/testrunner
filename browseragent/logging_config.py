"""
Logging configuration for Browser Agent Desktop Application
"""

import logging
import os
from datetime import datetime

def setup_logging(log_level=logging.INFO, log_file=None):
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (default: INFO)
        log_file: Optional log file path (default: auto-generated)
    """
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Generate log filename if not provided
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/browser_agent_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Console output
        ]
    )
    
    # Set specific logger levels
    logging.getLogger('PyQt6').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    # Suppress browser-use authentication and verbose logs
    logging.getLogger('browser_use.sync.auth').setLevel(logging.ERROR)
    logging.getLogger('browser_use.auth').setLevel(logging.ERROR)
    logging.getLogger('browser_use.sync').setLevel(logging.ERROR)
    logging.getLogger('browser_use.agent').setLevel(logging.WARNING)
    logging.getLogger('browser_use.evaluation').setLevel(logging.WARNING)
    logging.getLogger('browser_use.detection').setLevel(logging.WARNING)
    
    # Suppress other verbose logs
    logging.getLogger('httpx').setLevel(logging.ERROR)
    logging.getLogger('asyncio').setLevel(logging.ERROR)
    
    return log_file

def get_performance_logger():
    """Get a logger specifically for performance monitoring"""
    logger = logging.getLogger('performance')
    logger.setLevel(logging.INFO)
    
    # Add file handler for performance logs
    if not logger.handlers:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        perf_log_file = f"logs/performance_{timestamp}.log"
        
        handler = logging.FileHandler(perf_log_file, encoding='utf-8')
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    return logger 