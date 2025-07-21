#!/usr/bin/env python3
"""
Test script to verify browser-use authentication log suppression
"""

import logging
from utils.network_blocker import disable_cloud_environment, suppress_browser_use_logs

def test_auth_suppression():
    """Test if authentication logs are suppressed"""
    print("Testing Browser-Use Authentication Log Suppression")
    print("=" * 50)
    
    # Apply environment variables and log suppression
    disable_cloud_environment()
    
    # Test logging levels
    auth_logger = logging.getLogger('browser_use.sync.auth')
    sync_logger = logging.getLogger('browser_use.sync')
    agent_logger = logging.getLogger('browser_use.agent')
    
    print(f"Auth logger level: {auth_logger.level} (ERROR={logging.ERROR})")
    print(f"Sync logger level: {sync_logger.level} (ERROR={logging.ERROR})")
    print(f"Agent logger level: {agent_logger.level} (WARNING={logging.WARNING})")
    
    # Test if logs are actually suppressed
    print("\nTesting log suppression:")
    auth_logger.info("This auth log should NOT appear")
    auth_logger.warning("This auth warning should NOT appear")
    auth_logger.error("This auth error SHOULD appear")
    
    agent_logger.info("This agent info should NOT appear")
    agent_logger.warning("This agent warning SHOULD appear")
    agent_logger.error("This agent error SHOULD appear")
    
    print("\n✅ Authentication log suppression test completed!")
    print("Check that only ERROR level logs appear above.")

if __name__ == "__main__":
    test_auth_suppression() 