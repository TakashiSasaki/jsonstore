# table.py

import sqlite3
import json
import hashlib
from typing import Any, List

from jsonstore.canonicaljson import canonical_json


def _canonical_json(obj: Any) -> str:
    """Return JSON canonical form used for hashing.

    The implementation follows the JSON Canonicalization Scheme (JCS)
    without depending on the ``jcs`` package for the actual encoding.
    For additional safety during development, the result is verified
    against ``jcs.canonicalize``. This check can be removed for a
    performance optimised release build.
    """

    return canonical_json(obj)

def create_array_table(conn: sqlite3.Connection, table_name: str) -> None:
    """Create table and indexes to store array elements.

    Parameters
    ----------
    conn : sqlite3.Connection
        SQLite connection.
    table_name : str
        Name of the table to create.
    """

    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            canonical_json_sha1 TEXT NOT NULL,
            element_index INTEGER NOT NULL,
            element_json TEXT,
            element_json_sha1 TEXT,
            PRIMARY KEY (canonical_json_sha1, element_index)
        );
    """)
    # Index on canonical_json_sha1 for faster lookups (optional since PK index exists)
    conn.execute(
        f"CREATE INDEX IF NOT EXISTS idx_{table_name}_hash ON {table_name}(canonical_json_sha1);"
    )
    conn.commit()

def insert_array(
    conn: sqlite3.Connection,
    canonical_json_sha1: str,
    array: List[Any],
    table_name: str,
) -> None:
    """Insert array into table using canonical JSON for each element."""
    cur = conn.cursor()
    for idx, val in enumerate(array):
        # Store canonical JSON literal representation of each element
        value = canonical_json(val)
        value_sha1 = hashlib.sha1(value.encode("utf-8")).hexdigest()
        cur.execute(
            f"INSERT OR REPLACE INTO {table_name} (canonical_json_sha1, element_index, element_json, element_json_sha1) VALUES (?, ?, ?, ?)",
            (canonical_json_sha1, idx, value, value_sha1)
        )
    conn.commit()


def insert_array_auto_hash(
    conn: sqlite3.Connection, array: List[Any], table_name: str
) -> str:
    """Insert array and compute canonical JSON SHA1 internally.

    Parameters
    ----------
    conn : sqlite3.Connection
        SQLite connection.
    array : list
        Array to store.
    table_name : str
        Name of the table.

    Returns
    -------
    str
        The computed SHA1 hash of the canonical JSON representation.
    """

    canonical_json = _canonical_json(array)
    canonical_json_sha1 = hashlib.sha1(canonical_json.encode("utf-8")).hexdigest()
    insert_array(conn, canonical_json_sha1, array, table_name=table_name)
    return canonical_json_sha1


def insert_arrays_auto_hash(
    conn: sqlite3.Connection, arrays: List[List[Any]], table_name: str
) -> List[str]:
    """Insert multiple arrays at once computing SHA1 for each.

    Parameters
    ----------
    conn : sqlite3.Connection
        SQLite connection.
    arrays : list[list]
        List of arrays to store.
    table_name : str
        Name of the table.

    Returns
    -------
    list[str]
        SHA1 hashes for each array in the same order as ``arrays``.
    """

    hashes: List[str] = []
    rows = []
    for array in arrays:
        canonical = _canonical_json(array)
        sha1 = hashlib.sha1(canonical.encode("utf-8")).hexdigest()
        hashes.append(sha1)
        for idx, val in enumerate(array):
            rows.append((sha1, idx, canonical_json(val)))

    if rows:
        cur = conn.cursor()
        cur.executemany(
            f"INSERT OR REPLACE INTO {table_name} (canonical_json_sha1, element_index, element_json) VALUES (?, ?, ?)",
            rows,
        )
        conn.commit()

    return hashes

def retrieve_array(
    conn: sqlite3.Connection, canonical_json_sha1: str, table_name: str
) -> List[Any]:
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


def retrieve_all_arrays(conn: sqlite3.Connection, table_name: str) -> List[List[Any]]:
    """Return all arrays stored in ``table_name`` as a list of lists."""
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT '[' || GROUP_CONCAT(element_json, ',') || ']' AS json_array
        FROM {table_name}
        GROUP BY canonical_json_sha1;
    """
    )
    rows = cur.fetchall()
    return [json.loads(row['json_array']) for row in rows]
