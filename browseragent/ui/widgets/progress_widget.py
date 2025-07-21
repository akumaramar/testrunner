from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QProgressBar, QTextEdit, 
                             QPushButton, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QTextCursor, QColor, QPalette

class ProgressWidget(QWidget):
    stop_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Status group
        status_group = QGroupBox("Task Status")
        status_layout = QVBoxLayout(status_group)
        
        # Current step label
        self.step_label = QLabel("Ready to start task...")
        self.step_label.setStyleSheet("QLabel { font-weight: bold; color: #2196F3; }")
        status_layout.addWidget(self.step_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Progress: %p%")
        status_layout.addWidget(self.progress_bar)
        
        # Stop button
        self.stop_btn = QPushButton("Stop Task")
        self.stop_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; padding: 6px; }")
        self.stop_btn.clicked.connect(self.stop_task)
        self.stop_btn.setEnabled(False)
        status_layout.addWidget(self.stop_btn)
        
        layout.addWidget(status_group)
        
        # Log group
        log_group = QGroupBox("Execution Log")
        log_layout = QVBoxLayout(log_group)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        
        # Set monospace font for better log readability
        font = self.log_text.font()
        font.setFamily("Courier New")
        font.setPointSize(9)
        self.log_text.setFont(font)
        
        log_layout.addWidget(self.log_text)
        
        # Clear log button
        clear_log_btn = QPushButton("Clear Log")
        clear_log_btn.clicked.connect(self.clear_log)
        log_layout.addWidget(clear_log_btn)
        
        layout.addWidget(log_group)
        
    def update_progress(self, step, progress_percent, message=""):
        """Update progress bar and step label"""
        self.step_label.setText(f"Step: {step}")
        self.progress_bar.setValue(progress_percent)
        
        if message:
            self.add_log_message(message, "info")
            
    def add_log_message(self, message, level="info"):
        """Add a message to the log with color coding"""
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Color coding based on level
        if level == "error":
            color = QColor("#f44336")  # Red
        elif level == "warning":
            color = QColor("#ff9800")  # Orange
        elif level == "success":
            color = QColor("#4caf50")  # Green
        else:
            color = QColor("#000000")  # Black
            
        # Format timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Insert formatted message
        cursor.insertText(f"[{timestamp}] {message}\n")
        
        # Apply color to the inserted text
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        format = cursor.charFormat()
        format.setForeground(color)
        cursor.setCharFormat(format)
        
        # Scroll to bottom
        self.log_text.setTextCursor(cursor)
        self.log_text.ensureCursorVisible()
        
    def start_task(self):
        """Called when task starts"""
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.step_label.setText("Starting task...")
        self.add_log_message("Task started", "info")
        
    def complete_task(self):
        """Called when task completes"""
        self.stop_btn.setEnabled(False)
        self.progress_bar.setValue(100)
        self.step_label.setText("Task completed!")
        self.add_log_message("Task completed successfully", "success")
        
    def stop_task(self):
        """Stop the current task"""
        self.stop_btn.setEnabled(False)
        self.step_label.setText("Stopping task...")
        self.add_log_message("Stop requested by user", "warning")
        self.stop_requested.emit()
        
    def show_error(self, error_message):
        """Display error message"""
        self.step_label.setText("Error occurred")
        self.add_log_message(f"ERROR: {error_message}", "error")
        self.stop_btn.setEnabled(False)
        
    def clear_log(self):
        """Clear the log text area"""
        self.log_text.clear()
        
    def reset(self):
        """Reset the widget to initial state"""
        self.progress_bar.setValue(0)
        self.step_label.setText("Ready to start task...")
        self.stop_btn.setEnabled(False)
        self.log_text.clear() 