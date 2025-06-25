import os
import sys
import sqlite3
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from jsonstore.objectstore.table import (
    create_object_table,
    insert_objects_auto_hash,
    retrieve_object,
)
from jsonstore import canonical_json

SAMPLE_FILE = os.path.join(
    os.path.dirname(__file__), "..", "samples", "jawiki-20250620-all-titles-in-ns0"
)


def test_bulk_insert_wikipedia_titles_as_objects():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_object_table(conn, table_name="objectstore")

    with open(SAMPLE_FILE, encoding="utf-8") as f:
        titles = [line.rstrip("\n") for line in f]

    def make_obj(chunk):
        keys = ["one", "two", "three", "four", "five"]
        obj = {}
        for i, val in enumerate(chunk):
            obj[keys[i]] = val
        return obj

    objects = [make_obj(titles[i : i + 5]) for i in range(0, len(titles), 5)]
    hashes = insert_objects_auto_hash(conn, objects, table_name="objectstore")

    assert len(hashes) == len(objects)

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM objectstore")
    row_count = cur.fetchone()[0]
    assert row_count == len(titles)

    for idx in [0, len(objects) // 2, len(objects) - 1]:
        expected_sha1 = hashlib.sha1(
            canonical_json(objects[idx]).encode("utf-8")
        ).hexdigest()
        restored = retrieve_object(conn, expected_sha1, table_name="objectstore")
        assert restored == objects[idx]

    conn.close()
