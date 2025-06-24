import sqlite3
from typing import Any, Dict, List, Optional

from .table import (
    create_object_table,
    insert_object,
    insert_object_auto_hash,
    insert_objects_auto_hash,
    retrieve_object,
)
from .view import create_property_concat_view
from .fts import create_property_concat_fts


class ObjectStore:
    """Convenience wrapper class for object storage operations."""

    def __init__(
        self,
        conn: sqlite3.Connection,
        *,
        table_name: str = "objectstore",
        view_name: Optional[str] = "objectstore_property_concat",
        fts_table_name: Optional[str] = "objectstore_property_fts",
    ) -> None:
        self.conn = conn
        self.table_name = table_name
        self.view_name = view_name
        self.fts_table_name = fts_table_name
        create_object_table(conn, table_name=table_name)
        if view_name is not None:
            create_property_concat_view(conn, view_name=view_name, table_name=table_name)
        if fts_table_name is not None:
            if view_name is None:
                create_property_concat_view(conn, table_name=table_name)
                self.view_name = "objectstore_property_concat"
            create_property_concat_fts(
                conn,
                fts_table_name=fts_table_name,
                view_name=self.view_name,
            )

    def insert_object(self, canonical_json_sha1: str, obj: Dict[str, Any]) -> None:
        insert_object(
            self.conn,
            canonical_json_sha1,
            obj,
            table_name=self.table_name,
        )

    def insert_object_auto_hash(self, obj: Dict[str, Any]) -> str:
        return insert_object_auto_hash(
            self.conn,
            obj,
            table_name=self.table_name,
        )

    def insert_objects_auto_hash(self, objs: List[Dict[str, Any]]) -> List[str]:
        return insert_objects_auto_hash(
            self.conn,
            objs,
            table_name=self.table_name,
        )

    def retrieve_object(self, canonical_json_sha1: str) -> Dict[str, Any]:
        return retrieve_object(
            self.conn,
            canonical_json_sha1,
            table_name=self.table_name,
        )

    def create_view(self) -> None:
        create_property_concat_view(
            self.conn,
            view_name=self.view_name or "objectstore_property_concat",
            table_name=self.table_name,
        )

    def create_fts(self) -> None:
        create_property_concat_fts(
            self.conn,
            fts_table_name=self.fts_table_name or "objectstore_property_fts",
            view_name=self.view_name or "objectstore_property_concat",
        )
