import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlite_store.objectstore.table import (
    create_object_table,
    insert_object,
)
from sqlite_store.objectstore.view import create_property_concat_view


def test_property_concat_view_default():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn, table_name="objectstore")
    insert_object(conn, "hash1", {"a": 1, "b": True}, table_name="objectstore")
    create_property_concat_view(
        conn,
        view_name="objectstore_property_concat",
        table_name="objectstore",
    )

    cur = conn.cursor()
    cur.execute(
        "SELECT property_json_space_joined FROM objectstore_property_concat WHERE canonical_json_sha1 = ?",
        ("hash1",),
    )
    row = cur.fetchone()
    assert row[0] == "1 true"
    conn.close()


def test_property_concat_view_custom_names():
    table = "custom_objs"
    view = "custom_view"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn, table_name=table)
    insert_object(conn, "h1", {"x": None, "y": 2}, table_name=table)
    create_property_concat_view(conn, view_name=view, table_name=table)

    cur = conn.cursor()
    cur.execute(
        f"SELECT property_json_space_joined FROM {view} WHERE canonical_json_sha1 = ?",
        ("h1",),
    )
    row = cur.fetchone()
    assert row[0] == "null 2"
    conn.close()

