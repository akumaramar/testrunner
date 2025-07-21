#!/usr/bin/env python3
"""
Test script to verify browser window sizing functionality
"""

import asyncio
import sys
import os
from playwright.async_api import async_playwright

async def test_browser_sizing():
    """Test browser window sizing with different configurations"""
    print("Testing Browser Window Sizing")
    print("=" * 40)
    
    # Test different sizes
    test_sizes = [
        {"width": 1280, "height": 720},
        {"width": 1920, "height": 1080},
        {"width": 1366, "height": 768},
        {"width": 800, "height": 600}
    ]
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            
            for i, size in enumerate(test_sizes, 1):
                print(f"\nTest {i}: {size['width']}x{size['height']}")
                
                page = await browser.new_page()
                
                # Set viewport size
                await page.set_viewport_size(size)
                
                # Set window size and position
                await page.evaluate(f"""
                    window.resizeTo({size['width']}, {size['height']});
                    window.moveTo(100 + {i * 50}, 100 + {i * 50});
                """)
                
                # Navigate to a test page
                await page.goto("https://www.google.com")
                
                # Wait a moment to see the window
                await asyncio.sleep(2)
                
                # Get actual viewport size
                viewport = await page.evaluate("""
                    () => ({
                        width: window.innerWidth,
                        height: window.innerHeight
                    })
                """)
                
                print(f"  Expected: {size['width']}x{size['height']}")
                print(f"  Actual: {viewport['width']}x{viewport['height']}")
                
                # Close the page
                await page.close()
            
            await browser.close()
            
    except Exception as e:
        print(f"Error during testing: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("Browser sizing test completed!")
    return True

def test_ui_configuration():
    """Test UI configuration parsing"""
    print("\nTesting UI Configuration Parsing")
    print("=" * 40)
    
    # Simulate the UI configuration logic
    def parse_browser_size(size_text, custom_width=None, custom_height=None):
        if size_text == "Custom":
            try:
                width = int(custom_width) if custom_width else 1280
                height = int(custom_height) if custom_height else 720
                return {"width": width, "height": height}
            except ValueError:
                return {"width": 1280, "height": 720}
        else:
            width, height = size_text.split("x")
            return {"width": int(width), "height": int(height)}
    
    # Test cases
    test_cases = [
        ("1280x720", None, None),
        ("1920x1080", None, None),
        ("Custom", "1600", "900"),
        ("Custom", "invalid", "invalid"),
        ("1366x768", None, None)
    ]
    
    for size_text, custom_w, custom_h in test_cases:
        result = parse_browser_size(size_text, custom_w, custom_h)
        print(f"Input: {size_text} (custom: {custom_w}x{custom_h})")
        print(f"Output: {result['width']}x{result['height']}")
        print()

if __name__ == "__main__":
    print("Browser Window Sizing Test Suite")
    print("=" * 50)
    
    # Test UI configuration
    test_ui_configuration()
    
    # Test actual browser sizing (only if user wants to see browser windows)
    if len(sys.argv) > 1 and sys.argv[1] == "--with-browser":
        asyncio.run(test_browser_sizing())
    else:
        print("\nTo test actual browser window sizing, run:")
        print("python test_browser_sizing.py --with-browser")
        print("\nThis will open browser windows to demonstrate the sizing.") 