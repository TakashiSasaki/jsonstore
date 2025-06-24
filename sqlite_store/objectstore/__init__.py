"""Public API for the :mod:`sqlite_store.objectstore` package."""

from .main import (
    create_object_table,
    insert_object,
    insert_object_auto_hash,
    insert_objects_auto_hash,
    retrieve_object,
)

__all__ = [
    "create_object_table",
    "insert_object",
    "insert_object_auto_hash",
    "insert_objects_auto_hash",
    "retrieve_object",
]
