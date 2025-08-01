import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from jsonstore.arraystore.table import create_array_table, insert_array
from jsonstore.arraystore.view import create_element_concat_view
from jsonstore.arraystore.fts import create_element_concat_fts


def test_element_concat_fts_search():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn, table_name="arraystore")
    insert_array(conn, "h1", ["hello", "world"], table_name="arraystore")
    insert_array(conn, "h2", ["another", "test"], table_name="arraystore")
    create_element_concat_view(
        conn,
        view_name="arraystore_element_concat",
        table_name="arraystore",
    )
    create_element_concat_fts(
        conn,
        fts_table_name="arraystore_element_fts",
        view_name="arraystore_element_concat",
    )

    cur = conn.cursor()
    cur.execute(
        "SELECT canonical_json_sha1 FROM arraystore_element_fts WHERE arraystore_element_fts MATCH ?",
        ("hello",),
    )
    row = cur.fetchone()
    assert row[0] == "h1"
    conn.close()


def test_element_concat_fts_custom_names():
    table = "arrs"
    view = "arrs_view"
    fts = "arrs_fts"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn, table_name=table)
    insert_array(conn, "c1", ["alpha", "beta"], table_name=table)
    create_element_concat_view(conn, view_name=view, table_name=table)
    create_element_concat_fts(conn, fts_table_name=fts, view_name=view)

    cur = conn.cursor()
    cur.execute(
        f"SELECT canonical_json_sha1 FROM {fts} WHERE {fts} MATCH ?",
        ("alpha",),
    )
    row = cur.fetchone()
    assert row[0] == "c1"
    conn.close()
