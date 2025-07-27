# Changelog

All notable changes to the MC (Magic Circle) Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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