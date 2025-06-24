# main.py for objectstore

import sqlite3
import json
import hashlib
from typing import Any, Dict, List

from sqlite_store.canonicaljson import canonical_json


def _canonical_json(obj: Any) -> str:
    """Return canonical JSON string for hashing.

    The function encodes according to the JSON Canonicalization Scheme
    (JCS) implemented locally and verifies the result using the ``jcs``
    package. The verification step provides extra safety during
    development and may be removed in a performance tuned release.
    """

    return canonical_json(obj)


def create_object_table(conn: sqlite3.Connection, table_name: str = "objectstore") -> None:
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
            property_json_sha1 TEXT,
            PRIMARY KEY (canonical_json_sha1, property_name)
        );
        """
    )
    conn.execute(
        f"CREATE INDEX IF NOT EXISTS idx_{table_name}_hash ON {table_name}(canonical_json_sha1);"
    )
    conn.commit()


def insert_object(
    conn: sqlite3.Connection,
    canonical_json_sha1: str,
    obj: Dict[str, Any],
    table_name: str = "objectstore",
) -> None:
    """Insert a Python dict into the table preserving JSON types."""
    cur = conn.cursor()
    for key, val in obj.items():
        value = canonical_json(val)
        value_sha1 = hashlib.sha1(value.encode("utf-8")).hexdigest()
        cur.execute(
            f"INSERT OR REPLACE INTO {table_name} (canonical_json_sha1, property_name, property_json, property_json_sha1) VALUES (?, ?, ?, ?)",
            (canonical_json_sha1, key, value, value_sha1),
        )
    conn.commit()


def insert_object_auto_hash(
    conn: sqlite3.Connection,
    obj: Dict[str, Any],
    table_name: str = "objectstore",
) -> str:
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


def insert_objects_auto_hash(
    conn: sqlite3.Connection,
    objs: List[Dict[str, Any]],
    table_name: str = "objectstore",
) -> List[str]:
    """Insert multiple objects computing canonical JSON SHA1 for each.

    Parameters
    ----------
    conn : sqlite3.Connection
        SQLite connection.
    objs : list of dict
        Objects to store.
    table_name : str, optional
        Name of the table. Defaults to ``"objectstore"``.

    Returns
    -------
    list of str
        SHA1 hashes for the canonical JSON of each object, in input order.
    """

    hashes: List[str] = []
    cur = conn.cursor()
    insert_sql = (
        f"INSERT OR REPLACE INTO {table_name} (canonical_json_sha1, property_name, property_json)"
        f" VALUES (?, ?, ?)"
    )
    for obj in objs:
        canon = _canonical_json(obj)
        sha1 = hashlib.sha1(canon.encode("utf-8")).hexdigest()
        for key, val in obj.items():
            cur.execute(insert_sql, (sha1, key, canonical_json(val)))
        hashes.append(sha1)
    conn.commit()
    return hashes


def retrieve_object(
    conn: sqlite3.Connection,
    canonical_json_sha1: str,
    table_name: str = "objectstore",
) -> Dict[str, Any]:
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
