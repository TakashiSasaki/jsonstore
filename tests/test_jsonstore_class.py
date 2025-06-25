import os
import sys
import sqlite3
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from jsonstore.jsonstore.store import JsonStore  # noqa: E402
from jsonstore import canonical_json  # noqa: E402


def test_class_basic_storage():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    store = JsonStore(conn)
    data = {"a": [1, True], "b": None}
    cid = "json1"
    store.insert_json(cid, data)
    result = store.retrieve_json(cid)

    assert result == data
    conn.close()


def test_class_auto_hash():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    store = JsonStore(conn)
    obj = {"x": 1, "y": False}
    cid = store.insert_json_auto_hash(obj)
    result = store.retrieve_json(cid)
    expected = hashlib.sha1(canonical_json(obj).encode("utf-8")).hexdigest()
    assert cid == expected
    assert result == obj
    conn.close()


def test_class_custom_names():
    table = "js_table"
    fts = "js_fts"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    store = JsonStore(conn, table_name=table, fts_table_name=fts)
    cid = store.insert_json_auto_hash({"msg": "alpha"})
    store.create_fts()
    cur = conn.cursor()
    cur.execute(
        f"SELECT canonical_json_sha1 FROM {fts} WHERE {fts} MATCH ?",
        ("alpha",),
    )
    row = cur.fetchone()
    assert row[0] == cid
    conn.close()


def test_class_retrieve_all_json():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    store = JsonStore(conn)

    data = [{"v": i} for i in range(5)]
    for obj in data:
        store.insert_json_auto_hash(obj)

    records = store.retrieve_all_json()
    records_sorted = sorted(records, key=lambda x: x["v"])

    assert records_sorted == data
    conn.close()


def test_class_insert_jsons_auto_hash():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    store = JsonStore(conn)
    objs = [{"a": 1}, [1, 2]]
    hashes = store.insert_jsons_auto_hash(objs)
    assert len(hashes) == len(objs)
    for obj, cid in zip(objs, hashes):
        restored = store.retrieve_json(cid)
        assert restored == obj
    conn.close()
