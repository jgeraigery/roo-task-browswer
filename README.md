# Roo Task Browser

A FastHTML-based web application for browsing and viewing your Roo task history.

## Features

- List all Roo tasks sorted by most recent
- Search tasks by name
- View both UI messages and API conversation history
- Markdown rendering for message content
- Syntax highlighting for code blocks and JSON

## Requirements

- Python 3.7+
- FastHTML

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/roo-task-browser.git
   cd roo-task-browser
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```bash
python app/main.py
```

or

```bash
./app/main.py
```

Then open a web browser and navigate to:
```
http://localhost:5001
```

## Task Directory

The application looks for Roo tasks in:
```
~/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/tasks
```

## File Types

For each task, the application can display:
- `ui_messages.json` - UI interaction messages
- `api_conversation_history.json` - Backend API conversation history

## License

MIT