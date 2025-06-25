"""Public API for the :mod:`jsonstore.jsonstore` package."""

from .table import (
    create_json_table,
    insert_json,
    insert_json_auto_hash,
    insert_jsons_auto_hash,
    retrieve_json,
    retrieve_all_json,
)
from .fts import create_json_fts
from .store import JsonStore

__all__ = [
    "create_json_table",
    "insert_json",
    "insert_json_auto_hash",
    "insert_jsons_auto_hash",
    "retrieve_json",
    "retrieve_all_json",
    "create_json_fts",
    "JsonStore",
]
