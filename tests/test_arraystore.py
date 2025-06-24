# test_arraystore.py

import os
import sys
import sqlite3
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlite_store.arraystore.main import (
    create_array_table,
    insert_array,
    insert_array_auto_hash,
    retrieve_array,
)
from sqlite_store import canonical_json
import hashlib


def test_method1_storage():
    """Test storing and retrieving array via Method 1."""
    test_array = [42, 3.14, None, True, False, "hello", "true", "false", "null", "", 0, -0, 1, -1, "0", "1"]
    canonical_json_sha1 = "testhash"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn)
    insert_array(conn, canonical_json_sha1, test_array)
    result = retrieve_array(conn, canonical_json_sha1)

    assert result == test_array, (
        f"Restored array does not match original.\n"
        f"Original: {test_array}\nRestored: {result}"
    )
    assert json.dumps(result) == json.dumps(test_array), (
        f"JSON representation does not match.\n"
        f"Original: {json.dumps(test_array)}\nRestored: {json.dumps(result)}"
    )

    print("All tests passed. Array restored with exact type and value match.")
    conn.close()


def test_method1_nested_array():
    """Test storing and retrieving nested arrays via Method 1."""
    nested_array = [[1, 2], ["a", True], [], [None, [3.14]]]
    canonical_json_sha1 = "nested_test"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn)
    insert_array(conn, canonical_json_sha1, nested_array)
    result = retrieve_array(conn, canonical_json_sha1)

    assert result == nested_array, (
        f"Restored nested array does not match original.\n"
        f"Original: {nested_array}\nRestored: {result}"
    )
    assert json.dumps(result) == json.dumps(nested_array), (
        f"JSON representation of nested array does not match.\n"
        f"Original: {json.dumps(nested_array)}\nRestored: {json.dumps(result)}"
    )

    print("Nested array test passed. Structure and types preserved.")
    conn.close()


def test_method1_object_array():
    """Test storing and retrieving array with object elements via Method 1."""
    object_array = [
        {"a": 1, "b": [2, False]},
        {"nested": {"x": True, "y": None}}
    ]
    canonical_json_sha1 = "object_test"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn)
    insert_array(conn, canonical_json_sha1, object_array)
    result = retrieve_array(conn, canonical_json_sha1)

    assert result == object_array, (
        f"Restored object array does not match original.\n"
        f"Original: {object_array}\nRestored: {result}"
    )
    assert json.dumps(result) == json.dumps(object_array), (
        f"JSON representation of object array does not match.\n"
        f"Original: {json.dumps(object_array)}\nRestored: {json.dumps(result)}"
    )

    print("Object array test passed. Objects and nested structures preserved.")
    conn.close()


def test_custom_table_name():
    """Test using a custom table name for storage and retrieval."""
    custom_table = "custom_elements"
    test_array = [1, 2, 3]
    canonical_json_sha1 = "custom_table_test"

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn, table_name=custom_table)
    insert_array(conn, canonical_json_sha1, test_array, table_name=custom_table)
    result = retrieve_array(conn, canonical_json_sha1, table_name=custom_table)

    assert result == test_array
    conn.close()


def test_insert_array_auto_hash():
    """Ensure insert_array_auto_hash computes SHA1 and stores array."""
    arr = [1, {"b": True}, [2, 3]]
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn)
    computed_hash = insert_array_auto_hash(conn, arr)
    result = retrieve_array(conn, computed_hash)

    expected_hash = hashlib.sha1(canonical_json(arr).encode("utf-8")).hexdigest()

    assert computed_hash == expected_hash
    assert result == arr
    conn.close()


def test_element_json_canonical():
    """Ensure each element is stored using canonical JSON."""
    data = [0, 1.0, -0.0, {"b": [2, False]}, [1, 2], None]
    cid = "canon_test"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn)
    insert_array(conn, cid, data)

    cur = conn.cursor()
    cur.execute(
        "SELECT element_index, element_json FROM arraystore WHERE canonical_json_sha1 = ? ORDER BY element_index",
        (cid,),
    )
    rows = cur.fetchall()

    for idx, json_val in rows:
        assert json_val == canonical_json(data[idx])
    conn.close()


if __name__ == "__main__":
    test_method1_storage()
    test_method1_nested_array()
    test_method1_object_array()
