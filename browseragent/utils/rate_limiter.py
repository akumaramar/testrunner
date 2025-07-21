"""
Rate limiter utility to prevent throttling
"""

import asyncio
import time
import os
from collections import deque
from typing import Optional
from functools import wraps

class RateLimiter:
    """Rate limiter for API calls"""
    
    def __init__(self, calls_per_minute=60):
        self.calls_per_minute = calls_per_minute
        self.calls = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        # Remove calls older than 1 minute
        self.calls = [call_time for call_time in self.calls if now - call_time < 60]
        
        if len(self.calls) >= self.calls_per_minute:
            sleep_time = 60 - (now - self.calls[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.calls.append(now)

class AsyncRateLimiter:
    """Async rate limiter for API calls"""
    
    def __init__(self, max_requests: int = 1, time_window: float = 1.0):
        """
        Initialize rate limiter
        
        Args:
            max_requests: Maximum number of requests allowed in time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
        
    async def acquire(self):
        """Wait if necessary to respect rate limits"""
        now = time.time()
        
        # Remove old requests outside the time window
        while self.requests and now - self.requests[0] > self.time_window:
            self.requests.popleft()
        
        # If we've hit the limit, wait
        if len(self.requests) >= self.max_requests:
            wait_time = self.time_window - (now - self.requests[0])
            if wait_time > 0:
                await asyncio.sleep(wait_time)
                return await self.acquire()  # Recursive call after waiting
        
        # Add current request
        self.requests.append(now)

    def reset(self):
        """Reset the rate limiter"""
        self.requests.clear()

class ThrottlingProtection:
    """Helper class to add throttling protection to functions"""
    
    def __init__(self, rate_limiter: AsyncRateLimiter):
        self.rate_limiter = rate_limiter
        
    async def __aenter__(self):
        await self.rate_limiter.acquire()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

def create_rate_limiter(requests_per_second: float = 1.0) -> AsyncRateLimiter:
    """
    Create a rate limiter with specified requests per second
    
    Args:
        requests_per_second: Number of requests allowed per second
        
    Returns:
        AsyncRateLimiter instance
    """
    time_window = 1.0 / requests_per_second
    return AsyncRateLimiter(max_requests=1, time_window=time_window)

def rate_limit(calls_per_minute=60):
    """Decorator to rate limit function calls"""
    limiter = RateLimiter(calls_per_minute)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter.wait_if_needed()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def optimize_browser_use_performance():
    """Set environment variables to optimize browser-use performance"""
    # Disable cloud features (already done in network_blocker)
    os.environ['BROWSER_USE_DISABLE_CLOUD'] = '1'
    os.environ['BROWSER_USE_LOCAL_ONLY'] = '1'
    
    # Performance optimizations
    os.environ['BROWSER_USE_FAST_MODE'] = '1'
    os.environ['BROWSER_USE_MINIMAL_EVALUATION'] = '1'
    os.environ['BROWSER_USE_REDUCED_SCREENSHOTS'] = '1'
    os.environ['BROWSER_USE_QUICK_DETECTION'] = '1'
    os.environ['BROWSER_USE_SKIP_ANIMATIONS'] = '1'
    os.environ['BROWSER_USE_CACHE_ELEMENTS'] = '1'
    
    # Reduce evaluation depth
    os.environ['BROWSER_USE_MAX_ELEMENTS'] = '10'  # Limit elements to evaluate
    os.environ['BROWSER_USE_EVALUATION_TIMEOUT'] = '5'  # 5 second timeout
    os.environ['BROWSER_USE_SKIP_HIDDEN'] = '1'  # Skip hidden elements
    os.environ['BROWSER_USE_SKIP_OFFSCREEN'] = '1'  # Skip off-screen elements

def get_optimized_browser_config():
    """Get optimized browser configuration for faster performance"""
    return {
        'headless': True,  # Faster rendering
        'browser_size': {"width": 800, "height": 600},  # Smaller viewport
        'disable_images': False,  # Keep images for better detection
        'disable_javascript': False,  # Keep JS for interactive elements
        'disable_css': False,  # Keep CSS for layout detection
        'fast_mode': True,
        'minimal_evaluation': True,
        'skip_animations': True,
        'cache_elements': True
    } 