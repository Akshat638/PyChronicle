"""
PyChronicle - Execution Engine (Week 2)

Uses sys.settrace to watch a target script run line-by-line, capturing
every local variable's value at every line and persisting it to SQLite
via database.db.save_execution().
"""

import sys
import time

from database.db import init_db, clear_history, save_execution

# Names that show up in local scope but aren't "real" user variables
IGNORED_NAMES = {"sys", "trace", "file", "code", "execution_history"}

execution_history = []
_target_file = None


def _trace_calls(frame, event, arg):
    if event != "line":
        return _trace_calls

    filename = frame.f_code.co_filename
    if _target_file and _target_file not in filename:
        return _trace_calls

    line_no = frame.f_lineno

    for key, value in frame.f_locals.items():
        if key.startswith("__") or key in IGNORED_NAMES:
            continue

        try:
            serialized_value = repr(value)
        except Exception:
            serialized_value = "<unserializable>"

        entry = {
            "line": line_no,
            "variable": key,
            "value": serialized_value,
            "timestamp": time.time(),
        }
        execution_history.append(entry)
        save_execution(line_no, key, serialized_value)

    return _trace_calls


def run_and_trace(filepath):
    """Execute `filepath` under sys.settrace and return the full,
    in-memory list of captured variable-state snapshots."""
    global _target_file

    _target_file = filepath
    init_db()
    clear_history()
    execution_history.clear()

    with open(filepath, "r") as f:
        source = f.read()
    code = compile(source, filepath, "exec")

    sys.settrace(_trace_calls)
    try:
        exec(code, {"__name__": "__main__"})
    finally:
        sys.settrace(None)

    return execution_history


if __name__ == "__main__":
    import os

    sample_path = os.path.join(os.path.dirname(__file__), "..", "sample", "test.py")
    history = run_and_trace(sample_path)
    print(f"\nCaptured {len(history)} variable state snapshots.")
