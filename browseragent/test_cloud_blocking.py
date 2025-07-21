#!/usr/bin/env python3
"""
Test script to verify cloud blocking functionality
"""

import os
import sys
from utils.network_blocker import test_cloud_blocking, disable_cloud_environment

def test_environment_variables():
    """Test if environment variables are set correctly"""
    print("Testing environment variables...")
    
    disable_cloud_environment()
    
    expected_vars = [
        'BROWSER_USE_DISABLE_CLOUD',
        'BROWSER_USE_LOCAL_ONLY', 
        'BROWSER_USE_NO_UPLOAD',
        'BROWSER_USE_OFFLINE'
    ]
    
    for var in expected_vars:
        value = os.environ.get(var)
        if value == '1':
            print(f"✓ {var} = {value}")
        else:
            print(f"✗ {var} not set correctly")
            return False
    
    return True

def test_network_blocking():
    """Test if network blocking works"""
    print("\nTesting network blocking...")
    
    if test_cloud_blocking():
        print("✓ Cloud blocking is working")
        return True
    else:
        print("✗ Cloud blocking failed")
        return False

def test_browser_use_import():
    """Test if browser-use can be imported with cloud blocking"""
    print("\nTesting browser-use import with cloud blocking...")
    
    try:
        # Set environment variables first
        disable_cloud_environment()
        
        # Try to import browser-use
        from browser_use import Agent
        from browser_use.llm import ChatOpenAI
        
        print("✓ browser-use imported successfully")
        return True
        
    except Exception as e:
        print(f"✗ browser-use import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Cloud Blocking Test Suite")
    print("=" * 30)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Network Blocking", test_network_blocking),
        ("Browser-Use Import", test_browser_use_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        else:
            print(f"Test failed: {test_name}")
    
    print(f"\n{'='*30}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Cloud blocking is working correctly.")
    else:
        print("✗ Some tests failed. Cloud blocking may not work properly.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 