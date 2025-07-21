# core/click_tool.py
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError


class ClickInput(BaseModel):
    selector: str = Field(description="CSS selector of the element to click")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "selector": "button[type='submit']"
                }
            ]
        }
    }


class ClickTool(BaseTool):
    name: str = "click"
    description: str = "Click on a clickable element (button, link, etc) using CSS selector. The element must be visible and clickable."
    args_schema: Type[ClickInput] = ClickInput
    browser: Page = Field(default=None, description="Playwright page instance for browser interactions")

    def __init__(self, async_browser: Page):
        super().__init__()
        self.browser = async_browser

    async def _try_alternate_selectors(self, base_selector: str) -> tuple[bool, Optional[str]]:
        """Try various selector combinations to find the element."""
        # List of selector patterns to try
        selector_patterns = [
            base_selector,  # Original selector
            f"button{base_selector}",  # Add button tag if not present
            f"button[type='submit']",  # Common submit button
            f"input[type='submit']",   # Submit input
            f"*{base_selector}",       # Any element with the selector
            f"button:has-text('Sign In')", # Button with specific text
            f"button:has-text('Login')",   # Common button texts
            f"button:has-text('Submit')",
            f"[role='button']",        # ARIA role button
            f"a{base_selector}",       # Link variant
            base_selector.replace("button", "*")  # Try without button tag
        ]

        # Remove any duplicates while preserving order
        selectors = list(dict.fromkeys(selector_patterns))

        for selector in selectors:
            try:
                # First check in main frame
                element = await self.browser.wait_for_selector(
                    selector,
                    state="visible",
                    timeout=2000  # Shorter timeout for each attempt
                )
                if element and await element.is_enabled():
                    # Additional check for clickability
                    box = await element.bounding_box()
                    if box and box['width'] > 0 and box['height'] > 0:
                        return True, selector

                # Then check in all frames
                frames = self.browser.frames
                for frame in frames:
                    try:
                        element = await frame.wait_for_selector(
                            selector,
                            state="visible",
                            timeout=2000
                        )
                        if element and await element.is_enabled():
                            box = await element.bounding_box()
                            if box and box['width'] > 0 and box['height'] > 0:
                                return True, selector
                    except PlaywrightTimeoutError:
                        continue

            except PlaywrightTimeoutError:
                continue
            except Exception as e:
                print(f"Error trying selector {selector}: {str(e)}")
                continue

        return False, None

    async def _ensure_element_ready(self, selector: str) -> tuple[bool, Optional[str]]:
        """Ensure element is visible, enabled and ready for interaction."""
        try:
            # First try the exact selector
            success, working_selector = await self._try_alternate_selectors(selector)
            if success:
                element = await self.browser.wait_for_selector(
                    working_selector,
                    state="visible",
                    timeout=5000
                )
                
                # Scroll element into view if needed
                await element.scroll_into_view_if_needed()
                
                # Check if element is enabled and visible
                is_enabled = await element.is_enabled()
                is_visible = await element.is_visible()
                if not is_enabled or not is_visible:
                    return False, None

                return True, working_selector

            # If exact selector failed, print page content for debugging
            content = await self.browser.content()
            print(f"Page content preview: {content[:500]}...")  # First 500 chars
            
            return False, None

        except Exception as e:
            print(f"Error ensuring element ready: {str(e)}")
            return False, None

    def _run(self, selector: str) -> str:
        raise NotImplementedError("Use _arun instead - this tool only supports async operation")

    async def _arun(self, selector: str) -> str:
        try:
            # Ensure element is ready
            is_ready, working_selector = await self._ensure_element_ready(selector)
            if not is_ready:
                return f"Failed to interact with element '{selector}' - element not ready or not clickable. Please check if the selector is correct."

            # Try different click methods
            try:
                # Method 1: Regular click
                await self.browser.click(working_selector, timeout=5000)
            except Exception as e1:
                try:
                    # Method 2: Force click
                    element = await self.browser.wait_for_selector(working_selector)
                    await element.click(force=True)
                except Exception as e2:
                    try:
                        # Method 3: JavaScript click
                        await self.browser.evaluate(f"document.querySelector('{working_selector}').click()")
                    except Exception as e3:
                        return f"Failed to click using multiple methods: {str(e1)}, {str(e2)}, {str(e3)}"

            return f"Successfully clicked element '{working_selector}'"
        except Exception as e:
            return f"Failed to click: {str(e)}" 