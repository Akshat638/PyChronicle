"""
PyChronicle - Storage Schema (Week 1)

Stores the chronological variable-state deltas captured by the tracer.
Schema: (id, timestamp, line_number, variable_name, serialized_value)
"""

import sqlite3
import time

DB_NAME = "pychronicle.db"


def init_db():
    """Create the execution_history table if it doesn't already exist."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            line_number INTEGER,
            variable_name TEXT,
            serialized_value TEXT
        )
    """)
    connection.commit()
    connection.close()
    print("Database initialized successfully!")


def save_execution(line_number, variable_name, serialized_value):
    """Insert a single variable-state snapshot into the history table."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO execution_history
           (timestamp, line_number, variable_name, serialized_value)
           VALUES (?, ?, ?, ?)""",
        (time.time(), line_number, variable_name, serialized_value),
    )
    connection.commit()
    connection.close()


def fetch_all_history():
    """Return every recorded snapshot in chronological order."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM execution_history ORDER BY id ASC")
    rows = cursor.fetchall()
    connection.close()
    return rows


def clear_history():
    """Wipe previous run history so each trace starts clean."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM execution_history")
    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
