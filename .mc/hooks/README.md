# Magic Circle Hooks

このディレクトリには、Magic Circleの各種イベントで自動実行されるフックスクリプトが含まれています。

## 🔄 自動同期機能

**重要**: すべてのフックでプロジェクト状態（CLAUDE.mdとCHANGELOG.md）が自動的に更新されます。

## 利用可能なフック

### post-approve.sh
`/mc:spec-approve` コマンドでフェーズが承認された後に自動実行されます。
- ✅ プロジェクト状態を自動同期
- 📋 tasksフェーズ承認時はGitHub Issuesを自動作成

### post-spec-generate.sh
仕様書生成後（requirements, design, tasks）に自動実行されます。
- ✅ プロジェクト状態を自動同期

### post-task-complete.sh
タスク完了時（Issue close時など）に自動実行されます。
- ✅ プロジェクト状態を自動同期
- 📊 進捗状況を表示

**トリガー方法:**
1. **GitHub Actions** (推奨) - `.github/workflows/magic-circle-sync.yml`が自動実行
2. **手動監視** - `python .mc/scripts/watch_github_issues.py` でリアルタイム監視
3. **定期チェック** - `python .mc/scripts/check_closed_issues.py` で最近の変更確認

### Git Hooks
#### pre-commit
Gitコミット前に自動実行されます。
- ✅ CLAUDE.mdとCHANGELOG.mdを自動更新してステージング
- 💡 `git commit --no-verify` で一時的に無効化可能

#### post-commit
Gitコミット後に自動実行されます。
- 📝 重要な変更があった場合にヒントを表示

## セットアップ

### 1. 基本セットアップ
```bash
# フックの実行権限を設定
chmod +x .mc/hooks/*.sh
chmod +x .mc/scripts/*.py

# Git Hooksをインストール
.mc/hooks/setup-git-hooks.sh
```

### 2. GitHub CLI認証
```bash
gh auth login
```

### 3. GitHub Actions有効化
リポジトリで自動的に有効になります。Issue closeで自動同期されます。

## Issue完了時の自動同期

### 方法1: GitHub Actions（推奨）
- Issueがクローズされると自動的にワークフローが実行
- CLAUDE.mdとCHANGELOG.mdが自動更新
- コミットも自動実行

### 方法2: ローカル監視
```bash
# リアルタイム監視（60秒ごとにチェック）
python .mc/scripts/watch_github_issues.py

# 10秒ごとにチェックする場合
python .mc/scripts/watch_github_issues.py 10
```

### 方法3: 手動チェック
```bash
# 過去24時間にクローズされたIssueをチェック
python .mc/scripts/check_closed_issues.py

# 過去1時間の変更をチェック
python .mc/scripts/check_closed_issues.py 1
```

## トラブルシューティング

### GitHub CLIが認証されていない
```
❌ GitHub CLI is not authenticated
```
→ `gh auth login` を実行

### Python3が見つからない
```
⚠️ Python3 not found
```
→ Python 3.6以上をインストール

### 権限エラー
```bash
chmod +x .mc/hooks/*.sh
chmod +x .mc/scripts/*.py
```

---

*Magic Circle Hooks - プロジェクト状態を常に最新に保つ*