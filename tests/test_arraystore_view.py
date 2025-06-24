import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlite_store.arraystore.main import create_array_table, insert_array
from sqlite_store.arraystore.view import create_element_concat_view


def test_element_concat_view_default():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn)
    insert_array(conn, "hash1", [1, True])
    create_element_concat_view(conn)

    cur = conn.cursor()
    cur.execute(
        "SELECT element_json_space_joined FROM arraystore_element_concat WHERE canonical_json_sha1 = ?",
        ("hash1",),
    )
    row = cur.fetchone()
    assert row[0] == "1 true"
    conn.close()


def test_element_concat_view_custom_names():
    table = "custom_arrs"
    view = "custom_view"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn, table_name=table)
    insert_array(conn, "h1", [None, 2], table_name=table)
    create_element_concat_view(conn, view_name=view, table_name=table)

    cur = conn.cursor()
    cur.execute(
        f"SELECT element_json_space_joined FROM {view} WHERE canonical_json_sha1 = ?",
        ("h1",),
    )
    row = cur.fetchone()
    assert row[0] == "null 2"
    conn.close()

