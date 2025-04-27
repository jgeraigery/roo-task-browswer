#!/usr/bin/env python3
from fasthtml.common import *
import json
from pathlib import Path
import os
import re

# Path to Roo tasks directory
TASKS_DIR = Path.home() / 'Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/tasks'

# Initialize FastHTML app with markdown and syntax highlighting support
app, rt = fast_app(
    pico=False,  # Disable Pico CSS for better control over styling
    hdrs=(
        MarkdownJS(),
        HighlightJS(langs=['json', 'python', 'javascript', 'bash', 'markdown']),
        # Add some custom styling
        Style("""
            body { 
                overflow-x: hidden; 
                background-color: #ffffff;
                color: #333333;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            .app-container {
                display: flex;
                width: 100%;
                min-height: 100vh;
            }
            /* Resizable sidebar with handle */
            .sidebar {
                width: 25%;
                min-width: 250px;
                max-width: 60%;
                padding: 1rem;
                border-right: 5px solid #ddd;
                overflow-y: auto;
                height: 100vh;
                position: sticky;
                top: 0;
                background-color: #f8f8f8;
                box-sizing: border-box;
                z-index: 1;
            }
            /* Improved resize handle with better visibility and positioning */
            .resize-handle {
                position: absolute;
                top: 0;
                right: -7px; /* Position it slightly outside the sidebar */
                width: 14px; /* Wider for easier grabbing */
                height: 100%;
                cursor: col-resize;
                z-index: 100; /* Ensure it's above other elements */
                background-color: transparent;
            }
            /* Visual indicator for the resize handle */
            .resize-handle::after {
                content: "";
                position: absolute;
                top: 0;
                left: 5px;
                width: 4px;
                height: 100%;
                background-color: #ddd;
                border-radius: 2px;
            }
            /* Enhanced visibility when hovering */
            .resize-handle:hover::after, .resize-handle.active::after {
                background-color: #0078d7;
                box-shadow: 0 0 4px rgba(0, 120, 215, 0.5);
            }
            .sidebar.resizing {
                user-select: none;
                pointer-events: none;
                border-right-color: #0078d7;
            }
            .main-content {
                flex: 1;
                padding: 1rem;
                overflow-y: auto;
                background-color: #ffffff;
                min-width: 30%;
            }
            .task-list { 
                margin: 1rem 0;
            }
            .task-item { 
                display: block; 
                padding: 0.5rem 1rem;
                margin: 0.25rem 0;
                border: 1px solid #ddd;
                border-radius: 4px;
                text-decoration: none;
                transition: background-color 0.2s;
                white-space: normal;
                overflow: hidden;
                font-size: 0.9rem;
                line-height: 1.5;
                min-height: 2em; /* Enough for at least one line */
                max-height: 6em; /* Limit to 4 lines of text */
                text-overflow: ellipsis;
                word-wrap: break-word;
                word-break: normal;
                background-color: white;
                color: #444;
                display: -webkit-box;
                -webkit-line-clamp: 4; /* Limit to 4 lines */
                -webkit-box-orient: vertical;
            }
            .task-item:hover { background-color: #f0f0f0; }
            .task-item.active {
                background-color: #e0e0ff;
                border-color: #9090ff;
            }
            /* Task title styling */
            .task-title {
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
                line-height: 1.3;
                max-height: 2.6em;
                overflow: hidden;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
            }
            /* Task content wrapper */
            .task-content-wrapper {
                width: 100%;
                padding: 0;
                margin: 0;
            }
            /* Full text box */
            .task-full-text {
                width: 100%;
                min-height: 100px;
                max-height: 200px;
                padding: 0.75rem;
                margin-bottom: 1rem;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #f8f8f8;
                overflow-y: auto;
                resize: vertical;
                font-size: 0.85rem;
                line-height: 1.4;
                white-space: pre-wrap;
                word-wrap: break-word;
                box-sizing: border-box;
            }
            .tab-container {
                display: flex;
                margin-bottom: 1rem;
                border-bottom: 1px solid #ddd;
                width: 100%;
            }
            .tab {
                padding: 0.5rem 1rem;
                margin-right: 0.5rem;
                border: 1px solid #ddd;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
                cursor: pointer;
                background-color: #f5f5f5;
            }
            .tab.active {
                background-color: #fff;
                border-bottom: 1px solid #fff;
                margin-bottom: -1px;
                font-weight: bold;
            }
            /* File content container */
            #file-content {
                background-color: #fff;
                color: #333;
                padding: 1rem;
                border-radius: 4px;
                overflow-x: hidden;
            }
            /* Message styling */
            .message {
                padding: 0.5rem 0.75rem;
                margin-bottom: 1rem;
                border-radius: 4px;
                border: 1px solid #ddd;
                background-color: #fff;
                color: #333;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            .user-message { border-left: 4px solid #4d7cc3; }
            .assistant-message { border-left: 4px solid #45a175; }
            .message-content {
                margin-top: 0.25rem;
                white-space: pre-wrap;
                overflow-wrap: break-word;
                word-break: break-word;
                max-width: 100%;
            }
            /* Json field styling */
            .json-field {
                margin-bottom: 0.1rem;
                padding: 0.1rem 0;
                border-bottom: 1px dashed #eee;
                line-height: 1.3;
            }
            .json-field:last-child {
                border-bottom: none;
            }
            .field-name {
                font-weight: bold;
                color: #555;
                margin-right: 0.3rem;
                display: inline-block;
                vertical-align: top;
            }
            .field-value {
                display: inline-block;
                color: #333;
                vertical-align: top;
            }
            .field-value-complex {
                margin-top: 0.1rem;
                margin-left: 0.75rem;
                padding: 0.25rem;
                background-color: #f9f9f9;
                border-radius: 3px;
                width: 100%;
                box-sizing: border-box;
                overflow-x: auto;
            }
            /* Long text display */
            .long-text {
                white-space: pre-wrap;
                word-wrap: break-word;
                word-break: break-word;
                font-family: monospace;
                font-size: 0.9em;
                line-height: 1.4;
                max-height: 300px;
                overflow-y: auto;
                padding: 0.5rem;
                background-color: #f9f9f9;
                border-radius: 3px;
                width: 100%;
                box-sizing: border-box;
            }
            /* Code blocks */
            pre {
                max-height: 400px;
                overflow: auto;
                background-color: #f5f5f5;
                border-radius: 3px;
                padding: 0.75rem;
                margin: 0.5rem 0;
                font-size: 0.9em;
                line-height: 1.4;
                width: 100%;
                box-sizing: border-box;
                white-space: pre-wrap;
            }
            .search-container { 
                margin-bottom: 1rem;
            }
            #search-input {
                width: 100%;
                padding: 0.5rem 1rem;
                margin: 0 0;
                border-radius: 4px;
                border: 1px solid #ddd;
                box-sizing: border-box;
                font-size: 0.9rem;
            }
            h1 { margin-top: 0; }
            h2 { margin-top: 0; font-size: 1.5rem; }
            .no-task-selected { 
                display: flex;
                justify-content: center;
                align-items: center;
                height: 50vh;
                color: #666;
            }
        """)
    )
)

