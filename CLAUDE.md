# Claude Code Spec-Driven Development

このプロジェクトは、Claude Codeを使用した仕様書駆動開発（Spec-Driven Development）を実践します。

## 概要

このプロジェクトでは、以下の3段階承認プロセスを通じて、品質の高いソフトウェア開発を実現します：

1. **要件定義フェーズ** - 機能の要件を明確に定義
2. **技術設計フェーズ** - 実装方法の技術的な設計
3. **タスク生成フェーズ** - 実装に必要なタスクの生成

## ディレクトリ構造

```
.mc/
├── steering/          # プロジェクトのステアリング文書
│   └── README.md      # プロジェクトの方向性と目的
└── specs/            # 機能仕様書
    └── [feature-name]/
        ├── spec.json       # フェーズ承認状態の追跡
        ├── requirements.md # 機能要件
        ├── design.md      # 技術設計
        └── tasks.md       # 実装タスク
```

## 利用可能なスラッシュコマンド

### 基本コマンド
- `/mc:steering-init` - ステアリング文書の初期化
- `/mc:steering-update` - ステアリング文書の更新
- `/mc:spec-init` - 新機能の仕様書作成開始
- `/mc:spec-requirements` - 要件定義文書の生成
- `/mc:spec-design` - 技術設計文書の作成
- `/mc:spec-tasks` - 実装タスクの生成
- `/mc:spec-status` - 現在のプロジェクト進捗確認
- `/mc:spec-approve` - フェーズの承認

### SOW統合コマンド
- `/mc:sow-create` - 作業用SOWの生成
- `/mc:task-execute` - SOWベースのタスク実行
- `/mc:spec-diff` - 仕様書の差分表示
- `/mc:context-optimize` - AIコンテキストの最適化

### GitHub Actions連携コマンド
- `/mc:github-issue-create` - 承認済みタスクからGitHubイシューを自動作成
- `/mc:workflow-trigger` - GitHub Actionsワークフローを手動トリガー
- `/mc:feedback-analyze` - 実装結果を分析してパターンを抽出

## 開発フロー

1. **ステアリング文書の作成**（推奨）
   - `/mc:steering-init`を実行してプロジェクトの方向性を定義

2. **機能仕様の作成**
   - `/mc:spec-init [feature-name]`で新機能の仕様書作成を開始
   - 各フェーズでAIが文書を生成し、人間がレビュー・承認

3. **自動実装（GitHub Actions統合）**
   - `/mc:github-issue-create [spec-name]`でタスクをGitHubイシュー化
   - Claude Code GitHub Actionsが自動的にタスクを実行
   - 各タスクの実装結果がPRとして作成される
   - 自動レビューによる品質チェック

4. **フィードバックと学習**
   - `/mc:feedback-analyze [spec-name] --pr [number]`で実装を分析
   - パターンとインサイトが自動的に蓄積
   - 次回の開発で活用される

## 重要な原則

- **フェーズをスキップしない** - 各フェーズは順番に完了させる
- **人間によるレビュー必須** - AIが生成した文書は必ず人間がレビュー
- **承認の明示的な記録** - spec.jsonで各フェーズの承認状態を管理

## 自動化機能

### Hooks統合
- **事前検証**: 承認前に仕様書の品質を自動チェック
- **事後処理**: 承認後にGitHubイシュー作成やCI/CDトリガー
- **進捗追跡**: タスク完了時の自動更新

### GitHub Actions連携
- **並列実行**: 複数のClaude Codeインスタンスによる高速処理
- **自動PR作成**: 実装結果は自動的にPRとして提出
- **品質保証**: 自動レビューによる仕様適合性チェック

### フィードバックループ
- **パターン学習**: 成功した実装パターンを自動抽出
- **エラー分析**: 頻出するエラーを特定し改善提案
- **継続的改善**: 蓄積された知見を次の開発に活用

## 注意事項

- 仕様書は`.mc/specs/`ディレクトリに自動的に整理されます
- 各機能の承認状態は`spec.json`で追跡されます
- ステアリング文書は定期的に更新し、プロジェクトの方向性を維持します
- GitHub Actions利用にはサブスクリプションプランのClaude Codeが必要です
- Hooksは`.mc/hooks/`で設定可能です