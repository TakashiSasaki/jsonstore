import subprocess
import sys
import textwrap
import pytest

pytest.importorskip("httpimport")


def test_remote_import_via_httpimport():
    script = textwrap.dedent(
        """
        from httpimport import github_repo
        import sqlite3
        import jcs
        with github_repo('TakashiSasaki', 'jsonstore', ref='master'):
            from jsonstore import canonical_json
            from jsonstore.jsonstore.store import JsonStore
            data = {'b': 1, 'a': [True, None]}
            result = canonical_json(data)
            assert result == jcs.canonicalize(data).decode('utf-8')
            conn = sqlite3.connect(':memory:')
            conn.row_factory = sqlite3.Row
            store = JsonStore(conn)
            sha1 = store.insert_json_auto_hash(data)
            restored = store.retrieve_json(sha1)
            assert restored == data
        """
    )
    proc = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr

