import sqlite3


def create_property_concat_fts(
    conn: sqlite3.Connection,
    fts_table_name: str,
    view_name: str,
) -> None:
    """Create FTS5 virtual table for the property concat view.

    This function creates an FTS5 table that indexes the space-joined
    JSON property strings produced by
    :func:`sqlite_store.objectstore.view.create_property_concat_view`.
    """

    conn.execute(
        f"CREATE VIRTUAL TABLE IF NOT EXISTS {fts_table_name} "
        "USING fts5(property_json_space_joined, canonical_json_sha1 UNINDEXED)"
    )
    conn.execute(
        f"INSERT INTO {fts_table_name}(property_json_space_joined, canonical_json_sha1) "
        f"SELECT property_json_space_joined, canonical_json_sha1 FROM {view_name}"
    )
    conn.commit()
