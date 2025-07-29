# Claude Code Spec-Driven Development

このプロジェクトは、Claude Codeを使用した仕様書駆動開発（Spec-Driven Development）を実践します。

## 現在のステータス
_最終更新: [/mc:spec-status で自動更新されます]_

### アクティブな作業
- **仕様**: [未設定]
- **フェーズ**: [未設定]
- **GitHub Issue**: [未設定]
- **次のアクション**: `/mc:steering-init`

### スプリント情報
- **現在**: [未設定]
- **進捗**: 0/0 SP
- **終了予定**: [未設定]

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
├── specs/            # 機能仕様書
│   └── [feature-name]/
│       ├── spec.json       # フェーズ承認状態の追跡
│       ├── requirements.md # 機能要件
│       ├── design.md      # 技術設計
│       └── tasks.md       # 実装タスク
├── iterations/       # スプリント管理
│   ├── current.json  # 現在のスプリント情報
│   ├── sprint-*.json # スプリント履歴
│   └── metrics.json  # ベロシティ等のメトリクス
├── deploys/          # デプロイメント管理
│   ├── candidates.jsonl    # デプロイ候補
│   ├── history.jsonl      # デプロイ履歴
│   └── [env]-[version].yaml # デプロイマニフェスト
├── cache/            # 状態キャッシュ
│   └── last-status.json   # 最終状態のスナップショット
└── commands/         # コマンド定義
    └── mc:*.md       # 各コマンドの詳細仕様
```

## 利用可能なスラッシュコマンド

### 基本コマンド
- `/mc:steering-init` - ステアリング文書の初期化（GitHub環境セットアップ含む）
- `/mc:steering-update` - ステアリング文書の更新
- `/mc:spec-init` - 新機能の仕様書作成開始
- `/mc:spec-requirements` - 要件定義文書の生成
- `/mc:spec-design` - 技術設計文書の作成
- `/mc:spec-tasks` - 実装タスクの生成
- `/mc:spec-status` - 現在のプロジェクト進捗確認（再開機能強化版）
- `/mc:spec-approve` - フェーズの承認

### イテレーション管理コマンド
- `/mc:iteration-plan` - スプリント計画の作成・管理
  - `create` - 新しいスプリント作成
  - `update` - 進捗更新
  - `close` - スプリント終了とレトロスペクティブ
  - `status` - 現在の状況表示
- `/mc:github-issue-create` - GitHub Issue自動作成（スプリント・デプロイ統合）

### デプロイ管理コマンド
- `/mc:deploy-prepare` - デプロイメント準備とリリース管理
  - 環境別設定（dev/staging/prod）
  - リリースノート自動生成
  - ロールバック計画

### SOW統合コマンド
- `/mc:sow-create` - 作業用SOWの生成
- `/mc:task-execute` - SOWベースのタスク実行
- `/mc:spec-diff` - 仕様書の差分表示
- `/mc:context-optimize` - AIコンテキストの最適化

### 分析コマンド
- `/mc:feedback-analyze` - 実装フィードバック分析
- `/mc:quality-check` - 品質チェック
- `/mc:workflow-trigger` - ワークフロートリガー

## 開発フロー

1. **ステアリング文書の作成**（必須）
   - `/mc:steering-init`を実行してGitHub環境をセットアップ
   - プロジェクトの方向性を定義

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
- **現在地の正確な把握** - `/mc:spec-status --sync`で常に最新状態を確認
- **変更履歴の追跡** - CHANGELOG.mdとリリースノートですべてを記録

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

## 5つの駆動方式の統合

### 1. 仕様書駆動（Spec-Driven）
- 3段階承認プロセスによる品質管理
- AIアシスタントによる文書生成支援
- 人間のレビューと承認

### 2. GitHub Issue駆動（Issue-Driven）
- タスク承認後の自動Issue作成
- 依存関係の管理と可視化
- PRとの自動連携

### 3. イテレーション駆動（Iteration-Driven）
- スプリント計画とベロシティ追跡
- バーンダウンチャートと進捗可視化
- レトロスペクティブによる改善

### 4. タイプ駆動（Type-Driven）
- タスクの自動分類（feature/bug/refactor/docs/test/infra）
- タイプ別のテンプレートとワークフロー
- コミットメッセージ規約の自動適用

### 5. デプロイ駆動（Deploy-Driven）
- 環境別のデプロイパイプライン
- リリースノートの自動生成
- ロールバック計画と監視設定

## 注意事項

- 仕様書は`.mc/specs/`ディレクトリに自動的に整理されます
- 各機能の承認状態は`spec.json`で追跡されます
- ステアリング文書は定期的に更新し、プロジェクトの方向性を維持します
- GitHub Actions利用にはサブスクリプションプランのClaude Codeが必要です
- Hooksは`.mc/hooks/`で設定可能です
- **Claude Code再起動時**: 必ず`/mc:spec-status --resume`を実行して現在地を確認

## クイックスタート

### 新規プロジェクトの場合
```bash
# 1. GitHub環境のセットアップとステアリング文書作成
/mc:steering-init

# 2. 最初の機能仕様を作成
/mc:spec-init my-first-feature

# 3. 要件定義を生成
/mc:spec-requirements

# 4. レビュー後、承認
/mc:spec-approve requirements

# 5. 以降、design → tasks と進める
```

### Claude Code再起動時
```bash
# 1. 現在地の確認と同期
/mc:spec-status --sync

# 2. 再開用のコンテキスト取得
/mc:spec-status --resume

# 3. 推奨されたコマンドを実行
```

### スプリント開始時
```bash
# 1. 新しいスプリントを作成
/mc:iteration-plan create --sprint-length 14 --capacity 40

# 2. タスクをGitHub Issueとして作成
/mc:github-issue-create [spec-name] --sprint 1

# 3. 進捗を追跡
/mc:iteration-plan status
```

### デプロイ準備時
```bash
# 1. デプロイ準備（staging環境）
/mc:deploy-prepare staging --release-notes

# 2. 本番デプロイ準備
/mc:deploy-prepare prod --version v2.4.0 --rollback-plan
```

## トラブルシューティング

### 状態が不明な場合
```bash
/mc:spec-status --sync --detailed
```

### GitHubとの同期エラー
```bash
gh auth status  # 認証状態確認
gh auth login   # 再認証
```

### スプリント情報が見つからない
```bash
/mc:iteration-plan status  # 現在のスプリント確認
/mc:iteration-plan create  # 新規作成
```

---
# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.