# Add improved JavaScript for the resizable panels with more reliable resize handling
panel_resize_js = Script("""
    document.addEventListener('DOMContentLoaded', function() {
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main-content');
        const resizeHandle = document.getElementById('resize-handle');
        
        // Make resize handle take full height of sidebar
        setTimeout(() => {
            resizeHandle.style.height = sidebar.offsetHeight + 'px';
        }, 100);
        
        // State variables
        let isResizing = false;
        let startX = 0;
        let startWidth = 0;
        
        // Handle resize start with cursor anywhere on resize handle
        resizeHandle.addEventListener('mousedown', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            isResizing = true;
            startX = e.clientX;
            startWidth = sidebar.offsetWidth;
            
            // Add the active resize class
            sidebar.classList.add('resizing');
            resizeHandle.classList.add('active');
            
            // Prevent text selection during resize
            document.body.style.userSelect = 'none';
            document.body.style.cursor = 'col-resize';
        });
        
        // Drag events - also capture pointer events to improve reliability
        document.addEventListener('mousemove', handleResize);
        document.addEventListener('pointermove', handleResize);
        
        function handleResize(e) {
            if (!isResizing) return;
            
            // Calculate new width based on mouse movement
            const deltaX = e.clientX - startX;
            const newWidth = startWidth + deltaX;
            
            // Enforce min/max constraints
            if (newWidth >= 250 && newWidth <= window.innerWidth * 0.6) {
                sidebar.style.width = newWidth + 'px';
                mainContent.style.width = `calc(100% - ${newWidth}px)`;
            }
        }
        
        // End resize on mouse up anywhere in the document
        document.addEventListener('mouseup', endResize);
        document.addEventListener('pointerup', endResize);
        document.addEventListener('pointercancel', endResize);
        
        function endResize() {
            if (isResizing) {
                isResizing = false;
                sidebar.classList.remove('resizing');
                resizeHandle.classList.remove('active');
                document.body.style.userSelect = '';
                document.body.style.cursor = '';
                
                // Save the width preference
                localStorage.setItem('sidebarWidth', sidebar.style.width);
            }
        }
        
        // Handle window resize
        window.addEventListener('resize', function() {
            // Make sure resize handle takes full height
            resizeHandle.style.height = sidebar.offsetHeight + 'px';
            
            // Make sure sidebar doesn't exceed max width
            const maxWidth = window.innerWidth * 0.6;
            if (sidebar.offsetWidth > maxWidth) {
                sidebar.style.width = maxWidth + 'px';
                mainContent.style.width = `calc(100% - ${maxWidth}px)`;
            }
        });
        
        // Load saved width preference if available
        const savedWidth = localStorage.getItem('sidebarWidth');
        if (savedWidth && savedWidth.match(/^\\d+px$/)) {
            const numWidth = parseInt(savedWidth);
            if (numWidth >= 250 && numWidth <= window.innerWidth * 0.6) {
                sidebar.style.width = savedWidth;
                mainContent.style.width = `calc(100% - ${savedWidth})`;
            }
        }
    });
""")

