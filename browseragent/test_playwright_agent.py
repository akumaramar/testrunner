import sys
import os
import asyncio
from core.playwright_agent_runner import PlaywrightAgentRunner

# Minimal PyQt6 event loop for QThread
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QEventLoop

def run_playwright_agent_test():
    app = QApplication([])
    loop = QEventLoop(app)
    
    # Minimal task config
    task_config = {
        'task': 'Go to https://example.com and report the page title',
        'agent_type': 'Playwright + LangChain',
        'model': 'gpt-4o-mini',
        'temperature': 0,
        'verbose': True,
        'show_browser': False,
        'headless': True,
        'browser_size': {"width": 800, "height": 600},
        'rate_limit': False,
        'disable_cloud': True
    }

    result_holder = {'result': None, 'error': None}

    def on_completed(result):
        print("[TEST] Task completed:", result)
        result_holder['result'] = result
        app.quit()

    def on_error(error):
        print("[TEST] Error:", error)
        result_holder['error'] = error
        app.quit()

    agent = PlaywrightAgentRunner(task_config)
    agent.task_completed.connect(on_completed)
    agent.error_occurred.connect(on_error)
    agent.start()
    app.exec()
    return result_holder

if __name__ == "__main__":
    result = run_playwright_agent_test()
    if result['error']:
        print("[TEST FAILED]", result['error'])
        sys.exit(1)
    print("[TEST PASSED]", result['result'])
    sys.exit(0) 