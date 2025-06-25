import sqlite3
from typing import Any, Optional

from .table import (
    create_json_table,
    insert_json,
    insert_json_auto_hash,
    retrieve_json,
    retrieve_all_json,
)
from .fts import create_json_fts


class JsonStore:
    """Convenience wrapper class for JSON storage operations."""

    def __init__(
        self,
        conn: sqlite3.Connection,
        *,
        table_name: str = "jsonstore",
        fts_table_name: Optional[str] = "jsonstore_fts",
    ) -> None:
        self.conn = conn
        self.table_name = table_name
        self.fts_table_name = fts_table_name
        create_json_table(conn, table_name=table_name)
        if fts_table_name is not None:
            create_json_fts(conn, fts_table_name=fts_table_name, table_name=table_name)

    def insert_json(self, canonical_json_sha1: str, obj: Any) -> None:
        insert_json(
            self.conn,
            canonical_json_sha1,
            obj,
            table_name=self.table_name,
        )

    def insert_json_auto_hash(self, obj: Any) -> str:
        return insert_json_auto_hash(
            self.conn,
            obj,
            table_name=self.table_name,
        )

    def retrieve_json(self, canonical_json_sha1: str) -> Any:
        return retrieve_json(
            self.conn,
            canonical_json_sha1,
            table_name=self.table_name,
        )

    def retrieve_all_json(self) -> list:
        return retrieve_all_json(
            self.conn,
            table_name=self.table_name,
        )

    def create_fts(self) -> None:
        create_json_fts(
            self.conn,
            fts_table_name=self.fts_table_name or "jsonstore_fts",
            table_name=self.table_name,
        )
