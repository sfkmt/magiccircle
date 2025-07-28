# Magic Circle 改善作業指示書

このドキュメントは、Magic Circleフレームワークの改善のための作業指示書です。
@sfkmtの別プロジェクトで実証済みの改善内容をまとめています。

## 改善内容の概要

1. **GitHub Issues自動作成機能** - tasksフェーズ承認時の自動化
2. **Claude Code Actions統合ドキュメント** - MAXプランでの完全自動化
3. **不要なワークフローの削除** - エラー通知の防止

## 作業手順

### 1. GitHub Issues自動作成機能の追加

#### 1.1 ディレクトリ作成
```bash
mkdir -p .mc/hooks
mkdir -p .mc/scripts
```

#### 1.2 post-approveフックの作成
ファイル: `.mc/hooks/post-approve.sh`

```bash
#!/bin/bash
# Magic Circle Post-Approve Hook
# このフックは/mc:spec-approveコマンドでフェーズが承認された後に自動実行されます

# 環境変数から情報を取得
FEATURE_NAME="${MC_FEATURE_NAME:-}"
PHASE="${MC_PHASE:-}"
SPEC_FILE="${MC_SPEC_FILE:-}"

echo "🔄 Post-approve hook triggered for $FEATURE_NAME - $PHASE phase"

# tasksフェーズが承認された場合、GitHub Issuesを自動作成
if [ "$PHASE" = "tasks" ]; then
    echo "📋 Tasks phase approved. Creating GitHub Issues..."
    
    # GitHub CLIがインストールされているか確認
    if ! command -v gh &> /dev/null; then
        echo "⚠️  GitHub CLI (gh) is not installed. Please install it first:"
        echo "   brew install gh"
        echo "   gh auth login"
        exit 1
    fi
    
    # GitHub認証状態を確認
    if ! gh auth status &> /dev/null; then
        echo "⚠️  Not authenticated with GitHub. Please run:"
        echo "   gh auth login"
        exit 1
    fi
    
    # タスクファイルの存在確認
    TASKS_FILE=".mc/specs/$FEATURE_NAME/tasks.md"
    if [ -f "$TASKS_FILE" ]; then
        echo "📄 Found tasks file: $TASKS_FILE"
        
        # Pythonスクリプトを使用してGitHub Issuesを作成
        if [ -f ".mc/scripts/create_github_issues.py" ]; then
            python3 .mc/scripts/create_github_issues.py "$FEATURE_NAME"
        else
            echo "❌ GitHub Issues creation script not found"
            echo "   Please ensure .mc/scripts/create_github_issues.py exists"
        fi
        
        echo "✅ GitHub Issues creation process completed"
    else
        echo "❌ Tasks file not found: $TASKS_FILE"
        exit 1
    fi
fi

# その他のフェーズ承認時の処理
case "$PHASE" in
    "requirements")
        echo "📝 Requirements approved. Ready for design phase."
        ;;
    "design")
        echo "🏗️  Design approved. Ready for task generation."
        ;;
esac

echo "✨ Post-approve hook completed"
```

#### 1.3 GitHub Issues作成スクリプト
ファイル: `.mc/scripts/create_github_issues.py`

