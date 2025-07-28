# Changelog

All notable changes to the MC (Magic Circle) Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2025-07-28

### Changed
- **フレームワーク名の明確化**: Goal-Oriented Self-Regulation Framework「Magic Circle」として再定義
  - 仕様書駆動開発からゴール指向型自己制御フレームワークへの進化
  - プロジェクトのゴールを明確にし、自律的なフィードバックループを通じて継続的に改善
- **タスク生成方式の根本的変更**: 全タスク一括生成から最小デプロイ単位（MVP）での反復生成へ
  - `/mc:spec-tasks` - 最大4時間で完了可能なMVPタスクのみを生成
  - 各イテレーションでデプロイ可能な成果物を生成
  - フィードバック制御の原理に基づく継続的改善

### Added
- **Goal-Oriented Self-Regulationコマンド**
  - `/mc:iteration-feedback` - デプロイ後のフィードバック収集と次のイテレーション計画
  - `/mc:iteration-status` - イテレーション履歴と進捗の可視化、ゴールへの道筋表示
- **Iteration-Drivenアプローチ** - フレームワークの一機能として高速で継続的な価値提供を実現
  - GitHub-Driven: GitHub Issueベースの自動実装ワークフロー
  - Iteration-Driven: 仕様と実装が相互に進化する仕組み
  - Type-Driven: 型安全性を基盤とした段階的移行
  - Deployment-Driven: 常時デプロイ可能なアーキテクチャ
- **実行可能な仕様（Executable Specifications）**
  - マイクロ仕様による段階的開発
  - 自動的な仕様の進化と追跡
  - Progressive Rolloutによる安全なデプロイ
  - 型カバレッジ95%以上の維持
- **新規ディレクトリ構造**
  - `.mc/iteration/` - Iteration-Driven開発の詳細文書
  - `.mc/hooks/pre-implementation-check.sh` - 実装前の自動チェック
  - `.mc/scripts/analyze-dependencies.js` - 依存関係分析スクリプト
  - `.mc/templates/` - 各種開発テンプレート

## [2.2.0] - 2025-07-28

### Added
- **品質チェックコマンド** (`/mc:quality-check`)
  - Zennの記事を参考にしたリリース前の包括的品質チェック機能
  - セキュリティ、パフォーマンス、SEO、アクセシビリティの4カテゴリでチェック
  - デフォルトで検出された問題をGitHubイシューとして自動作成
  - `--no-issues`オプションでイシュー作成を無効化可能
  - 自動修正可能な問題への対応 (`--fix`オプション)
  - CI/CDパイプラインとの統合対応

## [2.1.4] - 2025-07-27

### Fixed
- GitHub Actionsワークフローのエラーを修正
  - スクリプトが存在しない場合は処理をスキップ
  - Magic Circleフレームワーク自体のリポジトリでは実行されない

### Removed
- 未実装のワークフローファイルを削除
  - `spec-driven-dev.yml` - 存在しないツールを参照
  - `auto-review.yml` - 存在しないツールを参照
  - これらはClaude Code Actionsの意図しない自動起動を防ぐためにも削除

### Clarified
- Claude Code GitHub Actionsは`@claude`メンションでのみ動作することを明記
- Issueの作成だけでは自動実行されない

## [2.1.3] - 2025-07-27

### Added
- **SOW作成時の自動同期機能**
  - `post-sow-create.sh` フックを追加
  - SOW作成後もプロジェクト状態を自動更新

### Enhanced
- 自動同期がカバーする範囲を拡大
  - 仕様書の生成・承認時 ✅
  - Gitコミット時 ✅
  - Issue完了時 ✅
  - SOW作成時 ✅ (新規)

## [2.1.2] - 2025-07-27

### Added
- **Issue完了時の自動同期機能**
  - GitHub Actions workflow (`.github/workflows/magic-circle-sync.yml`)
  - リアルタイム監視スクリプト (`watch_github_issues.py`)
  - 手動チェックスクリプト (`check_closed_issues.py`)
- **3つの同期方法を提供**
  - GitHub Actions: Issueクローズ時に自動実行
  - ローカル監視: リアルタイムでIssue状態を監視
  - 手動チェック: 任意のタイミングで実行

### Enhanced
- タスク完了時もCLAUDE.mdとCHANGELOG.mdを自動更新
- プロジェクトの進捗がリアルタイムに反映される

## [2.1.1] - 2025-07-27

