import os
import sys
import jcs

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlite_store import canonical_json


def test_canonical_numbers():
    values = [
        0,
        -0.0,
        1,
        1.0,
        -1.0,
        0.1,
        1e-6,
        1e20,
        -123.456,
        3.141592653589793,
    ]
    for val in values:
        assert canonical_json(val) == jcs.canonicalize(val).decode("utf-8")


def test_canonical_complex_structure():
    obj = {
        "b": [1, 2.0, -0.0, None],
        "a": {"x": 1e20, "y": True},
        "c": "text",
    }
    expected = jcs.canonicalize(obj).decode("utf-8")
    assert canonical_json(obj) == expected


def test_unicode_in_keys_and_values():
    obj = {
        "😀": "🍣 sushi",
        "text": "こんにちは世界",
        "emoji_key\U0001F600": "value",
    }
    expected = jcs.canonicalize(obj).decode("utf-8")
    assert canonical_json(obj) == expected


def test_control_chars_in_strings():
    obj = {
        "line\nbreak": "val\tcontrol",
        "ctrl\u0001key": "\u0002value",
    }
    expected = jcs.canonicalize(obj).decode("utf-8")
    assert canonical_json(obj) == expected
