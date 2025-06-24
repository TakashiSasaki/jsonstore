import sqlite3
from typing import Any, List, Optional

from .table import (
    create_array_table,
    insert_array,
    insert_array_auto_hash,
    insert_arrays_auto_hash,
    retrieve_array,
)
from .view import create_element_concat_view
from .fts import create_element_concat_fts


class ArrayStore:
    """Convenience wrapper class for array storage operations."""

    def __init__(
        self,
        conn: sqlite3.Connection,
        *,
        table_name: str = "arraystore",
        view_name: Optional[str] = "arraystore_element_concat",
        fts_table_name: Optional[str] = "arraystore_element_fts",
    ) -> None:
        self.conn = conn
        self.table_name = table_name
        self.view_name = view_name
        self.fts_table_name = fts_table_name
        create_array_table(conn, table_name=table_name)
        if view_name is not None:
            create_element_concat_view(conn, view_name=view_name, table_name=table_name)
        if fts_table_name is not None:
            if view_name is None:
                create_element_concat_view(conn, table_name=table_name)
                self.view_name = "arraystore_element_concat"
            create_element_concat_fts(
                conn,
                fts_table_name=fts_table_name,
                view_name=self.view_name,
            )

    def insert_array(self, canonical_json_sha1: str, array: List[Any]) -> None:
        insert_array(
            self.conn,
            canonical_json_sha1,
            array,
            table_name=self.table_name,
        )

    def insert_array_auto_hash(self, array: List[Any]) -> str:
        return insert_array_auto_hash(
            self.conn,
            array,
            table_name=self.table_name,
        )

    def insert_arrays_auto_hash(self, arrays: List[List[Any]]) -> List[str]:
        return insert_arrays_auto_hash(
            self.conn,
            arrays,
            table_name=self.table_name,
        )

    def retrieve_array(self, canonical_json_sha1: str) -> List[Any]:
        return retrieve_array(
            self.conn,
            canonical_json_sha1,
            table_name=self.table_name,
        )

    def create_view(self) -> None:
        create_element_concat_view(
            self.conn,
            view_name=self.view_name or "arraystore_element_concat",
            table_name=self.table_name,
        )

    def create_fts(self) -> None:
        create_element_concat_fts(
            self.conn,
            fts_table_name=self.fts_table_name or "arraystore_element_fts",
            view_name=self.view_name or "arraystore_element_concat",
        )

