from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTextEdit, QComboBox, QLineEdit,
                             QSlider, QCheckBox, QPushButton, QGroupBox)
from PyQt6.QtCore import pyqtSignal, Qt

class TaskInputWidget(QWidget):
    task_started = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Task description group
        task_group = QGroupBox("Task Description")
        task_layout = QVBoxLayout(task_group)
        
        self.task_text = QTextEdit()
        self.task_text.setPlaceholderText("Enter your browser automation task...\n\nExample: Search for the best north indian restaurant in bangalore")
        self.task_text.setMaximumHeight(150)
        task_layout.addWidget(self.task_text)
        layout.addWidget(task_group)
        
        # Agent configuration group
        config_group = QGroupBox("Agent Configuration")
        config_layout = QVBoxLayout(config_group)
        
        # Agent type selection
        agent_layout = QHBoxLayout()
        agent_layout.addWidget(QLabel("Agent Type:"))
        self.agent_combo = QComboBox()
        self.agent_combo.addItems(["Browser-Use", "Playwright + LangChain"])
        self.agent_combo.setToolTip("Browser-Use: Original library (may have auth issues)\nPlaywright + LangChain: More reliable alternative")
        agent_layout.addWidget(self.agent_combo)
        config_layout.addLayout(agent_layout)
        
        # Model selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"])
        model_layout.addWidget(self.model_combo)
        config_layout.addLayout(model_layout)
        
        # Temperature
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(QLabel("Temperature:"))
        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setRange(0, 100)
        self.temp_slider.setValue(0)
        self.temp_label = QLabel("0.0")
        self.temp_slider.valueChanged.connect(self.update_temp_label)
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_label)
        config_layout.addLayout(temp_layout)
        
        # Verbose mode
        self.verbose_check = QCheckBox("Verbose Mode")
        self.verbose_check.setToolTip("Enable detailed logging during task execution")
        config_layout.addWidget(self.verbose_check)
        
        # Show browser option (for Playwright)
        self.show_browser_check = QCheckBox("Show Browser Window")
        self.show_browser_check.setToolTip("Show browser window during execution (Playwright only)")
        self.show_browser_check.setChecked(True)
        config_layout.addWidget(self.show_browser_check)
        
        # Browser window size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Browser Size:"))
        self.size_combo = QComboBox()
        self.size_combo.addItems(["1280x720", "1920x1080", "1366x768", "1440x900", "Custom"])
        self.size_combo.setToolTip("Set browser window size")
        self.size_combo.currentTextChanged.connect(self.on_size_changed)
        size_layout.addWidget(self.size_combo)
        
        # Custom size inputs
        self.custom_size_widget = QWidget()
        self.custom_size_layout = QHBoxLayout(self.custom_size_widget)
        self.custom_size_layout.addWidget(QLabel("Width:"))
        self.width_input = QLineEdit("1280")
        self.width_input.setMaximumWidth(80)
        self.custom_size_layout.addWidget(self.width_input)
        self.custom_size_layout.addWidget(QLabel("Height:"))
        self.height_input = QLineEdit("720")
        self.height_input.setMaximumWidth(80)
        self.custom_size_layout.addWidget(self.height_input)
        self.custom_size_widget.setVisible(False)
        config_layout.addLayout(size_layout)
        config_layout.addWidget(self.custom_size_widget)
        
        # Performance optimizations (for browser-use)
        perf_group = QGroupBox("Performance Optimizations")
        perf_layout = QVBoxLayout()
        
        self.fast_mode_check = QCheckBox("Fast Mode")
        self.fast_mode_check.setToolTip("Enable fast mode for quicker page evaluation")
        self.fast_mode_check.setChecked(True)
        perf_layout.addWidget(self.fast_mode_check)
        
        self.minimal_eval_check = QCheckBox("Minimal Evaluation")
        self.minimal_eval_check.setToolTip("Reduce element evaluation depth for speed")
        self.minimal_eval_check.setChecked(True)
        perf_layout.addWidget(self.minimal_eval_check)
        
        self.skip_animations_check = QCheckBox("Skip Animations")
        self.skip_animations_check.setToolTip("Skip CSS animations for faster processing")
        self.skip_animations_check.setChecked(True)
        perf_layout.addWidget(self.skip_animations_check)
        
        self.cache_elements_check = QCheckBox("Cache Elements")
        self.cache_elements_check.setToolTip("Cache detected elements for reuse")
        self.cache_elements_check.setChecked(True)
        perf_layout.addWidget(self.cache_elements_check)
        
        perf_group.setLayout(perf_layout)
        config_layout.addWidget(perf_group)
        
        # Anti-throttling options
        throttling_group = QGroupBox("Anti-Throttling Settings")
        throttling_layout = QVBoxLayout(throttling_group)
        
        self.headless_check = QCheckBox("Headless Mode")
        self.headless_check.setToolTip("Run browser in headless mode to reduce resource usage")
        self.headless_check.setChecked(True)
        throttling_layout.addWidget(self.headless_check)
        
        self.rate_limit_check = QCheckBox("Enable Rate Limiting")
        self.rate_limit_check.setToolTip("Limit requests to prevent throttling")
        self.rate_limit_check.setChecked(True)
        throttling_layout.addWidget(self.rate_limit_check)
        
        self.disable_cloud_check = QCheckBox("Disable Cloud Uploads")
        self.disable_cloud_check.setToolTip("Prevent uploading results to browser-use cloud service")
        self.disable_cloud_check.setChecked(True)
        throttling_layout.addWidget(self.disable_cloud_check)
        
        config_layout.addWidget(throttling_group)
        
        layout.addWidget(config_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Task")
        self.start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 8px; font-weight: bold; }")
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; padding: 8px; }")
        self.start_btn.clicked.connect(self.start_task)
        self.clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.clear_btn)
        layout.addLayout(button_layout)
        
        layout.addStretch()
        
    def update_temp_label(self, value):
        self.temp_label.setText(f"{value / 100:.1f}")
        
    def on_size_changed(self, size_text):
        """Handle browser size selection change"""
        if size_text == "Custom":
            self.custom_size_widget.setVisible(True)
        else:
            self.custom_size_widget.setVisible(False)
        
    def start_task(self):
        task_description = self.task_text.toPlainText().strip()
        
        if not task_description:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Input Error", "Please enter a task description!")
            return
            
        # Parse browser size
        size_text = self.size_combo.currentText()
        if size_text == "Custom":
            try:
                width = int(self.width_input.text())
                height = int(self.height_input.text())
                browser_size = {"width": width, "height": height}
            except ValueError:
                browser_size = {"width": 1280, "height": 720}  # Default if invalid input
        else:
            width, height = size_text.split("x")
            browser_size = {"width": int(width), "height": int(height)}
        
        task_config = {
            'task': task_description,
            'agent_type': self.agent_combo.currentText(),
            'model': self.model_combo.currentText(),
            'temperature': self.temp_slider.value() / 100,
            'verbose': self.verbose_check.isChecked(),
            'show_browser': self.show_browser_check.isChecked(),
            'browser_size': browser_size,
            'headless': self.headless_check.isChecked(),
            'rate_limit': self.rate_limit_check.isChecked(),
            'disable_cloud': self.disable_cloud_check.isChecked(),
            # Performance optimizations
            'fast_mode': self.fast_mode_check.isChecked(),
            'minimal_evaluation': self.minimal_eval_check.isChecked(),
            'skip_animations': self.skip_animations_check.isChecked(),
            'cache_elements': self.cache_elements_check.isChecked()
        }
        
        # Disable start button during execution
        self.start_btn.setEnabled(False)
        self.start_btn.setText("Running...")
        
        self.task_started.emit(task_config)
        
    def clear_form(self):
        self.task_text.clear()
        self.temp_slider.setValue(0)
        self.verbose_check.setChecked(False)
        self.show_browser_check.setChecked(True)
        self.size_combo.setCurrentText("1280x720")
        self.width_input.setText("1280")
        self.height_input.setText("720")
        self.custom_size_widget.setVisible(False)
        self.headless_check.setChecked(True)
        self.rate_limit_check.setChecked(True)
        self.disable_cloud_check.setChecked(True)
        self.start_btn.setEnabled(True)
        self.start_btn.setText("Start Task")
        
    def enable_start_button(self):
        """Re-enable start button after task completion"""
        self.start_btn.setEnabled(True)
        self.start_btn.setText("Start Task") 