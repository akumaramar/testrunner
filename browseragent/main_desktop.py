import sys
import asyncio
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal
from ui.main_window import MainWindow
from logging_config import setup_logging

class AsyncThread(QThread):
    finished = pyqtSignal()
    
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_forever()

def main():
    # Setup logging
    log_file = setup_logging(log_level=logging.INFO)
    print(f"Logging to: {log_file}")
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Browser Agent")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("BrowserAgent")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 