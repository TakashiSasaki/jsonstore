# main.py

import sqlite3
import json

def create_array_table(conn, table_name: str = "array_elements"):
    """Create table and indexes to store array elements.

    Parameters
    ----------
    conn : sqlite3.Connection
        SQLite connection.
    table_name : str, optional
        Name of the table to create. Defaults to ``"array_elements"``.
    """

    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            array_hash TEXT NOT NULL,
            element_index INTEGER NOT NULL,
            element_json TEXT,
            PRIMARY KEY (array_hash, element_index)
        );
    """)
    # Index on array_hash for faster lookups (optional since PK index exists)
    conn.execute(
        f"CREATE INDEX IF NOT EXISTS idx_{table_name}_hash ON {table_name}(array_hash);"
    )
    conn.commit()

def insert_array(conn, array_hash, array, table_name: str = "array_elements"):
    """Insert array into table using json.dumps to preserve types."""
    cur = conn.cursor()
    for idx, val in enumerate(array):
        # Store JSON literal representation
        value = 'null' if val is None else json.dumps(val)
        cur.execute(
            f"INSERT OR REPLACE INTO {table_name} (array_hash, element_index, element_json) VALUES (?, ?, ?)",
            (array_hash, idx, value)
        )
    conn.commit()

def retrieve_array(conn, array_hash, table_name: str = "array_elements"):
    """Retrieve array as Python list with preserved types."""
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT '[' || GROUP_CONCAT(element_json, ',') || ']' AS json_array
        FROM {table_name}
        WHERE array_hash = ?
        GROUP BY array_hash;
    """,
        (array_hash,),
    )
    row = cur.fetchone()
    return json.loads(row['json_array']) if row else []
