from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTextEdit, QPushButton, 
                             QGroupBox, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor

class ResultsViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.current_results = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Results group
        results_group = QGroupBox("Task Results")
        results_layout = QVBoxLayout(results_group)
        
        # Results text area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText("Task results will appear here...")
        results_layout.addWidget(self.results_text)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Results")
        self.save_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; padding: 6px; }")
        self.save_btn.clicked.connect(self.save_results)
        self.save_btn.setEnabled(False)
        
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 6px; }")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setEnabled(False)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setStyleSheet("QPushButton { background-color: #9E9E9E; color: white; padding: 6px; }")
        self.clear_btn.clicked.connect(self.clear_results)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.copy_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        
        results_layout.addLayout(button_layout)
        layout.addWidget(results_group)
        
        # Screenshots group (placeholder for future implementation)
        screenshots_group = QGroupBox("Screenshots")
        screenshots_layout = QVBoxLayout(screenshots_group)
        
        self.screenshots_label = QLabel("Screenshots will be displayed here when available")
        self.screenshots_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.screenshots_label.setStyleSheet("QLabel { color: #666; font-style: italic; }")
        screenshots_layout.addWidget(self.screenshots_label)
        
        layout.addWidget(screenshots_group)
        
    def show_results(self, results):
        """Display the task results"""
        self.current_results = results
        
        # Format and display results
        if isinstance(results, str):
            formatted_results = results
        else:
            # Handle different result types
            formatted_results = str(results)
            
        self.results_text.setPlainText(formatted_results)
        
        # Enable action buttons
        self.save_btn.setEnabled(True)
        self.copy_btn.setEnabled(True)
        
        # Scroll to top
        cursor = self.results_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        self.results_text.setTextCursor(cursor)
        
    def save_results(self):
        """Save results to a file"""
        if not self.current_results:
            QMessageBox.warning(self, "No Results", "No results to save!")
            return
            
        # Open file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Results",
            "browser_agent_results.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(self.current_results))
                QMessageBox.information(self, "Success", f"Results saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save results: {str(e)}")
                
    def copy_to_clipboard(self):
        """Copy results to clipboard"""
        if not self.current_results:
            QMessageBox.warning(self, "No Results", "No results to copy!")
            return
            
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(str(self.current_results))
        QMessageBox.information(self, "Success", "Results copied to clipboard!")
        
    def clear_results(self):
        """Clear the results display"""
        self.results_text.clear()
        self.current_results = None
        self.save_btn.setEnabled(False)
        self.copy_btn.setEnabled(False)
        
    def show_screenshots(self, screenshot_paths):
        """Display screenshots (future implementation)"""
        # TODO: Implement screenshot gallery
        if screenshot_paths:
            self.screenshots_label.setText(f"Found {len(screenshot_paths)} screenshots")
        else:
            self.screenshots_label.setText("No screenshots available")
            
    def reset(self):
        """Reset the widget to initial state"""
        self.clear_results()
        self.screenshots_label.setText("Screenshots will be displayed here when available") 