def get_task_dirs():
    """Get all task directories sorted by modification time (newest first)"""
    if not TASKS_DIR.exists():
        return []
    
    tasks = []
    try:
        for item in TASKS_DIR.iterdir():
            if item.is_dir():
                # Get the modification time for sorting
                try:
                    mtime = item.stat().st_mtime
                    tasks.append((item.name, mtime))
                except Exception:
                    # If stat fails, still include but with old timestamp
                    tasks.append((item.name, 0))
    except Exception as e:
        # Handle permission errors or other issues
        print(f"Error scanning tasks directory: {e}")
        return []
    
    # Sort by modification time (newest first)
    tasks.sort(key=lambda x: x[1], reverse=True)
    return [t[0] for t in tasks]

def get_task_title(task_id):
    """Get the task title from the first entry in ui_messages.json"""
    task_dir = TASKS_DIR / task_id
    ui_file = task_dir / "ui_messages.json"
    
    default_title = f"Task: {task_id}"
    
    if not ui_file.exists():
        return default_title
    
    try:
        with open(ui_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, list) and data and isinstance(data[0], dict):
            # Look for text field in the first entry
            text_keys = ["text", "content", "message"]
            for key in text_keys:
                if key in data[0] and isinstance(data[0][key], str):
                    # Get a much longer title without truncation
                    title = data[0][key].strip()
                    # Only truncate extremely long titles
                    if len(title) > 300:
                        title = title[:297] + "..."
                    return title
                    
    except Exception as e:
        print(f"Error getting task title: {e}")
    
    return default_title

