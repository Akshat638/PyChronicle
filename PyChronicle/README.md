# PyChronicle - AST-Powered Time-Travel Debugger

**Scope of this build: Week 1 + Week 2 only** (per the Project 1 plan).

## What's included

### Week 1
- `parser/ast_parser.py` — Parses a target Python file's Abstract Syntax
  Tree and identifies every variable assignment (name, line, value),
  without executing the code.
- `database/db.py` — SQLite storage schema: `(id, timestamp, line_number,
  variable_name, serialized_value)`, with `init_db`, `save_execution`,
  `fetch_all_history`, and `clear_history` helpers.

### Week 2
- `tracer/execution_tracer.py` — Uses `sys.settrace` to record the
  execution flow of the target script, capturing every variable's state
  at every line and saving it to SQLite.
- `ui/app.py` — Textual TUI scaffold: a code-view pane and a timeline
  pane, with left/right key bindings stubbed in. Actual DB-backed
  scrubbing and code highlighting are Week 3 work.

### Supporting files
- `sample/test.py` — Small script used to test the parser and tracer.
- `main.py` — CLI entry point tying the AST parser and tracer together.

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

## Running Week 1 (AST parsing only)

```bash
python -m parser.ast_parser
```

Prints every variable assignment found in `sample/test.py` as JSON.

## Running Week 2 (tracer + storage)

```bash
python main.py sample/test.py --show-ast
```

This will:
1. Print the statically-detected assignments (Week 1 AST parser).
2. Run `sample/test.py` under `sys.settrace`, capturing every variable's
   value at every executed line.
3. Save every snapshot into `pychronicle.db` (created automatically).

You can inspect the results directly:

```bash
python -c "from database.db import fetch_all_history; [print(r) for r in fetch_all_history()]"
```

## Launching the Week 2 TUI scaffold

```bash
python ui/app.py
```

Shows the two-pane layout (code view + timeline). Use ← / → — the step
counter updates, proving the scaffold and bindings work. Actually
reading from `pychronicle.db` and highlighting source lines is Week 3.

## Project structure

```
PyChronicle/
├── database/
│   └── db.py
├── parser/
│   └── ast_parser.py
├── tracer/
│   └── execution_tracer.py
├── ui/
│   └── app.py
├── sample/
│   └── test.py
├── main.py
├── requirements.txt
└── README.md
```
