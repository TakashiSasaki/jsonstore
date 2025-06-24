import sqlite3
import hashlib

from canonicaljson import canonical_json


def _canonical_json(obj) -> str:
    """Return JSON canonical form used for hashing."""
    return canonical_json(obj)


def create_json_table(conn: sqlite3.Connection, table_name: str = "jsonstore"):
    """Create a table for storing complete JSON structures.

    Parameters
    ----------
    conn : sqlite3.Connection
        SQLite connection.
    table_name : str, optional
        Name of the table to create. Defaults to ``"jsonstore"``.
    """
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            canonical_json_sha1 TEXT PRIMARY KEY,
            canonical_json       TEXT NOT NULL
        );
        """
    )
    conn.commit()


def insert_json(
    conn: sqlite3.Connection,
    canonical_json_sha1: str,
    obj,
    table_name: str = "jsonstore",
):
    """Insert JSON structure using the provided SHA1 hash."""
    value = canonical_json(obj)
    conn.execute(
        f"INSERT OR REPLACE INTO {table_name} (canonical_json_sha1, canonical_json) VALUES (?, ?)",
        (canonical_json_sha1, value),
    )
    conn.commit()


def insert_json_auto_hash(conn: sqlite3.Connection, obj, table_name: str = "jsonstore") -> str:
    """Insert JSON structure computing its canonical SHA1 hash.

    Returns the computed SHA1 hash string.
    """
    canon = _canonical_json(obj)
    canon_sha1 = hashlib.sha1(canon.encode("utf-8")).hexdigest()
    insert_json(conn, canon_sha1, obj, table_name=table_name)
    return canon_sha1


def retrieve_json(conn: sqlite3.Connection, canonical_json_sha1: str, table_name: str = "jsonstore"):
    """Retrieve JSON structure previously stored."""
    cur = conn.cursor()
    cur.execute(
        f"SELECT canonical_json FROM {table_name} WHERE canonical_json_sha1 = ?",
        (canonical_json_sha1,),
    )
    row = cur.fetchone()
    import json

    return json.loads(row[0]) if row else None

