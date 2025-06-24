"""Public API for the :mod:`sqlite_store.jsonstore` package."""

from .main import (
    create_json_table,
    insert_json,
    insert_json_auto_hash,
    retrieve_json,
)
from .fts import create_json_fts

__all__ = [
    "create_json_table",
    "insert_json",
    "insert_json_auto_hash",
    "retrieve_json",
    "create_json_fts",
]
