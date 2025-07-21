import asyncio
import sys
import time
import logging
from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
try:
    from langchain_community.tools import StructuredTool
except ImportError:
    from langchain.tools import StructuredTool
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools.playwright.navigate import NavigateTool
from langchain_community.tools.playwright.click import ClickTool
from langchain_community.tools.playwright.extract_text import ExtractTextTool
from langchain_community.tools.playwright.get_elements import GetElementsTool
from langchain_community.tools.playwright.extract_hyperlinks import ExtractHyperlinksTool
from langchain.tools import Tool
from core.type_text_tool import TypeTextTool
#from core.click_tool import ClickTool

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlaywrightAgentRunner(QThread):
    progress_updated = pyqtSignal(str, int, str)  # step, progress_percent, message
    task_completed = pyqtSignal(str)  # results
    error_occurred = pyqtSignal(str)  # error_message
    task_started = pyqtSignal()
    task_finished = pyqtSignal()
    
    def __init__(self, task_config):
        super().__init__()
        self.task_config = task_config
        self.is_running = False
        self.start_time = None
        self.timing_log = []
        self.playwright = None
        self.browser = None
        self.page = None
        
    def log_timing(self, phase, duration):
        """Log timing information"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.timing_log.append(f"[{timestamp}] {phase}: {duration:.3f}s")
        logger.info(f"TIMING: {phase}: {duration:.3f}s")
        
    def run(self):
        """Run the agent in a separate thread"""
        self.start_time = time.time()
        logger.info("=== PLAYWRIGHT AGENT RUNNER STARTED ===")
        
        try:
            # Load environment variables
            env_start = time.time()
            load_dotenv()
            env_duration = time.time() - env_start
            self.log_timing("Environment loading", env_duration)
            
            # Emit start signal
            self.task_started.emit()
            self.is_running = True
            
            # Create event loop for this thread
            loop_start = time.time()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop_duration = time.time() - loop_start
            self.log_timing("Event loop creation", loop_duration)
            
            # Run the async task
            run_start = time.time()
            result = loop.run_until_complete(self._run_agent())
            run_duration = time.time() - run_start
            self.log_timing("Async agent execution", run_duration)
            
            # Emit completion signal
            self.task_completed.emit(str(result))
            
        except Exception as e:
            # Emit error signal
            error_msg = f"Error: {str(e)}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
        finally:
            self.is_running = False
            self.task_finished.emit()
            
            # Log final timing
            total_duration = time.time() - self.start_time
            self.log_timing("TOTAL EXECUTION TIME", total_duration)
            
            # Print complete timing log
            logger.info("=== COMPLETE TIMING LOG ===")
            for log_entry in self.timing_log:
                logger.info(log_entry)
            
            loop.close()
            
    async def _run_agent(self):
        """Run the Playwright agent with progress updates"""
        try:
            # Update progress - Initializing
            init_start = time.time()
            self.progress_updated.emit("Initializing", 10, "Setting up Playwright agent...")
            
            # Initialize Playwright
            playwright_start = time.time()
            logger.info("Initializing Playwright...")
            self.playwright = await async_playwright().start()
            
            # Set viewport size from configuration
            browser_size = self.task_config.get('browser_size', {"width": 1280, "height": 720})
            width = browser_size["width"]
            height = browser_size["height"]

            self.browser = await self.playwright.chromium.launch(
                headless=not self.task_config.get('show_browser', False),
                args=[f'--window-size={width},{height}', '--window-position=100,100']
            )
            self.page = await self.browser.new_page()
            await self.page.set_viewport_size(browser_size)

            # If showing browser, set window size and position (optional, for extra reliability)
            if self.task_config.get('show_browser', False):
                await self.page.evaluate(f"window.resizeTo({width}, {height}); window.moveTo(100, 100);")
            playwright_duration = time.time() - playwright_start
            self.log_timing("Playwright initialization", playwright_duration)
            
            # Create ChatOpenAI
            llm_start = time.time()
            logger.info("Creating ChatOpenAI instance...")
            llm = ChatOpenAI(
                model=self.task_config['model'], 
                temperature=self.task_config['temperature']
            )
            llm_duration = time.time() - llm_start
            self.log_timing("ChatOpenAI creation", llm_duration)
            
            # Create browser tools (built-in + custom type_text)
            tools_start = time.time()
            logger.info("Creating browser tools (built-in + custom type_text)...")
            
            tools = [
                NavigateTool(async_browser=self.browser),
                ClickTool(async_browser=self.browser),
                ExtractTextTool(async_browser=self.browser),
                GetElementsTool(async_browser=self.browser),
                TypeTextTool(async_browser=self.browser)
            ]
            tools_duration = time.time() - tools_start
            self.log_timing("Tools creation", tools_duration)
            
            # Create agent using initialize_agent (more compatible)
            agent_start = time.time()
            logger.info("Creating LangChain agent...")
            
            agent = initialize_agent(
                tools,
                llm,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                max_iterations=40,         # Increase the number of allowed steps
                max_execution_time=300,    # Increase the allowed time (in seconds)
                handle_parsing_errors=True
            )
            agent_duration = time.time() - agent_start
            self.log_timing("Agent creation", agent_duration)
            
            init_duration = time.time() - init_start
            self.log_timing("Total initialization", init_duration)
            
            # Update progress - Agent created
            self.progress_updated.emit("Agent Created", 20, "Playwright agent initialized successfully")
            
            # Check if we should stop
            if not self.is_running:
                return "Task cancelled by user"
            
            # Update progress - Starting execution
            self.progress_updated.emit("Executing", 30, "Starting browser automation...")
            
            # Run the agent
            execution_start = time.time()
            logger.info("Starting agent execution...")
            result = await agent.ainvoke({"input": self.task_config['task']})
            execution_duration = time.time() - execution_start
            self.log_timing("Agent execution", execution_duration)
            
            # Update progress - Completed
            self.progress_updated.emit("Completed", 100, "Task completed successfully")
            
            return result.get('output', str(result))
            
        except Exception as e:
            # Update progress - Error
            error_msg = f"Error occurred: {str(e)}"
            self.progress_updated.emit("Error", 0, error_msg)
            logger.error(f"Agent execution error: {str(e)}")
            raise e
        finally:
            # Cleanup
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop() 