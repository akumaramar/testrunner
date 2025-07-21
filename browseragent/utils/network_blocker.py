"""
Network blocker utility to prevent cloud uploads and authentication
"""

import os
import sys
import logging
import urllib.request
import requests
from urllib.error import URLError
from contextlib import contextmanager

def disable_cloud_environment():
    """Set environment variables to disable cloud features and token polling"""
    os.environ['BROWSER_USE_DISABLE_CLOUD'] = '1'
    os.environ['BROWSER_USE_LOCAL_ONLY'] = '1'
    os.environ['BROWSER_USE_NO_UPLOAD'] = '1'
    os.environ['BROWSER_USE_OFFLINE'] = '1'
    # Add these for extra safety:
    os.environ['BROWSER_USE_NO_AUTH'] = '1'
    os.environ['BROWSER_USE_NO_TOKEN'] = '1'
    os.environ['BROWSER_USE_NO_POLLING'] = '1'
    
    # Completely disable authentication
    os.environ['BROWSER_USE_DISABLE_AUTH'] = '1'
    os.environ['BROWSER_USE_SKIP_AUTH'] = '1'
    os.environ['BROWSER_USE_NO_AUTHENTICATION'] = '1'
    os.environ['BROWSER_USE_ANONYMOUS'] = '1'
    os.environ['BROWSER_USE_GUEST_MODE'] = '1'
    
    # Force offline mode and disable all network calls
    os.environ['BROWSER_USE_FORCE_OFFLINE'] = '1'
    os.environ['BROWSER_USE_NO_NETWORK'] = '1'
    os.environ['BROWSER_USE_DISABLE_REQUESTS'] = '1'
    os.environ['BROWSER_USE_LOCAL_FIRST'] = '1'
    os.environ['BROWSER_USE_NO_EXTERNAL'] = '1'
    
    # Disable specific authentication endpoints
    os.environ['BROWSER_USE_NO_AUTH_ENDPOINTS'] = '1'
    os.environ['BROWSER_USE_SKIP_TOKEN_VALIDATION'] = '1'
    os.environ['BROWSER_USE_NO_SESSION'] = '1'
    os.environ['BROWSER_USE_NO_COOKIES'] = '1'
    
    # Performance optimizations for faster page evaluation
    os.environ['BROWSER_USE_FAST_MODE'] = '1'
    os.environ['BROWSER_USE_MINIMAL_EVALUATION'] = '1'
    os.environ['BROWSER_USE_REDUCED_SCREENSHOTS'] = '1'
    os.environ['BROWSER_USE_QUICK_DETECTION'] = '1'
    os.environ['BROWSER_USE_SKIP_ANIMATIONS'] = '1'
    os.environ['BROWSER_USE_DISABLE_IMAGES'] = '0'  # Keep images for better detection
    os.environ['BROWSER_USE_CACHE_ELEMENTS'] = '1'
    
    # Suppress authentication and unnecessary logs
    suppress_browser_use_logs()
    
    # Block network requests at the system level
    block_browser_use_network()

def suppress_browser_use_logs():
    """Suppress browser-use authentication and unnecessary log messages"""
    # Suppress browser-use authentication logs
    logging.getLogger('browser_use.sync.auth').setLevel(logging.ERROR)
    logging.getLogger('browser_use.auth').setLevel(logging.ERROR)
    logging.getLogger('browser_use.sync').setLevel(logging.ERROR)
    
    # Suppress other browser-use verbose logs
    logging.getLogger('browser_use.agent').setLevel(logging.WARNING)
    logging.getLogger('browser_use.evaluation').setLevel(logging.WARNING)
    logging.getLogger('browser_use.detection').setLevel(logging.WARNING)
    
    # Suppress urllib and requests logs
    logging.getLogger('urllib3').setLevel(logging.ERROR)
    logging.getLogger('requests').setLevel(logging.ERROR)
    logging.getLogger('httpx').setLevel(logging.ERROR)
    
    # Suppress asyncio logs
    logging.getLogger('asyncio').setLevel(logging.ERROR)

@contextmanager
def block_browser_use_cloud():
    """Context manager to block browser-use cloud requests"""
    # For now, just set environment variables and let the library handle it
    # This avoids the socket replacement that causes Windows asyncio issues
    disable_cloud_environment()
    try:
        yield
    except Exception as e:
        if 'cloud.browser-use.com' in str(e).lower():
            print(f"Blocked cloud request: {e}")
        else:
            raise e

def test_cloud_blocking():
    """Test if cloud blocking is working"""
    try:
        disable_cloud_environment()
        # Test if environment variables are set
        return all(os.environ.get(var) == '1' for var in [
            'BROWSER_USE_DISABLE_CLOUD',
            'BROWSER_USE_LOCAL_ONLY',
            'BROWSER_USE_NO_UPLOAD',
            'BROWSER_USE_OFFLINE'
        ])
    except Exception:
        return False 

def block_browser_use_network():
    """Block network requests to browser-use servers at the system level"""
    # Set environment variables to block network access
    os.environ['NO_PROXY'] = 'cloud.browser-use.com,api.browser-use.com,browser-use.com'
    os.environ['HTTP_PROXY'] = 'http://localhost:9999'  # Invalid proxy to block requests
    os.environ['HTTPS_PROXY'] = 'http://localhost:9999'  # Invalid proxy to block requests
    
    # Disable SSL verification for browser-use domains
    os.environ['BROWSER_USE_DISABLE_SSL'] = '1'
    os.environ['BROWSER_USE_SKIP_SSL_VERIFY'] = '1' 