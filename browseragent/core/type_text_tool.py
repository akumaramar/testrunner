# core/type_text_tool.py
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional, Annotated
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError


class TypeTextInput(BaseModel):
    selector: str = Field(description="CSS selector of the input element")
    text: str = Field(description="Text to type into the input field")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "selector": "input[name='username']",
                    "text": "myusername"
                }
            ]
        }
    }


class TypeTextTool(BaseTool):
    name: str = "type_text"
    description: str = "Types text into a specific input field using CSS selector. The element must be visible and editable. You can use various selectors like input[name='username'], #username, .username-field, etc."
    args_schema: Type[TypeTextInput] = TypeTextInput
    browser: Page = Field(default=None, description="Playwright page instance for browser interactions")

    def __init__(self, async_browser: Page):
        super().__init__()
        self.browser = async_browser

    async def _try_alternate_selectors(self, base_selector: str) -> tuple[bool, Optional[str]]:
        """Try various selector combinations to find the element."""
        # List of selector patterns to try
        selector_patterns = [
            base_selector,  # Original selector
            f"input{base_selector}",  # Add input tag if not present
            f"input[placeholder*='{base_selector.replace('[name=', '').replace(']', '')}']",  # Try placeholder
            f"input[id*='{base_selector.replace('[name=', '').replace(']', '')}']",  # Try ID
            f"input[class*='{base_selector.replace('[name=', '').replace(']', '')}']",  # Try class
            f"textarea{base_selector}",  # Try textarea
            f"*{base_selector}"  # Try any element
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
                if element:
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
                        if element:
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
                
                # Check if element is enabled
                is_enabled = await element.is_enabled()
                if not is_enabled:
                    return False, None

                # Try to focus the element
                await element.focus()
                
                return True, working_selector

            # If exact selector failed, print page content for debugging
            content = await self.browser.content()
            print(f"Page content preview: {content[:500]}...")  # First 500 chars
            
            return False, None

        except Exception as e:
            print(f"Error ensuring element ready: {str(e)}")
            return False, None

    def _run(self, selector: str, text: str) -> str:
        raise NotImplementedError("Use _arun instead - this tool only supports async operation")

    async def _arun(self, selector: str, text: str) -> str:
        try:
            # Ensure element is ready
            is_ready, working_selector = await self._ensure_element_ready(selector)
            if not is_ready:
                return f"Failed to interact with element '{selector}' - element not ready. Please check if the selector is correct."

            # Type the text using the working selector
            await self.browser.fill(working_selector, text)
            
            return f"Successfully typed '{text}' into element '{working_selector}'"
        except Exception as e:
            return f"Failed to type text: {str(e)}"
