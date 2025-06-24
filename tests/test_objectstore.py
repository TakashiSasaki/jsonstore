import os
import sys
import sqlite3
import json
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlite_store.objectstore.main import (
    create_object_table,
    insert_object,
    insert_object_auto_hash,
    insert_objects_auto_hash,
    retrieve_object,
)
from sqlite_store import canonical_json


def test_object_storage():
    data = {"a": 1, "b": True, "c": None, "d": [1, 2], "e": {"x": False}}
    canonical_json_sha1 = "objhash"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn)
    insert_object(conn, canonical_json_sha1, data)
    result = retrieve_object(conn, canonical_json_sha1)

    assert result == data
    assert json.dumps(result, sort_keys=True) == json.dumps(data, sort_keys=True)
    conn.close()


def test_custom_table_name_object():
    custom_table = "custom_objects"
    data = {"key": "value"}
    canonical_json_sha1 = "custom_obj"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn, table_name=custom_table)
    insert_object(conn, canonical_json_sha1, data, table_name=custom_table)
    result = retrieve_object(conn, canonical_json_sha1, table_name=custom_table)

    assert result == data
    conn.close()


def test_object_storage_various_types():
    values = [
        42,
        3.14,
        None,
        True,
        False,
        "hello",
        "true",
        "false",
        "null",
        "",
        0,
        -0,
        1,
        -1,
        "0",
        "1",
    ]
    data = {f"val_{i}": v for i, v in enumerate(values)}
    obj_hash = "various_types"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn)
    insert_object(conn, obj_hash, data)
    result = retrieve_object(conn, obj_hash)

    assert result == data
    for key, val in data.items():
        assert type(result[key]) is type(val)
    conn.close()


def test_insert_object_auto_hash():
    """Ensure insert_object_auto_hash computes SHA1 and stores object."""
    obj = {"x": 1, "y": [True, False]}
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn)
    computed_hash = insert_object_auto_hash(conn, obj)
    result = retrieve_object(conn, computed_hash)

    expected_hash = hashlib.sha1(canonical_json(obj).encode("utf-8")).hexdigest()

    assert computed_hash == expected_hash
    assert result == obj
    conn.close()


def test_property_json_is_canonical():
    """Ensure stored JSON uses canonical form."""
    obj = {
        "unsorted": {"b": 1, "a": 2},
        "array": [1, 2.0, -0.0],
        "nullval": None,
    }
    hash_id = "canonprop"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn)
    insert_object(conn, hash_id, obj)

    cur = conn.cursor()
    cur.execute(
        "SELECT property_name, property_json, property_json_sha1 FROM objectstore WHERE canonical_json_sha1 = ?",
        (hash_id,),
    )
    rows = cur.fetchall()

    for row in rows:
        name = row[0]
        stored = row[1]
        sha1_val = row[2]
        canonical = canonical_json(obj[name])
        expected_sha1 = hashlib.sha1(canonical.encode("utf-8")).hexdigest()
        assert stored == canonical
        assert sha1_val == expected_sha1
    conn.close()


def test_insert_objects_auto_hash():
    objs = [
        {"a": 1, "b": True},
        {"x": [1, 2], "y": None},
    ]
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn)
    hashes = insert_objects_auto_hash(conn, objs)

    expected = [
        hashlib.sha1(canonical_json(o).encode("utf-8")).hexdigest() for o in objs
    ]

    assert hashes == expected
    for h, original in zip(hashes, objs):
        restored = retrieve_object(conn, h)
        assert restored == original
    conn.close()
