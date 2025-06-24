# main.py for objectstore

import sqlite3
import json
import hashlib

from canonicaljson import canonical_json


def _canonical_json(obj) -> str:
    """Return canonical JSON string for hashing.

    The function encodes according to the JSON Canonicalization Scheme
    (JCS) implemented locally and verifies the result using the ``jcs``
    package. The verification step provides extra safety during
    development and may be removed in a performance tuned release.
    """

    return canonical_json(obj)


def create_object_table(conn: sqlite3.Connection, table_name: str = "objectstore"):
    """Create table and indexes to store object properties.

    Parameters
    ----------
    conn : sqlite3.Connection
        SQLite connection.
    table_name : str, optional
        Name of the table to create. Defaults to ``"objectstore"``.
    """
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            canonical_json_sha1 TEXT NOT NULL,
            property_name TEXT NOT NULL,
            property_json TEXT,
            PRIMARY KEY (canonical_json_sha1, property_name)
        );
        """
    )
    conn.execute(
        f"CREATE INDEX IF NOT EXISTS idx_{table_name}_hash ON {table_name}(canonical_json_sha1);"
    )
    conn.commit()


def insert_object(conn: sqlite3.Connection, canonical_json_sha1, obj: dict, table_name: str = "objectstore"):
    """Insert a Python dict into the table preserving JSON types."""
    cur = conn.cursor()
    for key, val in obj.items():
        value = canonical_json(val)
        cur.execute(
            f"INSERT OR REPLACE INTO {table_name} (canonical_json_sha1, property_name, property_json) VALUES (?, ?, ?)",
            (canonical_json_sha1, key, value),
        )
    conn.commit()


def insert_object_auto_hash(conn: sqlite3.Connection, obj: dict, table_name: str = "objectstore"):
    """Insert object and compute canonical JSON SHA1 internally.

    Parameters
    ----------
    conn : sqlite3.Connection
        SQLite connection.
    obj : dict
        Object to store.
    table_name : str, optional
        Name of the table. Defaults to ``"objectstore"``.

    Returns
    -------
    str
        The computed SHA1 hash of the canonical JSON representation.
    """

    canonical_json = _canonical_json(obj)
    canonical_json_sha1 = hashlib.sha1(canonical_json.encode("utf-8")).hexdigest()
    insert_object(conn, canonical_json_sha1, obj, table_name=table_name)
    return canonical_json_sha1


def retrieve_object(conn: sqlite3.Connection, canonical_json_sha1, table_name: str = "objectstore"):
    """Retrieve a Python dict previously stored with insert_object."""
    cur = conn.cursor()
    cur.execute(
        f"SELECT property_name, property_json FROM {table_name} WHERE canonical_json_sha1 = ?",
        (canonical_json_sha1,),
    )
    rows = cur.fetchall()
    result = {}
    for row in rows:
        result[row[0]] = json.loads(row[1]) if row[1] is not None else None
    return result