def fuzzy_match(text, query):
    """Word-component-based matching algorithm focused on semantic relevance"""
    if not query or not text:
        return False, 0
    
    # Normalize both query and text
    query = query.lower().strip()
    text = text.lower().strip()
    
    # Exact match has highest score
    if query == text:
        return True, 1.0
    
    # Contains full query is next best
    if query in text:
        return True, 0.95
    
    # Split into component words
    query_words = query.split()
    text_words = text.split()
    
    # If query is just one word
    if len(query_words) == 1:
        # Check for exact word match
        if query in text_words:
            return True, 0.9
        
        # Check for word prefix (starts with)
        for word in text_words:
            if word.startswith(query) and len(query) >= 3:
                # The longer the query, the higher the score
                return True, 0.7 + min(0.2, len(query) / len(word) * 0.2)
        
        # Check for substring in words (must be at least 4 chars to be meaningful)
        if len(query) >= 4:
            for word in text_words:
                if query in word and len(word) > len(query):
                    return True, 0.6
        
        # No meaningful match
        return False, 0
    
    # For multi-word queries, track how many query words match
    matched_words = 0
    partial_matches = 0
    
    for q_word in query_words:
        # Skip very short words (like "a", "of", etc.)
        if len(q_word) <= 2:
            continue
            
        word_matched = False
        
        # Check for exact word matches
        if q_word in text_words:
            matched_words += 1
            word_matched = True
            continue
        
        # Check for partial word matches (prefixes)
        for t_word in text_words:
            if t_word.startswith(q_word) and len(q_word) >= 3:
                partial_matches += 0.5
                word_matched = True
                break
        
        if word_matched:
            continue
            
        # If still no match, and the word is significant (4+ chars)
        # check if it appears as substring in any word
        if len(q_word) >= 4:
            for t_word in text_words:
                if q_word in t_word and len(t_word) > len(q_word):
                    partial_matches += 0.3
                    break
    
    # Calculate total number of significant words in query
    significant_words = sum(1 for w in query_words if len(w) > 2)
    
    if significant_words == 0:
        return False, 0
    
    # Calculate match score
    total_match = matched_words + partial_matches
    score = total_match / significant_words
    
    # Must match at least 50% of significant words to be considered a match
    if score < 0.5:
        return False, 0
        
    return True, min(score, 0.9)  # Cap at 0.9 for non-exact matches

def render_task_list(tasks, query="", selected_task=None):
    """Render the list of tasks, optionally filtered by query"""
    if query:
        # Fuzzy matching with scoring
        matched_tasks = []
        for task in tasks:
            title = get_task_title(task)
            is_match, score = fuzzy_match(title, query)
            if is_match:
                matched_tasks.append((task, score))
        
        # Sort by match score (best matches first)
        matched_tasks.sort(key=lambda x: x[1], reverse=True)
        tasks = [t[0] for t in matched_tasks]
    
    if not tasks:
        return [P("No tasks found.", cls="no-tasks")]
    
    task_items = []
    
    for task in tasks:
        title = get_task_title(task)
        is_active = task == selected_task
        active_class = " active" if is_active else ""
        
        task_items.append(
            A(
                title,
                hx_get=f"/load_task/{task}",
                hx_target="#task-content",
                hx_push_url=f"/task/{task}",
                cls=f"task-item{active_class}",
                id=f"task-{task}"
            )
        )
    
    return [Div(*task_items, cls="task-list")]

@rt
def index():
    """Home page with split layout"""
    tasks = get_task_dirs()
    
    return Titled(
        "Roo Task Browser",
        panel_resize_js,
        Div(
            # Left sidebar
            Div(
                H2("Search Tasks"),
                Div(
                    Input(
                        placeholder="Search tasks...",
                        id="search-input",
                        name="q",
                        hx_get=search,
                        hx_target="#tasks-container",
                        hx_trigger="keyup changed delay:300ms",
                    ),
                    cls="search-container"
                ),
                Div(
                    *render_task_list(tasks),
                    id="tasks-container"
                ),
                Div(cls="resize-handle", id="resize-handle"),  # Add resize handle element
                cls="sidebar"
            ),
            
            # Main content
            Div(
                Div(
                    H1("Roo Task Browser"),
                    P("Select a task from the sidebar to view its contents.", cls="no-task-selected"),
                    id="task-content"
                ),
                cls="main-content"
            ),
            
            cls="app-container"
        )
    )

