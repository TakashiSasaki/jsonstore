import sqlite3


def create_element_concat_view(
    conn: sqlite3.Connection,
    view_name: str = "arraystore_element_concat",
    table_name: str = "arraystore",
) -> None:
    """Create a view that concatenates element_json values by array hash.

    The view will contain ``canonical_json_sha1`` and a space separated
    concatenation of ``element_json`` values for each hash.
    """
    conn.execute(
        f"""
        CREATE VIEW IF NOT EXISTS {view_name} AS
        SELECT
            canonical_json_sha1,
            GROUP_CONCAT(element_json, ' ') AS element_json_space_joined
        FROM {table_name}
        GROUP BY canonical_json_sha1;
        """
    )
    conn.commit()

