# テーブル構造

`arraystore` モジュールと `objectstore` モジュールで使用される SQLite テーブルの構造について説明します。

## 配列保存テーブル (`create_array_table`)

`create_array_table()` 関数が生成するテーブルは次の定義になります。

```sql
CREATE TABLE IF NOT EXISTS {table_name} (
    canonical_json_sha1 TEXT NOT NULL,
    element_index       INTEGER NOT NULL,
    element_json        TEXT,
    element_json_sha1   TEXT,
    PRIMARY KEY (canonical_json_sha1, element_index)
);
CREATE INDEX IF NOT EXISTS idx_{table_name}_hash
    ON {table_name}(canonical_json_sha1);
```

- `canonical_json_sha1`: 配列全体をカノニカル JSON 形式でハッシュ化した値。配列 ID として機能します。
- `element_index`: 配列要素のインデックス (0 から開始)。
- `element_json`: 各要素を JSON リテラルとして保存した値。
- `element_json_sha1`: 各要素の JSON を SHA1 ハッシュ化した値。

主キーは `(canonical_json_sha1, element_index)` であり、同一配列内の各要素を一意に識別します。また、`canonical_json_sha1` での検索を高速化するために専用インデックスが作成されます。

## 辞書保存テーブル (`create_object_table`)

`create_object_table()` 関数は、辞書データを保存するために次のテーブルを作成します。

```sql
CREATE TABLE IF NOT EXISTS {table_name} (
    canonical_json_sha1 TEXT NOT NULL,
    property_name       TEXT NOT NULL,
    property_json       TEXT,
    property_json_sha1  TEXT,
    PRIMARY KEY (canonical_json_sha1, property_name)
);
CREATE INDEX IF NOT EXISTS idx_{table_name}_hash
    ON {table_name}(canonical_json_sha1);
```

- `canonical_json_sha1`: 辞書全体のカノニカル JSON ハッシュ。
- `property_name`: 辞書のキー名。
- `property_json`: 各値を JSON リテラルとして保存したもの。
- `property_json_sha1`: 各値の JSON を SHA1 ハッシュ化したもの。

主キーは `(canonical_json_sha1, property_name)` です。こちらもハッシュ値にインデックスを張ることで、同一オブジェクトを高速に取得できます。

## テーブル名

どちらのモジュールもデフォルトでは `arraystore`、`objectstore` というテーブル名を利用しますが、各関数の `table_name` 引数を指定することで任意の名前のテーブルを使用できます。
