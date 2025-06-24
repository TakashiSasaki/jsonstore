# arraystore

Pythonリスト（配列）を**型を保ったままSQLiteデータベースに保存・復元**するためのシンプルなライブラリです。また、同じ仕組みでPython辞書を扱う``objectstore``モジュールも提供します。
各要素をJSONリテラルとして保存することで、数値・真偽値・null・文字列・ネスト配列・辞書など、Pythonの型を損なわずに格納できます。

## 特徴

- Pythonリストの**すべての型情報を保持**してSQLiteに格納
- ネストした配列や辞書もサポート
- SQLiteの標準機能のみで動作
- シンプルなAPI
- Python辞書を保存・復元できる `objectstore` モジュールを同梱

## インストール

```sh
pip install .
# または poetry を利用
poetry install
```

## 使い方

```python
import sqlite3
from arraystore.main import create_array_table, insert_array, retrieve_array

# SQLite接続
conn = sqlite3.connect("example.db")
conn.row_factory = sqlite3.Row

# テーブル作成（任意でテーブル名を指定）
create_array_table(conn, table_name="my_arrays")

# 配列を保存
my_array = [42, 3.14, None, True, False, "hello", [1, 2], {"a": 1}]
canonical_json_sha1 = "my_array_hash"
insert_array(conn, canonical_json_sha1, my_array, table_name="my_arrays")

# 配列を復元
restored = retrieve_array(conn, canonical_json_sha1, table_name="my_arrays")
print(restored)  # 元の配列と同じ型・値で復元されます

conn.close()
```

### objectstore モジュールによる辞書の保存

`objectstore` は、辞書の各プロパティを JSON リテラルとして保存することで、
キーや値の型を損なわずに復元できるモジュールです。配列と同様の使い勝手で利用
できます。

```python
import sqlite3
from objectstore.main import create_object_table, insert_object, retrieve_object

conn = sqlite3.connect("example.db")
conn.row_factory = sqlite3.Row

create_object_table(conn, table_name="my_objects")

my_obj = {"name": "Alice", "age": 30, "flags": [True, False]}
canonical_json_sha1 = "my_obj_hash"
insert_object(conn, canonical_json_sha1, my_obj, table_name="my_objects")

restored = retrieve_object(conn, canonical_json_sha1, table_name="my_objects")
print(restored)  # 元の辞書と同じ型・値で復元されます

conn.close()
```

## API

- [`create_array_table(conn, table_name="arraystore")`](arraystore/main.py):
  配列格納用テーブルを作成します。`table_name` で任意のテーブル名を指定できます。

- [`insert_array(conn, canonical_json_sha1, array, table_name="arraystore")`](arraystore/main.py):
  配列を指定ハッシュ（ID）で保存します。`table_name` で保存先テーブルを指定します。

- [`retrieve_array(conn, canonical_json_sha1, table_name="arraystore")`](arraystore/main.py):
  指定ハッシュの配列を復元します。`table_name` を揃えることで任意のテーブルから取得できます。

- [`create_object_table(conn, table_name="objectstore")`](objectstore/main.py):
  辞書格納用テーブルを作成します。`table_name` で任意のテーブル名を指定できます。

- [`insert_object(conn, canonical_json_sha1, obj, table_name="objectstore")`](objectstore/main.py):
  辞書を指定ハッシュで保存します。`table_name` で保存先テーブルを指定します。

- [`retrieve_object(conn, canonical_json_sha1, table_name="objectstore")`](objectstore/main.py):
  指定ハッシュの辞書を復元します。`table_name` を揃えることで任意のテーブルから取得できます。

## テスト

```sh
pytest tests/
```

## 注意

- 配列要素の順序・型・値が完全に保持されます。
- SQLiteのTEXT型カラムに**JSONリテラル**として保存するため、型の混同や変換ロスがありません。
- 詳細な技術的背景や他方式との比較は [case_json_quote_type_loss.md](docs/case_json_quote_type_loss.md) を参照してください。

## ライセンス

MIT License