@rt("/task/{tid}")
def task_route(tid: str):
    """Direct route to a specific task"""
    tasks = get_task_dirs()
    
    # Check if task exists
    task_dir = TASKS_DIR / tid
    if not task_dir.exists() or not task_dir.is_dir():
        return Titled(
            "Task Not Found",
            panel_resize_js,
            Div(
                # Left sidebar
                Div(
                    H2("Search Tasks"),
                    Div(
                        Input(
                            placeholder="Search tasks...",
                            id="search-input",
                            name="q",
                            hx_get=search,
                            hx_target="#tasks-container",
                            hx_trigger="keyup changed delay:300ms",
                        ),
                        cls="search-container"
                    ),
                    Div(
                        *render_task_list(tasks),
                        id="tasks-container"
                    ),
                    Div(cls="resize-handle", id="resize-handle"),  # Add resize handle element
                    cls="sidebar"
                ),
                
                # Main content
                Div(
                    H1("Task Not Found"),
                    P(f"Task '{tid}' not found."),
                    cls="main-content"
                ),
                
                cls="app-container"
            )
        )
    
    # Redirect to index with the task loaded via HTMX
    return index()

@rt
def search(q: str = ""):
    """Search tasks and return filtered list"""
    tasks = get_task_dirs()
    return Div(*render_task_list(tasks, q), id="tasks-container")

@rt("/load_task/{tid}")
def load_task(tid: str):
    """Load a task and show its content"""
    task_dir = TASKS_DIR / tid
    
    if not task_dir.exists() or not task_dir.is_dir():
        return Div(
            H1("Task Not Found"),
            P(f"Task '{tid}' not found.")
        )
    
    # Check which files exist
    ui_file = task_dir / "ui_messages.json"
    api_file = task_dir / "api_conversation_history.json"
    
    ui_exists = ui_file.exists()
    api_exists = api_file.exists()
    
    # Get task title
    title = get_task_title(tid)
    
    # Get the full text of the first message for the text box
    full_text = ""
    if ui_exists:
        try:
            with open(ui_file, 'r', encoding='utf-8') as f:
                ui_data = json.load(f)
                if isinstance(ui_data, list) and ui_data and isinstance(ui_data[0], dict):
                    for key in ["text", "content", "message"]:
                        if key in ui_data[0] and isinstance(ui_data[0][key], str):
                            full_text = ui_data[0][key].strip()
                            break
        except Exception as e:
            print(f"Error loading task text: {e}")
    
    # Default to ui_messages.json content
    content = None
    if ui_exists:
        content = load_file_content(tid, "ui_messages")
    elif api_exists:
        content = load_file_content(tid, "api_conversation_history")
    
    return Div(
        # Title limited to 2 lines
        H1(title, cls="task-title"),
        
        # Task content wrapper for proper alignment
        Div(
            # Full text box (resizable and scrollable)
            Div(
                full_text, 
                cls="task-full-text"
            ),
            
            # Tabs for switching between files
            Div(
                Button(
                    "UI Messages", 
                    hx_get=f"/task/{tid}/ui_messages",
                    hx_target="#file-content",
                    disabled=not ui_exists,
                    cls=f"tab{' active' if ui_exists else ''}"
                ),
                Button(
                    "API Conversation History", 
                    hx_get=f"/task/{tid}/api_conversation_history",
                    hx_target="#file-content",
                    disabled=not api_exists,
                    cls=f"tab{' active' if not ui_exists and api_exists else ''}"
                ),
                cls="tab-container"
            ),
            
            # File content area
            Div(
                content if content else P("No content available for this task."),
                id="file-content"
            ),
            
            cls="task-content-wrapper"
        )
    )

def load_file_content(tid, file_type):
    """Helper to load and render file content"""
    task_dir = TASKS_DIR / tid
    file_path = task_dir / f"{file_type}.json"
    
    if not file_path.exists():
        return P(f"File not found: {file_type}.json")
    
    try:
        # Load JSON content
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Render based on file type
        return render_messages(data, file_type)
        
    except json.JSONDecodeError:
        return Div(
            P(f"Error: Invalid JSON in {file_type}.json"),
            Pre(file_path.read_text(encoding='utf-8', errors='replace'))
        )
    except Exception as e:
        return Div(P(f"Error loading file: {str(e)}"))

