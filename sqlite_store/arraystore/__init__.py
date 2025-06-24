"""Public API for the :mod:`sqlite_store.arraystore` package."""

from .main import (
    create_array_table,
    insert_array,
    insert_array_auto_hash,
    insert_arrays_auto_hash,
    retrieve_array,
)
from .view import create_element_concat_view

__all__ = [
    "create_array_table",
    "insert_array",
    "insert_array_auto_hash",
    "insert_arrays_auto_hash",
    "retrieve_array",
    "create_element_concat_view",
]
