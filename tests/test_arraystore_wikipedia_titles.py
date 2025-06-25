import os
import sys
import sqlite3
import hashlib
import itertools

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from jsonstore.arraystore.table import (
    create_array_table,
    insert_arrays_auto_hash,
    retrieve_array,
)
from jsonstore import canonical_json

SAMPLE_FILE = os.path.join(
    os.path.dirname(__file__), "..", "samples", "jawiki-20250620-all-titles-in-ns0"
)


def test_bulk_insert_wikipedia_titles_as_arrays():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_array_table(conn, table_name="arraystore")

    with open(SAMPLE_FILE, encoding="utf-8") as f:
        titles = [line.rstrip("\n") for line in itertools.islice(f, 10000)]

    arrays = [titles[i : i + 5] for i in range(0, len(titles), 5)]
    hashes = insert_arrays_auto_hash(conn, arrays, table_name="arraystore")

    assert len(hashes) == len(arrays)

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM arraystore")
    row_count = cur.fetchone()[0]
    assert row_count == len(titles)

    for idx in [0, len(arrays) // 2, len(arrays) - 1]:
        expected_sha1 = hashlib.sha1(
            canonical_json(arrays[idx]).encode("utf-8")
        ).hexdigest()
        restored = retrieve_array(conn, expected_sha1, table_name="arraystore")
        assert restored == arrays[idx]

    conn.close()