```python
#!/usr/bin/env python3
"""
Magic Circle - GitHub Issues自動作成スクリプト
tasks.mdファイルを解析してGitHub Issuesを作成します
"""

import os
import re
import json
import subprocess
import sys
from typing import List, Dict, Optional

def parse_tasks_file(file_path: str) -> List[Dict]:
    """tasks.mdファイルを解析してタスク情報を抽出"""
    tasks = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # タスクの詳細情報パターン
    detail_pattern = r'(T\d+):.+?\n\s+- 見積もり: (.+?)\n\s+- 依存: (.+?)\n\s+- 詳細: (.+?)(?=\n\n|\n- \[ \]|$)'
    
    # 全タスクの詳細を抽出
    for match in re.finditer(detail_pattern, content, re.DOTALL):
        task_id, estimate, dependencies, details = match.groups()
        
        # タスク名を取得
        task_name_match = re.search(f'{task_id}: (.+?)(?:\n|$)', content)
        task_name = task_name_match.group(1) if task_name_match else task_id
        
        # セクション名を取得
        section_match = re.search(r'### \d+\. (.+?)\n.*?' + re.escape(task_id), content, re.DOTALL)
        section = section_match.group(1) if section_match else "その他"
        
        tasks.append({
            'id': task_id,
            'name': task_name.strip(),
            'section': section,
            'estimate': estimate.strip(),
            'dependencies': [d.strip() for d in dependencies.split(',') if d.strip() != 'なし'],
            'details': details.strip()
        })
    
    return tasks

def create_github_issue(task: Dict, feature_name: str, task_to_issue_map: Dict[str, int]) -> Optional[int]:
    """GitHub CLIを使ってIssueを作成"""
    # ラベルの決定
    labels = [feature_name, 'task']
    
    # 見積もり時間によるラベル
    if 'h' in task['estimate']:
        hours_match = re.search(r'(\d+(?:\.\d+)?)', task['estimate'])
        if hours_match:
            hours = float(hours_match.group(1))
            if hours <= 1:
                labels.append('effort/small')
            elif hours <= 3:
                labels.append('effort/medium')
            else:
                labels.append('effort/large')
    
    # セクションによるラベル
    section_labels = {
        'セットアップ': 'setup',
        'インフラ': 'infrastructure',
        'データベース': 'database',
        'API': 'api',
        'テスト': 'testing',
        'ドキュメント': 'documentation'
    }
    
    for key, label in section_labels.items():
        if key in task['section']:
            labels.append(label)
            break
    
    # Issue本文の作成
    body = f"""## タスク: {task['name']}

**タスクID**: {task['id']}
**セクション**: {task['section']}
**見積もり時間**: {task['estimate']}

### 詳細
{task['details']}

### 依存関係
"""
    
    if task['dependencies']:
        for dep in task['dependencies']:
            if dep in task_to_issue_map:
                body += f"- #{task_to_issue_map[dep]} ({dep})\n"
            else:
                body += f"- {dep} (Issue未作成)\n"
    else:
        body += "- なし\n"
    
    body += f"\n---\n*このIssueはMagic Circleによって自動生成されました*"
    
    # GitHub CLIコマンドの構築
    cmd = [
        'gh', 'issue', 'create',
        '--title', f"[{task['id']}] {task['name']}",
        '--body', body
    ]
    
    # ラベルが存在する場合のみ追加
    existing_labels = get_existing_labels()
    for label in labels:
        if label in existing_labels:
            cmd.extend(['--label', label])
    
    try:
        # Issueを作成
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # 作成されたIssue番号を抽出
        issue_url = result.stdout.strip()
        issue_number = int(issue_url.split('/')[-1])
        
        print(f"✅ Created Issue #{issue_number} for {task['id']}: {task['name']}")
        return issue_number
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create issue for {task['id']}: {e}")
        print(f"   Error: {e.stderr}")
        return None

def get_existing_labels() -> set:
    """既存のラベルを取得"""
    try:
        result = subprocess.run(
            ['gh', 'label', 'list', '--json', 'name', '-L', '100'],
            capture_output=True,
            text=True,
            check=True
        )
        labels = json.loads(result.stdout)
        return {label['name'] for label in labels}
    except:
        return set()

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_github_issues.py <feature-name>")
        sys.exit(1)
    
    feature_name = sys.argv[1]
    tasks_file = f".mc/specs/{feature_name}/tasks.md"
    
    if not os.path.exists(tasks_file):
        print(f"❌ Tasks file not found: {tasks_file}")
        sys.exit(1)
    
    print(f"📄 Parsing tasks from: {tasks_file}")
    tasks = parse_tasks_file(tasks_file)
    print(f"📋 Found {len(tasks)} tasks")
    
    # 依存関係の順序でソート
    def get_dependency_level(task, level=0):
        if not task['dependencies']:
            return level
        max_level = level
        for dep_id in task['dependencies']:
            dep_task = next((t for t in tasks if t['id'] == dep_id), None)
            if dep_task:
                max_level = max(max_level, get_dependency_level(dep_task, level + 1))
        return max_level
    
    tasks.sort(key=lambda t: (get_dependency_level(t), t['id']))
    
    # タスクIDからIssue番号へのマッピング
    task_to_issue_map = {}
    
    print("\n🚀 Creating GitHub Issues...")
    created_count = 0
    for task in tasks:
        issue_number = create_github_issue(task, feature_name, task_to_issue_map)
        if issue_number:
            task_to_issue_map[task['id']] = issue_number
            created_count += 1
    
    # 結果の保存
    if created_count > 0:
        result_file = f".mc/specs/{feature_name}/github_issues.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(task_to_issue_map, f, indent=2)
        
        print(f"\n✨ Created {created_count} issues")
        print(f"📁 Issue mapping saved to: {result_file}")
    else:
        print("\n⚠️  No issues were created. Check if labels exist.")
        print("   Run 'gh label create <label-name>' to create missing labels")

if __name__ == "__main__":
    main()
```

