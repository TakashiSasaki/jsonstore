# main.py

import sqlite3
import json

def create_array_table(conn, table_name: str = "arraystore"):
    """Create table and indexes to store array elements.

    Parameters
    ----------
    conn : sqlite3.Connection
        SQLite connection.
    table_name : str, optional
        Name of the table to create. Defaults to ``"arraystore"``.
    """

    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            canonical_json_sha1 TEXT NOT NULL,
            element_index INTEGER NOT NULL,
            element_json TEXT,
            PRIMARY KEY (canonical_json_sha1, element_index)
        );
    """)
    # Index on canonical_json_sha1 for faster lookups (optional since PK index exists)
    conn.execute(
        f"CREATE INDEX IF NOT EXISTS idx_{table_name}_hash ON {table_name}(canonical_json_sha1);"
    )
    conn.commit()

def insert_array(conn, canonical_json_sha1, array, table_name: str = "arraystore"):
    """Insert array into table using json.dumps to preserve types."""
    cur = conn.cursor()
    for idx, val in enumerate(array):
        # Store JSON literal representation
        value = 'null' if val is None else json.dumps(val)
        cur.execute(
            f"INSERT OR REPLACE INTO {table_name} (canonical_json_sha1, element_index, element_json) VALUES (?, ?, ?)",
            (canonical_json_sha1, idx, value)
        )
    conn.commit()

def retrieve_array(conn, canonical_json_sha1, table_name: str = "arraystore"):
    """Retrieve array as Python list with preserved types."""
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT '[' || GROUP_CONCAT(element_json, ',') || ']' AS json_array
        FROM {table_name}
        WHERE canonical_json_sha1 = ?
        GROUP BY canonical_json_sha1;
    """,
        (canonical_json_sha1,),
    )
    row = cur.fetchone()
    return json.loads(row['json_array']) if row else []
