import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlite_store.jsonstore.main import create_json_table, insert_json
from sqlite_store.jsonstore.fts import create_json_fts


def test_json_fts_search():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_json_table(conn)
    insert_json(conn, "j1", {"text": "hello"})
    insert_json(conn, "j2", {"text": "world"})
    create_json_fts(conn)

    cur = conn.cursor()
    cur.execute(
        "SELECT canonical_json_sha1 FROM jsonstore_fts WHERE jsonstore_fts MATCH ?",
        ("hello",),
    )
    row = cur.fetchone()
    assert row[0] == "j1"
    conn.close()


def test_json_fts_custom_names():
    table = "js"
    fts = "js_fts"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_json_table(conn, table_name=table)
    insert_json(conn, "c1", {"msg": "alpha"}, table_name=table)
    create_json_fts(conn, fts_table_name=fts, table_name=table)

    cur = conn.cursor()
    cur.execute(
        f"SELECT canonical_json_sha1 FROM {fts} WHERE {fts} MATCH ?",
        ("alpha",),
    )
    row = cur.fetchone()
    assert row[0] == "c1"
    conn.close()
