import os
import sys
import sqlite3
import json
import hashlib
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from jsonstore.jsonstore.table import (
    create_json_table,
    insert_json,
    insert_json_auto_hash,
    retrieve_json,
    retrieve_all_json,
)
from jsonstore import canonical_json


def test_json_storage():
    data = {"a": [1, 2], "b": True}
    cid = "jsonhash"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_json_table(conn, table_name="jsonstore")
    insert_json(conn, cid, data, table_name="jsonstore")
    result = retrieve_json(conn, cid, table_name="jsonstore")

    assert result == data
    assert json.dumps(result, sort_keys=True) == json.dumps(data, sort_keys=True)
    conn.close()


def test_insert_json_auto_hash():
    obj = [1, {"b": False}]
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_json_table(conn, table_name="jsonstore")
    computed_hash = insert_json_auto_hash(conn, obj, table_name="jsonstore")
    result = retrieve_json(conn, computed_hash, table_name="jsonstore")

    expected_hash = hashlib.sha1(canonical_json(obj).encode("utf-8")).hexdigest()

    assert computed_hash == expected_hash
    assert result == obj
    conn.close()


def test_json_column_canonical():
    obj = {"b": 1, "a": 2}
    cid = "canonjson"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_json_table(conn, table_name="jsonstore")
    insert_json(conn, cid, obj, table_name="jsonstore")

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

    create_json_table(conn, table_name="jsonstore")
    hash_id = insert_json_auto_hash(conn, complex_obj, table_name="jsonstore")
    result = retrieve_json(conn, hash_id, table_name="jsonstore")

    assert result == complex_obj
    conn.close()


def _random_unicode_string(rng: random.Random, min_bytes: int) -> str:
    """Return a random Unicode string of at least ``min_bytes`` UTF-8 bytes."""
    parts = []
    size = 0
    while size < min_bytes:
        cp = rng.randint(0, 0x10FFFF)
        if 0xD800 <= cp <= 0xDFFF:
            continue
        ch = chr(cp)
        parts.append(ch)
        size += len(ch.encode("utf-8"))
    return "".join(parts)


def test_large_random_unicode_strings():
    """Store and retrieve many large random Unicode strings."""
    rng = random.Random(0)
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_json_table(conn, table_name="jsonstore")

    strings = [_random_unicode_string(rng, 102400) for _ in range(100)]
    hashes = [insert_json_auto_hash(conn, s, table_name="jsonstore") for s in strings]

    for cid, original in zip(hashes, strings):
        restored = retrieve_json(conn, cid, table_name="jsonstore")
        assert restored == original

    conn.close()


def test_retrieve_all_json():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_json_table(conn, table_name="jsonstore")
    data = [{"id": i} for i in range(3)]
    for obj in data:
        insert_json_auto_hash(conn, obj, table_name="jsonstore")

    records = retrieve_all_json(conn, table_name="jsonstore")
    records_sorted = sorted(records, key=lambda x: x["id"])

    assert records_sorted == data
    conn.close()
