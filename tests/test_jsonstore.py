import os
import sys
import sqlite3
import json
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from jsonstore.main import (
    create_json_table,
    insert_json,
    insert_json_auto_hash,
    retrieve_json,
)
from canonicaljson import canonical_json


def test_json_storage():
    data = {"a": [1, 2], "b": True}
    cid = "jsonhash"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_json_table(conn)
    insert_json(conn, cid, data)
    result = retrieve_json(conn, cid)

    assert result == data
    assert json.dumps(result, sort_keys=True) == json.dumps(data, sort_keys=True)
    conn.close()


def test_insert_json_auto_hash():
    obj = [1, {"b": False}]
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_json_table(conn)
    computed_hash = insert_json_auto_hash(conn, obj)
    result = retrieve_json(conn, computed_hash)

    expected_hash = hashlib.sha1(canonical_json(obj).encode("utf-8")).hexdigest()

    assert computed_hash == expected_hash
    assert result == obj
    conn.close()


def test_json_column_canonical():
    obj = {"b": 1, "a": 2}
    cid = "canonjson"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_json_table(conn)
    insert_json(conn, cid, obj)

    cur = conn.cursor()
    cur.execute("SELECT canonical_json FROM jsonstore WHERE canonical_json_sha1 = ?", (cid,))
    row = cur.fetchone()

    assert row[0] == canonical_json(obj)
    conn.close()


def test_jsonstore_various_types_and_strings():
    complex_obj = {
        "numbers": [0, -1, 1.2345, 1e20, -0.0],
        "bools": [True, False],
        "strings": [
            "", 
            "simple", 
            "quote\"test", 
            "line\nbreak", 
            "tab\tchar", 
            "unicode\u2603", 
            "日本語", 
        ],
        "nested": {"a": [None, {"b": "c"}], "x": {"y": [1, 2, {"z": False}]}},
        "num_strings": ["0", "-1", "1e10"],
        "bool_string": "false",
        "null_string": "null",
    }

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_json_table(conn)
    hash_id = insert_json_auto_hash(conn, complex_obj)
    result = retrieve_json(conn, hash_id)

    assert result == complex_obj
    conn.close()
