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

    assert result == test_array, f"Restored array does not match original.\nOriginal: {test_array}\nRestored: {result}"
    assert json.dumps(result) == json.dumps(test_array), f"JSON representation does not match.\nOriginal: {json.dumps(test_array)}\nRestored: {json.dumps(result)}"

    print("All tests passed. Array restored with exact type and value match.")
    conn.close()

if __name__ == "__main__":
    test_method1_storage()
