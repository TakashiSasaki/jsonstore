# main.py for objectstore

import sqlite3
import json


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
            object_hash TEXT NOT NULL,
            property_name TEXT NOT NULL,
            property_json TEXT,
            PRIMARY KEY (object_hash, property_name)
        );
        """
    )
    conn.execute(
        f"CREATE INDEX IF NOT EXISTS idx_{table_name}_hash ON {table_name}(object_hash);"
    )
    conn.commit()


def insert_object(conn: sqlite3.Connection, object_hash, obj: dict, table_name: str = "objectstore"):
    """Insert a Python dict into the table preserving JSON types."""
    cur = conn.cursor()
    for key, val in obj.items():
        value = 'null' if val is None else json.dumps(val)
        cur.execute(
            f"INSERT OR REPLACE INTO {table_name} (object_hash, property_name, property_json) VALUES (?, ?, ?)",
            (object_hash, key, value),
        )
    conn.commit()


def retrieve_object(conn: sqlite3.Connection, object_hash, table_name: str = "objectstore"):
    """Retrieve a Python dict previously stored with insert_object."""
    cur = conn.cursor()
    cur.execute(
        f"SELECT property_name, property_json FROM {table_name} WHERE object_hash = ?",
        (object_hash,),
    )
    rows = cur.fetchall()
    result = {}
    for row in rows:
        result[row[0]] = json.loads(row[1]) if row[1] is not None else None
    return result
