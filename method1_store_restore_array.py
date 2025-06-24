# method1_store_restore_array.py
import sqlite3
import json

def create_array_table(conn):
    """Create table to store array elements."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS array_elements (
            array_hash TEXT,
            element_index INTEGER,
            element_value TEXT
        );
    """)
    conn.commit()

def insert_array(conn, array_hash, array):
    """Insert array into table using json.dumps to preserve types."""
    cur = conn.cursor()
    for idx, val in enumerate(array):
        # Store JSON literal representation
        value = 'null' if val is None else json.dumps(val)
        cur.execute(
            "INSERT INTO array_elements (array_hash, element_index, element_value) VALUES (?, ?, ?)",
            (array_hash, idx, value)
        )
    conn.commit()

def retrieve_array(conn, array_hash):
    """Retrieve array as Python list with preserved types."""
    cur = conn.cursor()
    cur.execute("""
        SELECT '[' || GROUP_CONCAT(element_value, ',') || ']' AS json_array
        FROM array_elements
        WHERE array_hash = ?
        GROUP BY array_hash;
    """, (array_hash,))
    row = cur.fetchone()
    return json.loads(row["json_array"]) if row else []

# ---- TEST FUNCTION ----

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
    print("Test passed. Array restored with exact type and value match.")

    conn.close()

# Run the test
test_method1_storage()
