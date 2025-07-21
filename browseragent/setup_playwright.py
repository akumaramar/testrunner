#!/usr/bin/env python3
"""
Setup script for Playwright browsers
Run this script to install the required browsers for Playwright
"""

import subprocess
import sys
import os

def install_playwright_browsers():
    """Install Playwright browsers"""
    print("Installing Playwright browsers...")
    
    try:
        # Install browsers
        result = subprocess.run([
            sys.executable, "-m", "playwright", "install", "chromium"
        ], capture_output=True, text=True, check=True)
        
        print("✓ Chromium browser installed successfully")
        print(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install browsers: {e}")
        print(f"Error output: {e.stderr}")
        return False

def verify_installation():
    """Verify Playwright installation"""
    print("\nVerifying Playwright installation...")
    
    try:
        # Test import
        import playwright
        print("✓ Playwright library imported successfully")
        
        # Test browser launch
        from playwright.async_api import async_playwright
        print("✓ Playwright async API imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Playwright import failed: {e}")
        return False

def main():
    """Main setup function"""
    print("Playwright Setup Script")
    print("=" * 30)
    
    # Check if playwright is installed
    try:
        import playwright
        print("✓ Playwright is already installed")
    except ImportError:
        print("✗ Playwright not found. Please install it first:")
        print("  uv add playwright")
        return
    
    # Install browsers
    if install_playwright_browsers():
        print("\n✓ Browser installation completed")
    else:
        print("\n✗ Browser installation failed")
        return
    
    # Verify installation
    if verify_installation():
        print("\n✓ Playwright setup completed successfully!")
        print("\nYou can now use the Playwright + LangChain agent option.")
    else:
        print("\n✗ Playwright setup verification failed")

if __name__ == "__main__":
    main() 