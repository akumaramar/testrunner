# Browser Agent Desktop Application

A desktop GUI application for browser automation using AI agents.

## Features

- **User-friendly Interface**: Modern PyQt6-based desktop application
- **Real-time Progress**: Live progress updates and execution logs
- **Task Configuration**: Customize model, temperature, and verbose settings
- **Results Management**: Save, copy, and manage task results
- **Error Handling**: Graceful error handling with user-friendly messages

## Installation

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Install Playwright Browsers** (for Playwright + LangChain option):
   ```bash
   python setup_playwright.py
   ```

## Usage

### Running the Desktop Application

```bash
python main_desktop.py
```

### Running the Original Command-Line Version

```bash
python main.py
```

## Application Layout

The desktop application is divided into three main sections:

### 1. Task Input Panel (Left)
- **Agent Type**: Choose between "Browser-Use" or "Playwright + LangChain"
- **Task Description**: Enter your browser automation task
- **Model Selection**: Choose from GPT-4o-mini, GPT-4, or GPT-3.5-turbo
- **Temperature**: Adjust creativity level (0.0 - 1.0)
- **Verbose Mode**: Enable detailed logging
- **Show Browser Window**: Toggle browser visibility (Playwright only)
- **Start/Clear Buttons**: Control task execution

### 2. Progress Panel (Right Top)
- **Task Status**: Current step and progress bar
- **Execution Log**: Real-time log output with color coding
- **Stop Button**: Cancel running tasks

### 3. Results Panel (Right Bottom)
- **Task Results**: Display final results
- **Action Buttons**: Save, copy, or clear results
- **Screenshots**: View captured screenshots (future feature)

## Keyboard Shortcuts

- `Ctrl+N`: New Task
- `Ctrl+S`: Save Results
- `Ctrl+Q`: Exit Application

## File Structure

```
browseragent/
├── main.py                      # Original command-line version
├── main_desktop.py              # Desktop application entry point
├── setup_playwright.py          # Playwright browser setup script
├── ui/                          # User interface components
│   ├── main_window.py           # Main application window
│   └── widgets/                 # UI widgets
│       ├── task_input.py
│       ├── progress_widget.py
│       └── results_viewer.py
├── core/                        # Core application logic
│   ├── agent_runner.py          # Browser-use agent execution
│   └── playwright_agent_runner.py # Playwright + LangChain agent
└── backup/                      # Backup of original code
```

## Troubleshooting

### Common Issues

1. **PyQt6 Installation Error**:
   ```bash
   uv pip install PyQt6
   ```

2. **Missing OpenAI API Key**:
   Ensure your `.env` file contains the correct API key

3. **Browser-Use Issues**:
   - "Error polling for token": Try using "Playwright + LangChain" option instead
   - Browser authentication problems: Use Playwright option for better reliability

4. **Playwright Issues**:
   - Run `python setup_playwright.py` to install browsers
   - Ensure Chromium is installed: `playwright install chromium`

### Error Messages

- **"No results to save"**: Task hasn't completed or failed
- **"Please enter a task description"**: Task input is empty
- **"Error occurred"**: Check the execution log for details

## Development

### Adding New Features

1. **New Widgets**: Add to `ui/widgets/` directory
2. **Core Logic**: Add to `core/` directory
3. **UI Updates**: Modify `ui/main_window.py`

### Testing

```bash
# Test original version
python main.py

# Test desktop version
python main_desktop.py
```

## Backup and Recovery

Your original working code is backed up in the `backup/` directory. To restore:

```bash
cp backup/main_backup_20241219.py main.py
cp backup/pyproject_backup_20241219.toml pyproject.toml
uv sync
```

## License

This project uses the same license as the original browseragent application. 