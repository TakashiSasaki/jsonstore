# test_method1_array_store.py

import sqlite3
import json
from method1_store_restore_array import create_array_table, insert_array, retrieve_array


def test_method1_storage():
    """Test storing and retrieving array via Method 1."""
    test_array = [42, 3.14, None, True, False, "hello", "true", "false", "null", "", 0, -0, 1, -1, "0", "1"]
    array_hash = "testhash"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn)
    insert_array(conn, array_hash, test_array)
    result = retrieve_array(conn, array_hash)

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
    array_hash = "nested_test"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn)
    insert_array(conn, array_hash, nested_array)
    result = retrieve_array(conn, array_hash)

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
    array_hash = "object_test"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn)
    insert_array(conn, array_hash, object_array)
    result = retrieve_array(conn, array_hash)

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


if __name__ == "__main__":
    test_method1_storage()
    test_method1_nested_array()
    test_method1_object_array()
