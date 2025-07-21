import asyncio
import sys
import time
import logging
import os
from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal
from dotenv import load_dotenv
from browser_use import Agent
from browser_use.llm import ChatOpenAI
from utils.rate_limiter import create_rate_limiter, optimize_browser_use_performance, get_optimized_browser_config
from utils.network_blocker import disable_cloud_environment

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentRunner(QThread):
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
        self.rate_limiter = None
        
    def log_timing(self, phase, duration):
        """Log timing information"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.timing_log.append(f"[{timestamp}] {phase}: {duration:.3f}s")
        logger.info(f"TIMING: {phase}: {duration:.3f}s")
        
    def run(self):
        """Run the agent in a separate thread"""
        self.start_time = time.time()
        logger.info("=== AGENT RUNNER STARTED ===")
        
        try:
            # Load environment variables
            env_start = time.time()
            load_dotenv()
            
            # Configure environment to disable cloud uploads if requested
            if self.task_config.get('disable_cloud', True):
                # Set environment variables to disable cloud features
                disable_cloud_environment()
                logger.info("Cloud uploads disabled via environment variables")
            
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
        """Run the browser agent with progress updates"""
        try:
            # Update progress - Initializing
            init_start = time.time()
            self.progress_updated.emit("Initializing", 10, "Setting up browser agent...")
            
            # Create the agent with throttling prevention
            agent_start = time.time()
            logger.info("Creating ChatOpenAI instance...")
            
            # Initialize rate limiter if enabled
            if self.task_config.get('rate_limit', True):
                self.rate_limiter = create_rate_limiter(requests_per_second=0.5)  # 1 request every 2 seconds
                logger.info("Rate limiter initialized")
            
            llm = ChatOpenAI(
                model=self.task_config['model'], 
                temperature=self.task_config['temperature']
            )
            llm_duration = time.time() - agent_start
            self.log_timing("ChatOpenAI creation", llm_duration)
            
            agent_create_start = time.time()
            logger.info("Creating Agent instance...")
            
            # Apply performance optimizations
            if self.task_config.get('disable_cloud', True):
                disable_cloud_environment()
                optimize_browser_use_performance()
            
            # Get optimized browser configuration
            optimized_config = get_optimized_browser_config()
            
            # Create agent with basic configuration
            agent_config = {
                'llm': llm,
                'verbose': self.task_config['verbose'],
                'task': self.task_config['task'],
            }
            
            # Add headless mode if supported
            if hasattr(Agent, 'headless'):
                agent_config['headless'] = self.task_config.get('headless', True)
            
            # Add browser size configuration if supported
            browser_size = self.task_config.get('browser_size', optimized_config['browser_size'])
            if hasattr(Agent, 'viewport'):
                agent_config['viewport'] = browser_size
            
            # Add performance optimizations
            if hasattr(Agent, 'fast_mode'):
                agent_config['fast_mode'] = optimized_config['fast_mode']
            if hasattr(Agent, 'minimal_evaluation'):
                agent_config['minimal_evaluation'] = optimized_config['minimal_evaluation']
            if hasattr(Agent, 'skip_animations'):
                agent_config['skip_animations'] = optimized_config['skip_animations']
            if hasattr(Agent, 'cache_elements'):
                agent_config['cache_elements'] = optimized_config['cache_elements']
            
            agent = Agent(**agent_config)
            agent_create_duration = time.time() - agent_create_start
            self.log_timing("Agent creation", agent_create_duration)
            
            init_duration = time.time() - init_start
            self.log_timing("Total initialization", init_duration)
            
            # Update progress - Agent created
            self.progress_updated.emit("Agent Created", 20, "Browser agent initialized successfully")
            
            # Check if we should stop
            if not self.is_running:
                return "Task cancelled by user"
            
            # Update progress - Starting execution
            self.progress_updated.emit("Executing", 30, "Starting browser automation...")
            
            # Run the agent with throttling protection
            execution_start = time.time()
            logger.info("Starting agent.run()...")
            
            # Add retry logic for throttling issues
            max_retries = 3
            retry_delay = 5  # seconds
            
            for attempt in range(max_retries):
                try:
                    self.progress_updated.emit("Executing", 30 + (attempt * 10), f"Attempt {attempt + 1}/{max_retries}...")
                    
                    # Apply rate limiting if enabled
                    if self.rate_limiter:
                        await self.rate_limiter.acquire()
                        logger.info("Rate limit applied before agent execution")
                    
                    # Cloud uploads are already disabled via environment variables if requested
                    result = await agent.run()
                    break
                except Exception as e:
                    error_str = str(e).lower()
                    
                    # Detects throttling and retries with backoff
                    if 'throttle' in error_str or 'rate limit' in error_str:
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        # Non-throttling error, don't retry
                        raise e
            
            execution_duration = time.time() - execution_start
            self.log_timing("Agent.run() execution", execution_duration)
            
            # Update progress - Completed
            self.progress_updated.emit("Completed", 100, "Task completed successfully")
            
            return result
            
        except Exception as e:
            # Update progress - Error
            error_msg = f"Error occurred: {str(e)}"
            self.progress_updated.emit("Error", 0, error_msg)
            logger.error(f"Agent execution error: {str(e)}")
            raise e
            
    def stop(self):
        """Stop the agent execution"""
        self.is_running = False
        self.progress_updated.emit("Stopping", 0, "Stopping task execution...")
        logger.info("Agent execution stopped by user") 