#### 1.4 フックのREADME
ファイル: `.mc/hooks/README.md`

```markdown
# Magic Circle Hooks

このディレクトリには、Magic Circleの各種イベントで自動実行されるフックスクリプトが含まれています。

## 利用可能なフック

### post-approve.sh
`/mc:spec-approve` コマンドでフェーズが承認された後に自動実行されます。

**環境変数:**
- `MC_FEATURE_NAME`: 機能名（例: api-core）
- `MC_PHASE`: 承認されたフェーズ（requirements | design | tasks）
- `MC_SPEC_FILE`: spec.jsonファイルのパス

**現在の動作:**
- tasksフェーズが承認されると、GitHub Issuesを自動作成

## セットアップ手順

### 1. GitHub CLIのインストール
```bash
# macOS
brew install gh

# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 2. GitHub認証
```bash
gh auth login
```

### 3. 必要なラベルの作成（推奨）
```bash
# 基本ラベル
gh label create task --description "Task from Magic Circle"

# 工数ラベル
gh label create effort/small --description "Small effort (≤1h)"
gh label create effort/medium --description "Medium effort (2-3h)"
gh label create effort/large --description "Large effort (>3h)"

# カテゴリラベル
gh label create setup --description "Setup and configuration"
gh label create infrastructure --description "Infrastructure related"
gh label create database --description "Database related"
gh label create api --description "API related"
gh label create testing --description "Testing related"
gh label create documentation --description "Documentation related"
```

### 4. フックの有効化
フックは自動的に有効になりますが、実行権限を確認してください：
```bash
chmod +x .mc/hooks/post-approve.sh
chmod +x .mc/scripts/create_github_issues.py
```

## 手動実行

フックを手動でテストする場合：
```bash
# 環境変数を設定して実行
MC_FEATURE_NAME=my-feature \
MC_PHASE=tasks \
MC_SPEC_FILE=.mc/specs/my-feature/spec.json \
./.mc/hooks/post-approve.sh
```

## カスタマイズ

### 他のフェーズでの処理追加
`post-approve.sh` の case文に処理を追加できます：
```bash
case "$PHASE" in
    "requirements")
        # 要件承認時の処理
        echo "📧 Sending notification email..."
        ;;
    "design")
        # 設計承認時の処理  
        echo "📚 Publishing design docs..."
        ;;
esac
```

### Issue作成のカスタマイズ
`.mc/scripts/create_github_issues.py` を編集して：
- ラベルのマッピングを変更
- Issue本文のフォーマットを変更
- マイルストーンやアサイニーの自動設定を追加

## トラブルシューティング

### GitHub CLIが見つからない
```
⚠️  GitHub CLI (gh) is not installed
```
→ 上記のインストール手順を実行してください

### GitHub認証エラー
```
⚠️  Not authenticated with GitHub
```
→ `gh auth login` を実行してください

### Pythonスクリプトエラー
Python 3.6以上が必要です：
```bash
python3 --version
```

---

*Magic Circle Hooks - 開発プロセスの自動化*
```

#### 1.5 実行権限の設定
```bash
chmod +x .mc/hooks/post-approve.sh
chmod +x .mc/scripts/create_github_issues.py
```

### 2. Claude Code Actions統合ドキュメントの追加

ファイル: `docs/claude-code-actions-integration.md`

```markdown
# Claude Code GitHub Actions 統合ガイド

Magic CircleフレームワークとClaude Code GitHub Actionsを統合することで、仕様書駆動開発を完全に自動化できます。

## 前提条件

- Claude Code MAXプラン（無制限のGitHub Actions利用）
- GitHub CLI（`gh`）のインストール
- GitHubリポジトリへの書き込み権限

## セットアップ手順

### 1. Claude Codeのバージョン確認

```bash
claude --version
```

v1.0.44以上が必要です。

### 2. GitHub App のインストール

Claude Code内で以下のコマンドを実行：

```
/install-github-app
```

これにより：
- GitHub Appがインストールされる
- 認証トークンが自動設定される
- `.github/workflows/claude.yml`が作成される

### 3. ワークフローのカスタマイズ（オプション）

日本語対応やプロジェクト固有の設定を追加する場合：

```yaml
# .github/workflows/claude.yml に追加
custom_instructions: |
  あなたは日本語で応答するClaude Codeです。
  
  以下のルールに従ってください：
  1. すべてのコメント、PR説明、コミットメッセージは日本語で記述する
  2. コードのコメントも日本語で記述する
  3. 絵文字を適切に使用して親しみやすくする
```

### 4. 不要なワークフローの削除

Magic CircleテンプレートからCloneした場合、以下のファイルは削除してください：