def format_message_content(content):
    """Format message content with markdown rendering if needed"""
    # Check if content looks like markdown (contains common markdown characters)
    if not isinstance(content, str):
        return P(str(content), cls="message-content")

    # Try to detect JSON content (starts with { and ends with })
    if (content.strip().startswith('{') and content.strip().endswith('}')) or \
       (content.strip().startswith('[') and content.strip().endswith(']')):
        try:
            # Try to parse as JSON
            json_obj = json.loads(content)
            
            # Create a structured view of the JSON
            fields = []
            
            # For object types, extract each field
            if isinstance(json_obj, dict):
                for key, value in json_obj.items():
                    # Create a field renderer for this component
                    field = render_field(key, value)
                    if field is not None:
                        fields.append(field)
                        
                return Div(*fields, cls="message-content")
            elif isinstance(json_obj, list):
                # For arrays, create a structured list
                items = []
                for i, item in enumerate(json_obj):
                    items.append(H5(f"Item {i+1}:", style="margin: 0.2rem 0 0.1rem 0; padding: 0;"))
                    if isinstance(item, dict):
                        for key, value in item.items():
                            field = render_field(key, value)
                            if field is not None:
                                items.append(field)
                    else:
                        items.append(Pre(Code(json.dumps(item, indent=2), cls="language-json")))
                return Div(*items, cls="message-content")
        except json.JSONDecodeError:
            # Not valid JSON, continue with normal processing
            pass
    
    md_indicators = ['#', '```', '*', '_', '- ', '1. ', '|', '[', '![']
    is_markdown = any(indicator in content for indicator in md_indicators)
    
    if is_markdown:
        # Render as markdown
        return Div(content, cls="marked message-content")
    else:
        # Plain text
        return P(content, cls="message-content")

def render_field(name, value):
    """Render a single JSON field with proper formatting"""
    # Skip empty image arrays
    if name == "images" and isinstance(value, list) and len(value) == 0:
        return None
        
    if isinstance(value, (dict, list)):
        # Skip rendering if it's an empty list or dict
        if (isinstance(value, list) and len(value) == 0) or (isinstance(value, dict) and len(value) == 0):
            return Div(
                Span(name + ":", cls="field-name"),
                Span("(empty)", cls="field-value"),
                cls="json-field"
            )
            
        # Complex value (dict or list)
        try:
            # Special case for important fields that we want to extract into components
            if name in ["request", "content"] and isinstance(value, dict):
                # Extract component fields
                fields = []
                fields.append(Div(name + ":", cls="field-name", style="font-weight: bold; margin-bottom: 0.3rem;"))
                
                # Render each field in the nested object
                for key, nested_value in value.items():
                    # Use indentation to show hierarchy
                    nested_field = render_field(key, nested_value)
                    if nested_field is not None:
                        fields.append(Div(nested_field, style="margin-left: 1rem;"))
                        
                return Div(*fields, cls="json-field")
                
            # Try to handle the special content case for better readability
            if name == "content" and isinstance(value, str) and len(value) > 80:
                # Special handling for long content strings
                return Div(
                    Div(name + ":", cls="field-name"),
                    Div(value, cls="long-text"),
                    cls="json-field"
                )
                
            # Format the JSON for better readability
            if name == "request" or name == "content":
                # Special fields we want to extract components from
                if isinstance(value, dict):
                    fields = []
                    fields.append(Div(name + ":", cls="field-name", style="font-weight: bold; margin-bottom: 0.3rem;"))
                    
                    # Render each field in the dictionary
                    for key, nested_value in value.items():
                        nested_field = render_field(key, nested_value)
                        if nested_field is not None:
                            fields.append(Div(nested_field, style="margin-left: 1rem;"))
                            
                    return Div(*fields, cls="json-field")
                    
            # Default JSON rendering for other complex types
            pretty_value = json.dumps(value, indent=2, ensure_ascii=False)
            return Div(
                Div(name + ":", cls="field-name"),
                Div(
                    Pre(Code(pretty_value, cls="language-json")),
                    cls="field-value-complex"
                ),
                cls="json-field"
            )
        except Exception:
            # Fallback to simple display if JSON formatting fails
            return Div(
                Span(name + ":", cls="field-name"),
                Span(str(value)[:100] + ("..." if len(str(value)) > 100 else ""), cls="field-value"),
                cls="json-field"
            )
    elif isinstance(value, str):
        if len(value) > 80:
            # Long string with special formatting
            return Div(
                Div(name + ":", cls="field-name"),
                Div(value, cls="long-text"),
                cls="json-field"
            )
        else:
            # Simple string value (less than 80 chars)
            return Div(
                Span(name + ":", cls="field-name"),
                Span(value, cls="field-value"),
                cls="json-field"
            )
    else:
        # Simple non-string value
        return Div(
            Span(name + ":", cls="field-name"),
            Span(str(value), cls="field-value"),
            cls="json-field"
        )

