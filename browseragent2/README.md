# Generic Browser Automation System

A powerful, AI-driven browser automation system that can execute high-level instructions without needing to specify every detail. Built with Stagehand and GPT-4.

## Features

- 🤖 **AI-Powered**: Uses GPT-4 to understand and execute natural language instructions
- 🔄 **Automatic Retry**: Automatically retries failed operations with more detailed approaches
- 📋 **High-Level Instructions**: Just describe what you want to do, not how to do it
- 🎯 **Smart Verification**: Automatically verifies if instructions were completed successfully
- 📁 **Scenario Management**: Save and reuse automation scenarios
- 🖥️ **CLI Interface**: Easy-to-use command-line interface

## Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up your API key
echo "MODEL_API_KEY=your_openai_api_key_here" > .env
```

### 2. Run a Predefined Scenario

```bash
# List available scenarios
python run_automation.py list

# Run the task manager automation
python run_automation.py run task_manager
```

### 3. Run Custom Automation

```bash
# Interactive mode (recommended for beginners)
python run_automation.py interactive

# Custom mode
python run_automation.py custom
```

## Usage Examples

### Example 1: Task Manager Automation

Instead of writing detailed code like:
```python
# Old way - lots of specific steps
await page.click("#username")
await page.type("#username", "user")
await page.click("#password")
await page.type("#password", "pass")
await page.click("#login-button")
```

Just write:
```python
# New way - high-level instruction
instructions = [
    "Login to the application using username 'user' and password 'pass'",
    "Create a new task with title 'Complete automation project'",
    "Mark the task as completed",
    "Logout from the application"
]
```

### Example 2: E-commerce Automation

```python
instructions = [
    "Navigate to the products page",
    "Search for 'laptop'",
    "Add the first laptop to cart",
    "Proceed to checkout",
    "Fill in shipping information",
    "Complete the purchase"
]
```

### Example 3: Form Filling

```python
instructions = [
    "Fill out the contact form with name 'John Doe', email 'john@example.com', and message 'Hello world'",
    "Submit the form",
    "Verify the submission was successful"
]
```

## How It Works

1. **Instruction Processing**: The AI analyzes your high-level instruction and breaks it down into specific actions
2. **Smart Execution**: The system executes the instruction and waits for the page to respond
3. **Automatic Verification**: After each action, it verifies if the instruction was completed successfully
4. **Retry Logic**: If an instruction fails, it automatically tries a more detailed approach
5. **Context Awareness**: Each step builds on the previous ones, maintaining context throughout the automation

## File Structure

```
browseragent2/
├── main.py                    # Core automation engine
├── run_automation.py          # Command-line interface
├── automation_config.json     # Predefined automation scenarios
├── README.md                  # This file
├── pyproject.toml            # Project dependencies
└── .env                      # Environment variables (create this)
```

## Configuration

### Environment Variables

Create a `.env` file with:
```
MODEL_API_KEY=your_openai_api_key_here
```

### Automation Scenarios

Edit `automation_config.json` to add your own scenarios:

```json
{
  "scenarios": {
    "my_scenario": {
      "name": "My Custom Automation",
      "url": "https://example.com",
      "instructions": [
        "Your first instruction",
        "Your second instruction",
        "Your third instruction"
      ]
    }
  }
}
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `python run_automation.py list` | List all available scenarios |
| `python run_automation.py run <scenario>` | Run a specific scenario |
| `python run_automation.py custom` | Run custom automation with manual input |
| `python run_automation.py interactive` | Interactive mode to build automation step by step |

## Advanced Usage

### Programmatic Usage

```python
from main import run_generic_automation

# Run automation programmatically
instructions = [
    "Login to the website",
    "Navigate to the dashboard",
    "Create a new item"
]

results = await run_generic_automation(
    instructions=instructions,
    url="https://example.com"
)

# Check results
for i, result in enumerate(results, 1):
    if result['success']:
        print(f"Step {i}: ✅ Success")
    else:
        print(f"Step {i}: ❌ Failed")
```

### Custom Automation Class

```python
from main import TaskAutomation
from stagehand import StagehandConfig

config = StagehandConfig(
    env="LOCAL",
    model_name="openai/gpt-4.1-mini",
    model_client_options={"apiKey": "your_api_key"}
)

automation = TaskAutomation(config)
await automation.init()

# Run custom automation
result = await automation.execute_instruction("Click the login button")
print(f"Success: {result['success']}")

await automation.close()
```

## Tips for Writing Good Instructions

1. **Be Specific**: Instead of "click something", say "click the login button"
2. **Use Natural Language**: Write as if you're telling a person what to do
3. **Include Context**: Mention what you're looking for ("find the username field")
4. **Be Patient**: Complex instructions may take longer to execute
5. **Test Incrementally**: Start with simple instructions and build up

## Troubleshooting

### Common Issues

1. **Login Fails**: Make sure credentials are correct and the login form is visible
2. **Elements Not Found**: Try being more specific about what you're looking for
3. **Page Not Loading**: Check your internet connection and the URL
4. **API Key Issues**: Ensure your OpenAI API key is valid and has sufficient credits

### Debug Mode

The system automatically logs detailed information about each step. Check the console output for:
- Page state analysis
- Instruction execution attempts
- Verification results
- Error messages

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