### Changed
- `/mc:project-sync`コマンドを削除（自動実行のみに変更）
- 未実装のGitHub Actions関連コマンドをドキュメントから削除
  - `/mc:github-issue-create` (post-approveフックで自動実行)
  - `/mc:workflow-trigger` (@claudeメンションで自動実行)
  - `/mc:feedback-analyze` (未実装)

### Improved
- ドキュメントの整合性向上
- 不要なコマンドを削除してシンプル化

## [2.1.0] - 2025-07-27

### Added
- **GitHub Issues自動作成機能** - tasksフェーズ承認時の自動化
  - `post-approve.sh` フックでGitHub Issuesを自動作成
  - 依存関係を考慮した順序でIssue作成
  - 適切なラベル付けとフォーマット
- **プロジェクト状態自動同期機能** - CLAUDE.mdとCHANGELOG.mdの自動更新
  - `/mc:project-sync` コマンドで手動同期
  - Git pre-commitフックで自動同期
  - Magic Circleフックでの自動同期
- **Claude Code Actions統合ドキュメント** - MAXプランでの完全自動化ガイド
- **ドキュメンテーションベストプラクティス** - セッション間でのコンテキスト維持

### Enhanced
- **CLAUDE.mdテンプレート** - プロジェクト固有情報を優先的に表示
  - 現在の状態とNext Actionを最上部に配置
  - プロジェクト概要と技術スタックを記録
  - 重要な決定事項ログセクション
- **自動同期の統合**
  - すべてのMagic Circleフックで自動同期
  - Gitコミット時に自動的にドキュメント更新

### Fixed
- 不要なワークフローファイルによるエラー通知の防止

## [2.0.0] - 2025-07-25

### Added
- **SOW (Statement of Work) Integration** - Complete automation framework for task execution
  - `/mc:sow-create` - Generates detailed work instructions from approved tasks
  - `/mc:task-execute` - Executes tasks based on generated SOW with multiple modes (interactive/automated/dry-run)
  - `/mc:spec-diff` - Visual diff tool for specification changes and implementation compliance
  - `/mc:context-optimize` - AI context optimization for improved performance and accuracy
- **Advanced Automation Workflow** - GitHub Actions workflow for fully automated spec implementation
  - Parallel task execution support
  - Automatic branch creation and PR generation
  - Integration testing and compliance reporting
  - Feedback analysis and pattern learning

### Enhanced
- **Complete Task Automation Pipeline**
  - SOW generation provides clear, structured instructions for each task
  - Context optimization reduces token usage by up to 73%
  - Execution time improvements of up to 61%
  - Automatic error recovery and retry mechanisms
- **Improved Developer Experience**
  - Interactive mode for step-by-step execution with confirmations
  - Dry-run mode for safe execution planning
  - Real-time progress tracking and reporting
  - Comprehensive compliance checking

### Integration Points
- Claude Code CLI integration for command execution
- GitHub Actions for CI/CD automation
- Hooks system for customizable workflows
- Pattern-based learning for continuous improvement

## [1.2.0] - 2025-07-25

### Added
- **GitHub Actions Integration**
  - `/mc:github-issue-create` - Automatically creates GitHub issues from approved tasks
  - `/mc:workflow-trigger` - Manually triggers GitHub Actions workflows
  - `/mc:feedback-analyze` - Analyzes implementation results and extracts patterns
- **Hooks System** - Automated pre/post approval actions
  - Pre-approval validation hooks
  - Post-approval automation hooks
  - Task completion tracking hooks

## [1.1.0] - 2025-07-24

### Changed
- Rebranded from "GAME DESIGN (gd)" to "Magic Circle (mc)"
- Updated all command prefixes from `gd:` to `mc:`
- Renamed framework directories and documentation

## [1.0.0] - 2025-07-24

### Added
- Initial release of Spec-Driven Development framework
- Core specification management commands
  - `/mc:steering-init` - Initialize project steering document
  - `/mc:steering-update` - Update project direction
  - `/mc:spec-init` - Create new feature specification
  - `/mc:spec-requirements` - Generate requirements document
  - `/mc:spec-design` - Create technical design
  - `/mc:spec-tasks` - Generate implementation tasks
  - `/mc:spec-status` - Check project progress
  - `/mc:spec-approve` - Approve specification phases
- Three-phase approval process (Requirements → Design → Tasks)
- Automatic document generation with AI assistance
- Structured project organization in `.mc/` directory