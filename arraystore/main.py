# main.py

import sqlite3
import json

def create_array_table(conn):
    """Create table and indexes to store array elements."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS array_elements (
            array_hash TEXT NOT NULL,
            element_index INTEGER NOT NULL,
            element_value TEXT,
            PRIMARY KEY (array_hash, element_index)
        );
    """)
    # Index on array_hash for faster lookups (optional since PK index exists)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_array_elements_hash ON array_elements(array_hash);"
    )
    conn.commit()

def insert_array(conn, array_hash, array):
    """Insert array into table using json.dumps to preserve types."""
    cur = conn.cursor()
    for idx, val in enumerate(array):
        # Store JSON literal representation
        value = 'null' if val is None else json.dumps(val)
        cur.execute(
            "INSERT OR REPLACE INTO array_elements (array_hash, element_index, element_value) VALUES (?, ?, ?)",
            (array_hash, idx, value)
        )
    conn.commit()

def retrieve_array(conn, array_hash):
    """Retrieve array as Python list with preserved types."""
    cur = conn.cursor()
    cur.execute("""
        SELECT '[' || GROUP_CONCAT(element_value, ',') || ']' AS json_array
        FROM array_elements
        WHERE array_hash = ?
        GROUP BY array_hash;
    """, (array_hash,))
    row = cur.fetchone()
    return json.loads(row['json_array']) if row else []
