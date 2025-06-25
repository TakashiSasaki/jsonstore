import sqlite3


def create_json_fts(
    conn: sqlite3.Connection,
    fts_table_name: str,
    table_name: str,
) -> None:
    """Create FTS5 virtual table for the JSON store table.

    This function creates an FTS5 table that indexes the ``canonical_json``
    column from the table produced by
    :func:`jsonstore.jsonstore.table.create_json_table`.
    """

    conn.execute(
        f"CREATE VIRTUAL TABLE IF NOT EXISTS {fts_table_name} "
        "USING fts5(canonical_json, canonical_json_sha1 UNINDEXED)"
    )
    conn.execute(
        f"INSERT INTO {fts_table_name}(canonical_json, canonical_json_sha1) "
        f"SELECT canonical_json, canonical_json_sha1 FROM {table_name}"
    )
    conn.commit()
