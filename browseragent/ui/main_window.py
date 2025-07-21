import time
import logging
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QSplitter, QTabWidget, QMenuBar, QToolBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction
from .widgets.task_input import TaskInputWidget
from .widgets.progress_widget import ProgressWidget
from .widgets.results_viewer import ResultsViewer
from core.agent_runner import AgentRunner
from core.playwright_agent_runner import PlaywrightAgentRunner

# Set up logging
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("=== MAIN WINDOW INITIALIZATION STARTED ===")
        init_start = time.time()
        
        self.setWindowTitle("Browser Agent - Desktop")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize components
        self.agent_runner = None
        self.setup_ui()
        self.setup_menu()
        self.setup_toolbar()
        
        init_duration = time.time() - init_start
        logger.info(f"Main window initialization completed in {init_duration:.3f}s")
        
    def setup_ui(self):
        ui_start = time.time()
        logger.info("Setting up UI components...")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Task input
        task_input_start = time.time()
        self.task_input = TaskInputWidget()
        self.task_input.task_started.connect(self.start_task)
        task_input_duration = time.time() - task_input_start
        logger.info(f"Task input widget created in {task_input_duration:.3f}s")
        
        # Right panel - Progress and results
        right_panel_start = time.time()
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        progress_start = time.time()
        self.progress_widget = ProgressWidget()
        progress_duration = time.time() - progress_start
        logger.info(f"Progress widget created in {progress_duration:.3f}s")
        
        results_start = time.time()
        self.results_viewer = ResultsViewer()
        results_duration = time.time() - results_start
        logger.info(f"Results viewer created in {results_duration:.3f}s")
        
        right_layout.addWidget(self.progress_widget)
        right_layout.addWidget(self.results_viewer)
        right_panel_duration = time.time() - right_panel_start
        logger.info(f"Right panel setup completed in {right_panel_duration:.3f}s")
        
        # Add to splitter
        splitter.addWidget(self.task_input)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 800])  # Initial sizes
        
        main_layout.addWidget(splitter)
        
        ui_duration = time.time() - ui_start
        logger.info(f"UI setup completed in {ui_duration:.3f}s")
        
    def setup_menu(self):
        menu_start = time.time()
        logger.info("Setting up menu bar...")
        
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        new_task_action = QAction("New Task", self)
        new_task_action.setShortcut("Ctrl+N")
        new_task_action.triggered.connect(self.new_task)
        file_menu.addAction(new_task_action)
        
        save_action = QAction("Save Results", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_results)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Settings menu
        settings_menu = menubar.addMenu("Settings")
        preferences_action = QAction("Preferences", self)
        preferences_action.triggered.connect(self.show_preferences)
        settings_menu.addAction(preferences_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        menu_duration = time.time() - menu_start
        logger.info(f"Menu setup completed in {menu_duration:.3f}s")
        
    def setup_toolbar(self):
        toolbar_start = time.time()
        logger.info("Setting up toolbar...")
        
        toolbar = self.addToolBar("Main Toolbar")
        
        new_task_action = QAction("New Task", self)
        new_task_action.triggered.connect(self.new_task)
        toolbar.addAction(new_task_action)
        
        toolbar.addSeparator()
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_preferences)
        toolbar.addAction(settings_action)
        
        toolbar_duration = time.time() - toolbar_start
        logger.info(f"Toolbar setup completed in {toolbar_duration:.3f}s")
        
    def start_task(self, task_config):
        task_start_time = time.time()
        logger.info("=== TASK START REQUESTED ===")
        logger.info(f"Task config: {task_config}")
        
        # Choose agent type based on selection
        agent_type = task_config.get('agent_type', 'Browser-Use')
        logger.info(f"Selected agent type: {agent_type}")
        
        # Start agent execution in separate thread
        runner_start = time.time()
        
        if agent_type == "Playwright + LangChain":
            self.agent_runner = PlaywrightAgentRunner(task_config)
            logger.info("Using Playwright + LangChain agent")
        else:
            self.agent_runner = AgentRunner(task_config)
            logger.info("Using Browser-Use agent")
        
        # Connect signals
        self.agent_runner.progress_updated.connect(self.progress_widget.update_progress)
        self.agent_runner.task_completed.connect(self.results_viewer.show_results)
        self.agent_runner.error_occurred.connect(self.progress_widget.show_error)
        self.agent_runner.task_started.connect(self.progress_widget.start_task)
        self.agent_runner.task_finished.connect(self.task_input.enable_start_button)
        self.agent_runner.task_finished.connect(self.progress_widget.complete_task)
        
        runner_setup_duration = time.time() - runner_start
        logger.info(f"Agent runner setup completed in {runner_setup_duration:.3f}s")
        
        # Start the thread
        thread_start = time.time()
        self.agent_runner.start()
        thread_duration = time.time() - thread_start
        logger.info(f"Agent thread started in {thread_duration:.3f}s")
        
        total_task_start_duration = time.time() - task_start_time
        logger.info(f"Total task start process completed in {total_task_start_duration:.3f}s")
        
    def new_task(self):
        logger.info("New task requested")
        self.task_input.clear_form()
        
    def save_results(self):
        logger.info("Save results requested")
        self.results_viewer.save_results()
        
    def show_preferences(self):
        # TODO: Implement preferences dialog
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Preferences", "Preferences dialog will be implemented soon!")
        
    def show_about(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(self, "About Browser Agent", 
                         "Browser Agent Desktop Application\n\n"
                         "A desktop GUI for browser automation using AI agents.\n\n"
                         "Version: 1.0.0") 