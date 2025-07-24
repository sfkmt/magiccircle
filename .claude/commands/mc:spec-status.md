# Check Project Status

プロジェクト全体の進捗状況を確認します。各機能の仕様書作成状況と承認状態を一覧表示します。

## 実行内容

1. `.gd/specs/`内のすべての機能をスキャン
2. 各機能のspec.jsonを読み込み
3. 進捗サマリーを表示

## プロンプト

プロジェクトの仕様書作成状況を確認します。

1. `.gd/specs/`ディレクトリ内のすべてのサブディレクトリをスキャン
2. 各機能のspec.jsonを読み込んで状態を確認
3. 以下の形式でステータスレポートを生成：

```markdown
# プロジェクト仕様書ステータス

## 概要
- 総機能数: X
- 完了機能数: Y
- 進行中機能数: Z

## 機能別ステータス

### ✅ [機能名1]
- 作成日: YYYY-MM-DD
- Requirements: ✅ Approved (YYYY-MM-DD)
- Design: ✅ Approved (YYYY-MM-DD)
- Tasks: ✅ Approved (YYYY-MM-DD)
- 状態: 実装可能

### 🔄 [機能名2]
- 作成日: YYYY-MM-DD
- Requirements: ✅ Approved (YYYY-MM-DD)
- Design: 📝 Draft
- Tasks: ⏳ Pending
- 状態: Design レビュー待ち

### 📋 [機能名3]
- 作成日: YYYY-MM-DD
- Requirements: 📝 Draft
- Design: ⏳ Pending
- Tasks: ⏳ Pending
- 状態: Requirements レビュー待ち

## 推奨アクション
1. [機能名2]: design.mdのレビューと承認が必要です
2. [機能名3]: requirements.mdのレビューと承認が必要です

## 統計
- 平均リードタイム: X日（仕様作成開始から承認完了まで）
- 最速完了: [機能名] (Y日)
- 最長滞留: [機能名] (Z日)
```

凡例：
- ✅ Approved: 承認済み
- 📝 Draft: ドラフト作成済み（レビュー待ち）
- ⏳ Pending: 未作成
- 🔄 進行中の機能