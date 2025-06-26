# クラスメソッド一覧

このドキュメントでは、`ArrayStore`、`ObjectStore`、`JsonStore` の各クラスが提供するメソッドを表形式でまとめます。

## ArrayStore クラス

| メソッド | 説明 |
| --- | --- |
| `__init__(conn, *, table_name="arraystore", view_name="arraystore_element_concat", fts_table_name="arraystore_element_fts")` | テーブル・ビュー・FTS テーブルを作成して初期化します。 |
| `insert_array(canonical_json_sha1, array)` | 指定されたハッシュ ID で配列を保存します。 |
| `insert_array_auto_hash(array)` | 配列のカノニカル JSON SHA1 を計算して保存し、計算したハッシュを返します。 |
| `insert_arrays_auto_hash(arrays)` | 複数の配列を一度に保存し、それぞれのハッシュ値を返します。 |
| `retrieve_array(canonical_json_sha1)` | 指定されたハッシュ ID の配列を復元します。 |
| `retrieve_all_arrays()` | 保存されているすべての配列をリストで取得します。 |
| `create_view()` | 要素を連結したビューを作成します。 |
| `create_fts()` | FTS5 仮想テーブルを作成します。 |

## ObjectStore クラス

| メソッド | 説明 |
| --- | --- |
| `__init__(conn, *, table_name="objectstore", view_name="objectstore_property_concat", fts_table_name="objectstore_property_fts")` | テーブル・ビュー・FTS テーブルを作成して初期化します。 |
| `insert_object(canonical_json_sha1, obj)` | 指定されたハッシュ ID で辞書を保存します。 |
| `insert_object_auto_hash(obj)` | 辞書のカノニカル JSON SHA1 を計算して保存し、計算したハッシュを返します。 |
| `insert_objects_auto_hash(objs)` | 複数の辞書を一度に保存し、それぞれのハッシュ値を返します。 |
| `retrieve_object(canonical_json_sha1)` | 指定されたハッシュ ID の辞書を復元します。 |
| `retrieve_all_objects()` | 保存されているすべての辞書をリストで取得します。 |
| `create_view()` | プロパティを連結したビューを作成します。 |
| `create_fts()` | FTS5 仮想テーブルを作成します。 |

## JsonStore クラス

| メソッド | 説明 |
| --- | --- |
| `__init__(conn, *, table_name="jsonstore", fts_table_name="jsonstore_fts")` | テーブル・FTS テーブルを作成して初期化します。 |
| `insert_json(canonical_json_sha1, obj)` | 指定されたハッシュ ID で JSON データを保存します。 |
| `insert_json_auto_hash(obj)` | JSON データのカノニカル SHA1 を計算して保存し、計算したハッシュを返します。 |
| `insert_jsons_auto_hash(objs)` | 複数の JSON データを一度に保存し、それぞれのハッシュ値を返します。 |
| `retrieve_json(canonical_json_sha1)` | 指定されたハッシュ ID の JSON データを復元します。 |
| `retrieve_all_json()` | 保存されているすべての JSON データをリストで取得します。 |
| `create_fts()` | FTS5 仮想テーブルを作成します。 |

