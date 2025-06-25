"""Public API for the :mod:`jsonstore.arraystore` package."""

from .table import (
    create_array_table,
    insert_array,
    insert_array_auto_hash,
    insert_arrays_auto_hash,
    retrieve_array,
    retrieve_all_arrays,
)
from .view import create_element_concat_view
from .fts import create_element_concat_fts
from .store import ArrayStore

__all__ = [
    "create_array_table",
    "insert_array",
    "insert_array_auto_hash",
    "insert_arrays_auto_hash",
    "retrieve_array",
    "retrieve_all_arrays",
    "create_element_concat_view",
    "create_element_concat_fts",
    "ArrayStore",
]
