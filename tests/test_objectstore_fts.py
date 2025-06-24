import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlite_store.objectstore.table import create_object_table, insert_object
from sqlite_store.objectstore.view import create_property_concat_view
from sqlite_store.objectstore.fts import create_property_concat_fts


def test_property_concat_fts_search():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn)
    insert_object(conn, "obj1", {"a": 1, "b": "text"})
    insert_object(conn, "obj2", {"c": True})
    create_property_concat_view(conn)
    create_property_concat_fts(conn)

    cur = conn.cursor()
    cur.execute(
        "SELECT canonical_json_sha1 FROM objectstore_property_fts WHERE objectstore_property_fts MATCH ?",
        ("text",),
    )
    row = cur.fetchone()
    assert row[0] == "obj1"
    conn.close()


def test_property_concat_fts_custom_names():
    table = "objs"
    view = "objs_view"
    fts = "objs_fts"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn, table_name=table)
    insert_object(conn, "h1", {"x": "hello"}, table_name=table)
    create_property_concat_view(conn, view_name=view, table_name=table)
    create_property_concat_fts(conn, fts_table_name=fts, view_name=view)

    cur = conn.cursor()
    cur.execute(
        f"SELECT canonical_json_sha1 FROM {fts} WHERE {fts} MATCH ?",
        ("hello",),
    )
    row = cur.fetchone()
    assert row[0] == "h1"
    conn.close()
