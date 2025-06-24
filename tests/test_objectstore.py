import sqlite3
import json
from objectstore.main import create_object_table, insert_object, retrieve_object


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
