# SOWベースタスク実行コマンド

生成されたSOW（作業指示書）を基に、タスクを自動的に実行します。

## 使用方法
```
/mc:task-execute [spec-name] [--task-id <id>] [--mode <mode>] [--parallel]
```

## オプション
- `--task-id`: 特定のタスクIDのみ実行
- `--mode`: 実行モード（interactive|automated|dry-run）デフォルト: interactive
- `--parallel`: 依存関係のないタスクを並列実行

## 実行モード
### interactive（対話モード）
- 各ステップで確認を求める
- 実装内容をプレビュー可能
- エラー時に修正オプションを提示

### automated（自動モード）
- SOWに基づいて全自動実行
- エラー時は自動リトライ（最大3回）
- 実行ログを`.mc/logs/`に保存

### dry-run（ドライラン）
- 実際の変更は行わず実行計画のみ表示
- 影響を受けるファイルをリスト化
- 推定実行時間を表示

## 動作フロー
1. SOWファイルの読み込み（なければ`mc:sow-create`を自動実行）
2. 依存関係の解決と実行順序の決定
3. 各タスクに対して：
   - 必要なコンテキストの収集
   - Claude Codeによる実装
   - テストケースの実行
   - 成功基準の検証
4. 実行結果のレポート生成

## 実行例
```bash
# 対話モードで全タスク実行
/mc:task-execute user-auth

# 特定タスクを自動実行
/mc:task-execute user-auth --task-id task-001 --mode automated

# 並列実行でドライラン
/mc:task-execute user-auth --mode dry-run --parallel
```

## 統合機能
### コンテキスト最適化
- 各タスクに必要な最小限のコンテキストを自動選択
- 関連ファイルの自動読み込み
- 不要な情報のフィルタリング

### エラーハンドリング
- 型エラーの自動修正試行
- リンターエラーの自動修正
- テスト失敗時の自動デバッグ

### 進捗トラッキング
- リアルタイム進捗バー表示
- 各タスクの実行時間測定
- 成功/失敗の統計情報

## 出力例
```
Executing tasks for spec: user-auth
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1/3] task-001: Implementing auth endpoint... ✓ (2m 15s)
[2/3] task-002: Adding validation middleware... ✓ (1m 30s)
[3/3] task-003: Creating integration tests... ✓ (3m 45s)

Summary:
✓ All tasks completed successfully
⏱ Total execution time: 7m 30s
📊 Code coverage: 95%
🔍 0 linting errors, 0 type errors

Report saved to: .mc/reports/user-auth-execution-20240125.md
```

## 高度な使用法
```bash
# SOW生成と実行を一連で実行
/mc:sow-create user-auth && /mc:task-execute user-auth --mode automated

# 実行結果をGitHubイシューにコメント
/mc:task-execute user-auth --task-id task-001 | gh issue comment 123 -F -

# CI/CD環境での使用
MC_AUTO_APPROVE=true /mc:task-execute user-auth --mode automated --parallel
```