```bash
rm .github/workflows/spec-driven-dev.yml
rm .github/workflows/auto-review.yml
```

これらは未設定のままだとエラー通知を大量に送信する原因となります。

## 使用方法

### 基本的な使い方

IssueやPRにコメントして`@claude`をメンションすると、Claude Codeが自動的に実装を開始します：

```
@claude このIssueのタスクを実装してください
```

### Magic Circleワークフローとの統合

1. **仕様書作成**: `/mc:spec-init` → `/mc:spec-requirements` → `/mc:spec-design` → `/mc:spec-tasks`
2. **タスク承認**: `/mc:spec-approve tasks`
3. **自動Issue作成**: post-approveフックによりGitHub Issuesが自動作成される
4. **並列実装**: 各Issueに`@claude`メンションでコメントすることで並列実装

### 並列実装の例

```bash
# 複数のIssueに同時にコメント
gh issue comment 1 --body "@claude タスクT001を実装してください"
gh issue comment 4 --body "@claude タスクT004を実装してください"
gh issue comment 5 --body "@claude タスクT005を実装してください"
```

## GitHub Issues自動作成機能

### セットアップ

1. **フックスクリプトの配置**
   ```bash
   chmod +x .mc/hooks/post-approve.sh
   chmod +x .mc/scripts/create_github_issues.py
   ```

2. **必要なラベルの作成**
   ```bash
   gh label create task
   gh label create effort/small
   gh label create effort/medium
   gh label create effort/large
   ```

### 動作の流れ

1. `tasks`フェーズが承認される
2. `post-approve.sh`フックが自動実行
3. `create_github_issues.py`がtasks.mdを解析
4. 依存関係を考慮した順序でGitHub Issuesを作成
5. 各IssueにClaude Codeがコメントされると自動実装開始

## トラブルシューティング

### Claude Codeが反応しない

- GitHub Appが正しくインストールされているか確認
- ワークフローファイルが最新バージョンか確認
- `@claude`メンションが正しく含まれているか確認

### エラー通知メールが大量に届く

- 不要なワークフローファイルを削除
- 特に`spec-driven-dev.yml`と`auto-review.yml`

### Issueが作成されない

- GitHub CLIの認証状態を確認: `gh auth status`
- 必要なラベルが存在するか確認: `gh label list`

## 実証済みの効果

[@sfkmt](https://github.com/sfkmt)の別プロジェクトでの実証結果：
- 28個のタスクを自動的にGitHub Issues化
- 並列実装により開発時間を大幅短縮
- 仕様書に基づいた一貫性のある実装

## 注意事項

- Claude Code MAXプランではAPI KEY不要（GitHub App経由で認証）
- 実装されたコードは必ず人間によるレビューが必要
- 依存関係のあるタスクは適切な順序で実装すること

---

*Magic Circle + Claude Code Actions = 完全自動化された仕様書駆動開発*
```

### 3. 不要なワークフローの削除

以下のファイルを削除：
- `.github/workflows/spec-driven-dev.yml`
- `.github/workflows/auto-review.yml`

削除理由：
- 存在しないCLIツールを参照している
- Issue作成時にエラー通知を大量送信する原因となる

## コミットメッセージ例

### PR 1: GitHub Issues自動作成機能
```
feat: GitHub Issues自動作成機能を追加

- tasksフェーズ承認時にGitHub Issuesを自動作成
- 依存関係を考慮した順序でIssue作成
- 適切なラベル付けとフォーマット
- @sfkmtの別プロジェクトで実証済み
```

### PR 2: Claude Code Actions統合ドキュメント
```
docs: Claude Code Actions統合ガイドを追加

- MAXプランでのセットアップ手順
- 並列タスク実装の方法
- トラブルシューティング
- @sfkmtの別プロジェクトで実証済み
```

### PR 3: 不要なワークフロー削除
```
fix: 未設定のワークフローファイルを削除

- spec-driven-dev.yml: 存在しないCLIツールを参照
- auto-review.yml: 未設定のレビューワークフロー

これらがIssue作成時にエラー通知を大量送信する原因でした。
@sfkmtの別プロジェクトで問題を確認・解決済み。
```

## 実装の効果

- **自動化**: tasksフェーズ承認後、自動的にGitHub Issuesが作成される
- **並列実装**: Claude Codeにより複数タスクを同時に実装可能
- **品質向上**: 仕様書に基づいた一貫性のある実装
- **時間短縮**: 手動でのIssue作成が不要になり、開発速度が向上

---

*この作業指示書に従って、Magic Circleフレームワークを改善してください。*