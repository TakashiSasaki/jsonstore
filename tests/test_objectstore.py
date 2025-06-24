import os
import sys
import sqlite3
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from objectstore.main import create_object_table, insert_object, retrieve_object


def test_object_storage():
    data = {"a": 1, "b": True, "c": None, "d": [1, 2], "e": {"x": False}}
    obj_hash = "objhash"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn)
    insert_object(conn, obj_hash, data)
    result = retrieve_object(conn, obj_hash)

    assert result == data
    assert json.dumps(result, sort_keys=True) == json.dumps(data, sort_keys=True)
    conn.close()


def test_custom_table_name_object():
    custom_table = "custom_objects"
    data = {"key": "value"}
    obj_hash = "custom_obj"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn, table_name=custom_table)
    insert_object(conn, obj_hash, data, table_name=custom_table)
    result = retrieve_object(conn, obj_hash, table_name=custom_table)

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
