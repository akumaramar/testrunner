#!/usr/bin/env python3
"""
Performance Test Script for Browser Agent Desktop Application
This script helps identify performance bottlenecks in the application.
"""

import time
import logging
import sys
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('performance_test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def test_import_performance():
    """Test import performance of key modules"""
    logger.info("=== TESTING IMPORT PERFORMANCE ===")
    
    # Test PyQt6 imports
    qt_start = time.time()
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QThread, pyqtSignal
        qt_duration = time.time() - qt_start
        logger.info(f"PyQt6 imports: {qt_duration:.3f}s")
    except Exception as e:
        logger.error(f"PyQt6 import failed: {e}")
    
    # Test browser-use imports
    browser_start = time.time()
    try:
        from browser_use import Agent
        from browser_use.llm import ChatOpenAI
        browser_duration = time.time() - browser_start
        logger.info(f"browser-use imports: {browser_duration:.3f}s")
    except Exception as e:
        logger.error(f"browser-use import failed: {e}")
    
    # Test dotenv
    dotenv_start = time.time()
    try:
        from dotenv import load_dotenv
        dotenv_duration = time.time() - dotenv_start
        logger.info(f"dotenv import: {dotenv_duration:.3f}s")
    except Exception as e:
        logger.error(f"dotenv import failed: {e}")

def test_ui_creation_performance():
    """Test UI creation performance"""
    logger.info("=== TESTING UI CREATION PERFORMANCE ===")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.main_window import MainWindow
        
        # Create QApplication
        app_start = time.time()
        app = QApplication(sys.argv)
        app_duration = time.time() - app_start
        logger.info(f"QApplication creation: {app_duration:.3f}s")
        
        # Create MainWindow
        window_start = time.time()
        window = MainWindow()
        window_duration = time.time() - window_start
        logger.info(f"MainWindow creation: {window_duration:.3f}s")
        
        # Show window
        show_start = time.time()
        window.show()
        show_duration = time.time() - show_start
        logger.info(f"Window show: {show_duration:.3f}s")
        
        # Close window
        close_start = time.time()
        window.close()
        close_duration = time.time() - close_start
        logger.info(f"Window close: {close_duration:.3f}s")
        
    except Exception as e:
        logger.error(f"UI creation test failed: {e}")

def test_agent_creation_performance():
    """Test agent creation performance"""
    logger.info("=== TESTING AGENT CREATION PERFORMANCE ===")
    
    try:
        from dotenv import load_dotenv
        from browser_use.llm import ChatOpenAI
        from browser_use import Agent
        
        # Load environment
        env_start = time.time()
        load_dotenv()
        env_duration = time.time() - env_start
        logger.info(f"Environment loading: {env_duration:.3f}s")
        
        # Create ChatOpenAI
        llm_start = time.time()
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        llm_duration = time.time() - llm_start
        logger.info(f"ChatOpenAI creation: {llm_duration:.3f}s")
        
        # Create Agent
        agent_start = time.time()
        agent = Agent(
            llm=llm,
            verbose=False,
            task="test task"
        )
        agent_duration = time.time() - agent_start
        logger.info(f"Agent creation: {agent_duration:.3f}s")
        
    except Exception as e:
        logger.error(f"Agent creation test failed: {e}")

def test_system_info():
    """Display system information"""
    logger.info("=== SYSTEM INFORMATION ===")
    
    import platform
    import psutil
    
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"CPU cores: {psutil.cpu_count()}")
    logger.info(f"Memory: {psutil.virtual_memory().total / (1024**3):.1f} GB")
    logger.info(f"Available memory: {psutil.virtual_memory().available / (1024**3):.1f} GB")

def main():
    """Run all performance tests"""
    logger.info("Starting performance tests...")
    
    # Test system info
    test_system_info()
    
    # Test imports
    test_import_performance()
    
    # Test UI creation
    test_ui_creation_performance()
    
    # Test agent creation
    test_agent_creation_performance()
    
    logger.info("Performance tests completed. Check performance_test.log for detailed results.")

if __name__ == "__main__":
    main() 