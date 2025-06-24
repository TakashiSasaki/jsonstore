import sqlite3


def create_element_concat_fts(
    conn: sqlite3.Connection,
    fts_table_name: str = "arraystore_element_fts",
    view_name: str = "arraystore_element_concat",
) -> None:
    """Create FTS5 virtual table for the element concat view.

    This creates an FTS5 table that allows full-text search over the
    space-joined JSON element strings produced by
    :func:`sqlite_store.arraystore.view.create_element_concat_view`.
    """

    conn.execute(
        f"CREATE VIRTUAL TABLE IF NOT EXISTS {fts_table_name} "
        "USING fts5(element_json_space_joined, canonical_json_sha1 UNINDEXED)"
    )
    conn.execute(
        f"INSERT INTO {fts_table_name}(element_json_space_joined, canonical_json_sha1) "
        f"SELECT element_json_space_joined, canonical_json_sha1 FROM {view_name}"
    )
    conn.commit()
