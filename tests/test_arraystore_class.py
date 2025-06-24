import os
import sys
import sqlite3
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlite_store.arraystore.store import ArrayStore  # noqa: E402
from sqlite_store import canonical_json  # noqa: E402


def test_class_basic_storage():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    store = ArrayStore(conn)
    arr = [1, True, None]
    cid = "cid1"
    store.insert_array(cid, arr)
    result = store.retrieve_array(cid)

    assert result == arr
    conn.close()


def test_class_auto_hash():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    store = ArrayStore(conn)
    arr = ["a", {"b": False}]
    cid = store.insert_array_auto_hash(arr)
    result = store.retrieve_array(cid)
    expected = hashlib.sha1(canonical_json(arr).encode("utf-8")).hexdigest()
    assert cid == expected
    assert result == arr
    conn.close()


def test_class_insert_arrays_auto_hash():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    store = ArrayStore(conn)
    arrays = [[1], [True, False]]
    hashes = store.insert_arrays_auto_hash(arrays)
    assert len(hashes) == len(arrays)
    for arr, cid in zip(arrays, hashes):
        restored = store.retrieve_array(cid)
        assert restored == arr
    conn.close()


def test_class_custom_names():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    store = ArrayStore(
        conn,
        table_name="t",
        view_name="v",
        fts_table_name="f",
    )
    cid = store.insert_array_auto_hash(["x"])
    cur = conn.cursor()
    cur.execute("SELECT element_json_space_joined FROM v WHERE canonical_json_sha1 = ?", (cid,))
    row = cur.fetchone()
    assert row[0] == "\"x\""
    conn.close()

