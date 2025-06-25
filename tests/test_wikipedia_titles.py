import os
import sys
import sqlite3
import hashlib
import itertools

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from jsonstore.jsonstore.table import (
    create_json_table,
    insert_jsons_auto_hash,
    retrieve_json,
)
from jsonstore import canonical_json


SAMPLE_FILE = os.path.join(
    os.path.dirname(__file__), "..", "samples", "jawiki-20250620-all-titles-in-ns0"
)


def test_bulk_insert_wikipedia_titles():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    create_json_table(conn, table_name="jsonstore")

    with open(SAMPLE_FILE, encoding="utf-8") as f:
        titles = [line.rstrip("\n") for line in itertools.islice(f, 10000)]

    hashes = insert_jsons_auto_hash(conn, titles, table_name="jsonstore")

    assert len(hashes) == len(titles)

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM jsonstore")
    row_count = cur.fetchone()[0]
    assert row_count == len(titles)

    for idx in [0, len(titles) // 2, len(titles) - 1]:
        expected_sha1 = hashlib.sha1(
            canonical_json(titles[idx]).encode("utf-8")
        ).hexdigest()
        restored = retrieve_json(conn, expected_sha1, table_name="jsonstore")
        assert restored == titles[idx]

    conn.close()
