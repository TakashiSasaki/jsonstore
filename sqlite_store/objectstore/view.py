import sqlite3


def create_property_concat_view(
    conn: sqlite3.Connection,
    view_name: str,
    table_name: str,
) -> None:
    """Create a view that concatenates property_json values by object hash.

    The view will contain ``canonical_json_sha1`` and a space separated
    concatenation of ``property_json`` values for each hash.
    """
    conn.execute(
        f"""
        CREATE VIEW IF NOT EXISTS {view_name} AS
        SELECT
            canonical_json_sha1,
            GROUP_CONCAT(property_json, ' ') AS property_json_space_joined
        FROM {table_name}
        GROUP BY canonical_json_sha1;
        """
    )
    conn.commit()
