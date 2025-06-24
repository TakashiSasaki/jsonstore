# main.py

import sqlite3
import json
import hashlib


def _canonical_json(obj) -> str:
    """Return JSON canonical form used for hashing."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

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


def insert_array_auto_hash(conn, array, table_name: str = "arraystore"):
    """Insert array and compute canonical JSON SHA1 internally.

    Parameters
    ----------
    conn : sqlite3.Connection
        SQLite connection.
    array : list
        Array to store.
    table_name : str, optional
        Name of the table. Defaults to ``"arraystore"``.

    Returns
    -------
    str
        The computed SHA1 hash of the canonical JSON representation.
    """

    canonical_json = _canonical_json(array)
    canonical_json_sha1 = hashlib.sha1(canonical_json.encode("utf-8")).hexdigest()
    insert_array(conn, canonical_json_sha1, array, table_name=table_name)
    return canonical_json_sha1

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