def render_messages(data, file_type):
    """Render messages from JSON data with improved formatting"""
    result = []
    
    # Check if this is a list-like structure with messages
    if isinstance(data, list) and data and isinstance(data[0], dict):
        # Iterate through each item in the list
        for i, msg in enumerate(data):
            # Determine message class based on role/sender field
            role_key = next((k for k in ["role", "sender", "from"] if k in msg), None)
            role = msg.get(role_key, "unknown").lower() if role_key else "unknown"
            msg_class = "user-message" if "user" in role else "assistant-message"
            
            # Extract primary content if available
            content_key = next((k for k in ["content", "message", "text"] if k in msg), None)
            content = msg.get(content_key) if content_key else None
            
            # Start building fields
            fields = []
            
            # Message index/position with minimal vertical space
            fields.append(H4(f"Message {i+1}: {role.capitalize()}", style="margin: 0.15rem 0; padding: 0;"))
            
            # Render each field in the message object
            for key, value in msg.items():
                # Skip the primary content as we'll show it specially below
                if content_key and key == content_key:
                    continue
                
                # Don't add empty images field
                field = render_field(key, value)
                if field is not None:
                    fields.append(field)
            
            # Add the primary content last if it exists
            if content_key and content:
                fields.append(
                    Div(
                        H5("Content:", style="margin: 0.2rem 0 0.1rem 0; padding: 0;"),
                        format_message_content(content),
                        cls="message-content"
                    )
                )
            
            # Add the complete message div (filter out None values)
            result.append(
                Div(
                    *[f for f in fields if f is not None],
                    cls=f"message {msg_class}"
                )
            )
    
    # If we couldn't render as messages or if there were no messages
    if not result:
        # Format JSON as structured elements
        if isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, dict):
                    fields = [H4(f"Item {i+1}", style="margin: 0.15rem 0; padding: 0;")]
                    for key, value in item.items():
                        field = render_field(key, value)
                        if field is not None:
                            fields.append(field)
                    result.append(Div(*fields, cls="message"))
                else:
                    result.append(
                        Div(
                            H4(f"Item {i+1}", style="margin: 0.15rem 0; padding: 0;"),
                            Pre(Code(json.dumps(item, indent=2), cls="language-json")),
                            cls="message"
                        )
                    )
        elif isinstance(data, dict):
            fields = [H4("JSON Object", style="margin: 0.15rem 0; padding: 0;")]
            for key, value in data.items():
                field = render_field(key, value)
                if field is not None:
                    fields.append(field)
            result.append(Div(*fields, cls="message"))
        else:
            # Fallback for other types
            pretty_json = json.dumps(data, indent=2, ensure_ascii=False)
            result = [Pre(Code(pretty_json, cls="language-json"))]
    
    return Div(*result)

@rt("/task/{tid}/{file}")
def view(tid: str, file: str):
    """View a specific JSON file from a task"""
    # Validate file parameter
    if file not in ["ui_messages", "api_conversation_history"]:
        return Div(P(f"Invalid file type: {file}"))
    
    return load_file_content(tid, file)

# Start the server
if __name__ == "__main__":
    print(f"Scanning tasks in: {TASKS_DIR}")
    serve(port=5001)
else:
    # When imported
    serve()