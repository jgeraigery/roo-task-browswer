Roo Task Browser - FastHTML Application
======================================

High-Level Requirements Recap
-----------------------------

• List every task directory found under  
  `~/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/tasks`  
• Enable live search / filter of that list.  
• When a task is selected, allow viewing either

  - `ui_messages.json`
  - `api_conversation_history.json`

• Render the chosen file nicely:

  - Pretty-printed JSON with syntax highlighting.  
  - If Markdown strings exist inside the JSON (e.g. message content), render them as HTML with code highlighting.

FastHTML-Specific Design
------------------------

FastHTML strengths to leverage

* Decorator routing (`rt`) – very concise.  
* HTMX support – use `hx_get` for partial updates (search filtering & file switching).  
* Built-in `MarkdownJS()` and `HighlightJS()` helpers – no-config markup & code rendering.  
* FT components keep templates 100 % in Python.

Key FastHTML utilities we’ll use

* `fast_app()` – create `(app, rt)` pair.  
* `Titled()` – consistent page titles.  
* Optional `Beforeware` in future.

Routes & Flow
-------------

```
index()  ─ GET "/"  ───────────────────────►  List of tasks
              ▲  hx_get "/search" (query)  │  (Client types)  
task()   ─ GET "/task/{tid}" ──────────────►  Overview / tabs  
view()   ─ GET "/task/{tid}/{file}" ───────►  JSON+markdown render (partial)  
────────────────────────────────────────────┘
```

Mermaid diagram:

```mermaid
flowchart TD
  A[/Tasks dir scan/] -->|list| B[index /]
  B -->|click task row| C[task /task/{tid}]
  C -->|hx_get ui_messages| D[view /task/{tid}/ui_messages]
  C -->|hx_get api_history| E[view /task/{tid}/api_conversation_history]
  B -. hx_get search .-> B
```

Detailed Implementation Steps
-----------------------------

1. **Bootstrap**

   ```python
   from fasthtml.common import *
   TASKS_DIR = Path.home()/'Library/Application Support/Code/User/' \
               'globalStorage/rooveterinaryinc.roo-cline/tasks'
   app, rt = fast_app(
       hdrs=(MarkdownJS(), HighlightJS(langs=['json','python','markdown']))
   )
   ```

2. **Route: `index()`**

   * Scan `TASKS_DIR` for sub-directories.  
   * Return:

     ```python
     Titled("Roo Tasks",
       Input(placeholder="Search…", id="q",
             hx_get=search, hx_target="#tasks",
             hx_trigger="keyup changed delay:300ms"),
       Div(id="tasks", *_render_task_list(tasks))
     )
     ```

3. **Route: `search(q:str="")`**

   * Filter dir names with simple substring match.  
   * Return only the tasks list partial for HTMX swap.

4. **Route: `task(tid:str)`**

   * Validate directory exists.  
   * Return task page with two buttons:

     ```python
     Titled(f"Task {tid}",
       Button("UI Messages",
              hx_get=view.to(tid=tid, file="ui_messages"),
              hx_target="#viewer"),
       Button("API History",
              hx_get=view.to(tid=tid, file="api_conversation_history"),
              hx_target="#viewer"),
       Div(id="viewer")
     )
     ```

5. **Route: `view(tid:str, file:str)`**

   * Load the chosen JSON.  
   * Pretty-print:

     ```python
     pretty = json.dumps(data, indent=2, ensure_ascii=False)
     return Pre(Code(pretty, cls="language-json"))
     ```

   * Optional enrichment: detect messages list and render markdown for `"content"` values.

6. **Static / Style**

   * Pico CSS defaults.  
   * Optional custom small CSS via `Style()`.

7. **Run**

   * `serve(port=5001)` (default) → `http://localhost:5001`

Future Enhancements
-------------------

* Keyboard navigation.  
* Cache task list.  
* Download raw JSON.  
* Toast notifications on errors.  
* Dockerfile.

File & Dir Structure
--------------------

```
roo-task-browser/
└─ app/
   └─ main.py         # all FastHTML code
```

Validation & Testing
--------------------

* Unit: starlette.testclient.  
* Manual: run app and browse.  
* Edge cases: missing files.

---

Next Steps
----------

1. Implement the application in Code mode.  
2. Run and verify.

---