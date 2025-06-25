import os
import sys
import sqlite3
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from jsonstore.objectstore.store import ObjectStore  # noqa: E402
from jsonstore import canonical_json  # noqa: E402


def test_class_basic_storage():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    store = ObjectStore(conn)
    obj = {"a": 1, "b": True, "c": None}
    cid = "oid1"
    store.insert_object(cid, obj)
    result = store.retrieve_object(cid)

    assert result == obj
    conn.close()


def test_class_auto_hash():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    store = ObjectStore(conn)
    obj = {"x": [1], "y": False}
    cid = store.insert_object_auto_hash(obj)
    result = store.retrieve_object(cid)
    expected = hashlib.sha1(canonical_json(obj).encode("utf-8")).hexdigest()
    assert cid == expected
    assert result == obj
    conn.close()


def test_class_insert_objects_auto_hash():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    store = ObjectStore(conn)
    objects = [{"a": 1}, {"b": True, "c": None}]
    hashes = store.insert_objects_auto_hash(objects)
    assert len(hashes) == len(objects)
    for obj, cid in zip(objects, hashes):
        restored = store.retrieve_object(cid)
        assert restored == obj
    conn.close()


def test_class_custom_names():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    store = ObjectStore(
        conn,
        table_name="t_obj",
        view_name="v_obj",
        fts_table_name="f_obj",
    )
    cid = store.insert_object_auto_hash({"x": "y"})
    cur = conn.cursor()
    cur.execute("SELECT property_json_space_joined FROM v_obj WHERE canonical_json_sha1 = ?", (cid,))
    row = cur.fetchone()
    assert row[0] == "\"y\""
    conn.close()
