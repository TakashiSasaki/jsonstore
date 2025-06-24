# arraystore

Pythonリスト（配列）を**型を保ったままSQLiteデータベースに保存・復元**するためのシンプルなライブラリです。  
各要素をJSONリテラルとして保存することで、数値・真偽値・null・文字列・ネスト配列・辞書など、Pythonの型を損なわずに格納できます。

## 特徴

- Pythonリストの**すべての型情報を保持**してSQLiteに格納
- ネストした配列や辞書もサポート
- SQLiteの標準機能のみで動作
- シンプルなAPI

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

# テーブル作成
create_array_table(conn)

# 配列を保存
my_array = [42, 3.14, None, True, False, "hello", [1, 2], {"a": 1}]
array_hash = "my_array_hash"
insert_array(conn, array_hash, my_array)

# 配列を復元
restored = retrieve_array(conn, array_hash)
print(restored)  # 元の配列と同じ型・値で復元されます

conn.close()
```

## API

- [`create_array_table(conn)`](arraystore/main.py):  
  配列格納用テーブルを作成します。

- [`insert_array(conn, array_hash, array)`](arraystore/main.py):  
  配列を指定ハッシュ（ID）で保存します。

- [`retrieve_array(conn, array_hash)`](arraystore/main.py):  
  指定ハッシュの配列を復元します。

## テスト

```sh
pytest tests/
```

## 注意

- 配列要素の順序・型・値が完全に保持されます。
- SQLiteのTEXT型カラムに**JSONリテラル**として保存するため、型の混同や変換ロスがありません。
- 詳細な技術的背景や他方式との比較は [method2_type_loss_in_sqlite.md](method2_type_loss_in_sqlite.md) を参照してください。

## ライセンス

MIT License
