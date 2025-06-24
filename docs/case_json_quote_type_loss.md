## 方法2（CASE式＋json\_quote）による型保持問題の説明

### 概要

SQLiteのFTS5テーブル設計において、`element_value`カラムに配列要素を保存する方法として2つのアプローチが検討された。Method 2では、SQL側の`CASE`式と`json_quote()`関数を用いて、インサート時にJSONリテラルを生成しようとしたが、以下の理由により**テスト配列のすべての要素型を正しく保存・復元できない**問題がある。

### テスト配列

```python
[42, 3.14, None, True, False, 'hello', 'true', 'false', 'null', '', 0, -0, 1, -1, '0', '1']
```

### Method 2 のCASE式

```sql
CASE
  WHEN ? IS NULL THEN NULL
  WHEN typeof(?) IN ('integer','real') THEN ?
  WHEN lower(?) IN ('true','false') THEN lower(?)
  ELSE json_quote(?)
END
```

### 問題点

1. **Pythonブール値の扱い**

   * Pythonの`True`/`False`はSQLiteにバインドされると整数`1`/`0`として扱われる。
   * `typeof(?) IN ('integer','real')` の分岐が先に評価されるため、ブール値も数値分岐に入り、`1`/`0`として保存される。
   * その結果、元のブール型が失われ、JSONパース後も`1`/`0`の整数として復元される。

2. **文字列リテラル"true"/"false"の誤変換**

   * リテラル文字列`'true'`/`'false'`も最終的に`lower(?) IN ('true','false')`分岐に入り、JSON真偽値として扱われる。
   * したがって、元の文字列としての`'"true"'`/`'"false"'`が失われ、JSONパース後にPythonの`True`/`False`となる。

3. **数値と文字列"0"/"1"の競合**

   * リテラル文字列`'0'`/`'1'`は数値分岐で扱われ、整数`0`/`1`として保存される。
   * 元の文字列`'"0"'`/`'"1"'`の形が保持できない。

4. **NULLと文字列"null"の混同**

   * `WHEN ? IS NULL THEN NULL`によりSQL NULLは保存できるが、リテラル文字列`'null'`は`ELSE json_quote(?)`分岐に入り、文字列`'"null"'`として保存される。
   * SQL NULLと文字列"null"の区別は可能だが、動作が複雑でエラーの元となる。

### 結論

Method 2のアプローチでは、SQLiteの型アフィニティや`CASE`式の評価順序により、**ブール型、文字列リテラル、数値リテラル間の区別が担保できず**、元の配列要素型を完全に復元できない。

このため、すべての要素型を保証するには、\*\*Method 1（すべての要素をPython側で`json.dumps`し、JSONリテラルとして保存）\*\*を採用すべきである。
