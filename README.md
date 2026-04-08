# calculator

Pythonとプログラム構造の学習用に少しずつ機能追加してきた、四則演算ベースの計算アプリです。  
単に式を計算するだけでなく、`tokenize -> parse -> AST -> evaluate` の流れを分けて実装しており、構文解析やテスト、CI の練習題材として扱いやすい形になっています。

## このプロジェクトの特筆ポイント

- `src/calculator/` 配下で責務を分割
  - `tokenizer.py`: 入力文字列をトークン化
  - `parser.py`: 再帰下降パーサで AST を構築
  - `ast_nodes.py`: `NumberNode` / `BinaryOpNode` / `UnaryOpNode`
  - `evaluator.py`: AST を評価
  - `errors.py`: 独自例外 `CalculationError` と `ErrorCode`
- 学習用に AST を可視化できる
  - CLI 実行時は AST のツリー表示と評価ログが出るため、式がどう解釈されたか確認しやすいです
- 演算子の優先順位を実装
  - `()`
  - `^`（右結合）
  - 単項マイナス
  - `* / %`
  - `+ -`
- エラーをコード付きで扱う
  - 0 除算、未知の演算子、不正な数値、不正な式、AST 構造エラーなどを `ErrorCode` で判別できます

## 現在できること

- 対応演算子: `+`, `-`, `*`, `/`, `%`, `^`
- 括弧つき式の評価
- 単項マイナス
- 小数の計算
- エラー時のメッセージ表示

入力例:

```text
2 + 3 * 4
(2 + 3) * 4
-2^2
(-2)^2
11 % 3
```

## はじめ方

### 前提

- Python `3.12` 以上
- `uv`

### セットアップ

```bash
uv sync
```

`uv.lock` を含めて管理しているので、依存関係を揃えやすい構成です。

### 起動方法

このプロジェクトは `src` レイアウトなので、CLI 起動時は `PYTHONPATH=src` を付けるのが確実です。

```bash
env PYTHONPATH=src uv run python -m calculator.main
```

終了する場合:

```text
exit
```

実行イメージ:

```text
Simple Calculator
Format: number operator number (e.g. 2 + 3)
Type 'exit' to quit
>> 2 + 3 * 4

==== AST ====

└── BinaryOp(+)
  ├── Number(2.0)
  └── BinaryOp(*)
    ├── Number(3.0)
    └── Number(4.0)

====     ====

Evaluating: (2.0 + (3.0 * 4.0))
  Evaluating: 2.0
   -> 2.0
  Evaluating: (3.0 * 4.0)
    Evaluating: 3.0
     -> 3.0
    Evaluating: 4.0
     -> 4.0
   -> 3.0 * 4.0 = 12.0
 -> 2.0 + 12.0 = 14.0
2 + 3 * 4 = 14.0
```

## テスト

`pytest` でロジックを確認できます。現時点では 46 件のテストが通る状態です。

```bash
uv run pytest
```

カバレッジ付きで確認する場合:

```bash
uv run pytest --cov=calculator --cov-report=term
```

主に次の観点をテストしています。

- 基本計算
- 演算子の優先順位
- 括弧
- 単項マイナス
- 不正入力と例外コード
- AST ノードの基本動作

## Lint / Format / pre-commit

コード品質チェックには `ruff` と `pre-commit` を使っています。

```bash
uv run ruff check .
uv run ruff format --check .
uv run pre-commit run --all-files
```

初回だけ hook を入れる場合:

```bash
uv run pre-commit install
```

## CI

GitHub Actions の `.github/workflows/ci.yml` で CI を動かしています。

実行内容:

- Python `3.12`
- `uv sync`
- `ruff check`
- `ruff format --check`
- `pytest`
- `pytest --cov=calculator --cov-report=term`

トリガー:

- `develop` ブランチへの `push`
- `main` / `develop` 向けの `pull_request`

## ディレクトリ構成

```text
calculator/
├── src/calculator/
│   ├── ast_nodes.py
│   ├── errors.py
│   ├── evaluator.py
│   ├── main.py
│   ├── operators.py
│   ├── parser.py
│   └── tokenizer.py
├── tests/
├── .github/workflows/ci.yml
├── .pre-commit-config.yaml
├── pyproject.toml
└── uv.lock
```

## 補足

- `pytest` では `pyproject.toml` の `pythonpath = ["src"]` を使って `src` 配下を import しています
- 一方、CLI の直接起動はその設定を自動では見ないため、README では `PYTHONPATH=src` 付きの起動方法を案内しています
- 学習用の実装なので、今後エントリポイント定義やパッケージングを追加すると、起動方法はさらに整理できます
