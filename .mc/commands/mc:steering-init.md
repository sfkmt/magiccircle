# /mc:steering-init

プロジェクトのステアリング文書を初期化し、GitHub環境をセットアップします。

## 実行内容

1. **GitHubリポジトリの確認**
   - 現在のディレクトリがGitリポジトリかチェック
   - リモートリポジトリの設定を確認

2. **初期コミットの作成**
   - 必要に応じて初期コミットを作成
   - .gitignoreファイルの設定

3. **GitHub App接続確認**
   - Claude Code GitHub Appの接続状態を確認
   - 未接続の場合は接続手順を案内

4. **ステアリング文書の作成**
   - プロジェクトの方向性と目的を定義
   - `.mc/steering/README.md`を生成

## 使用方法

```bash
/mc:steering-init
```

## プロンプト

AIアシスタントへの指示：

1. まず以下のGitHub環境チェックを実行してください：
   ```bash
   # Gitリポジトリかチェック
   git rev-parse --git-dir 2>/dev/null
   
   # リモートリポジトリの確認
   git remote -v
   
   # 現在のブランチと状態
   git branch --show-current
   git status --porcelain
   ```

2. Gitリポジトリでない場合は初期化：
   ```bash
   git init
   ```

3. 初期コミットが必要な場合：
   ```bash
   # .gitignoreの作成（既存でなければ）
   echo "# Spec-driven development metadata
.mc/cache/
.mc/logs/
.mc/tmp/
*.tmp
*.log
.DS_Store
node_modules/
.env
.env.local" > .gitignore
   
   # 初期コミット
   git add .
   git commit -m "Initial commit: Setup spec-driven development"
   ```

4. GitHub App接続確認：
   ```bash
   # gh CLIでの認証状態確認
   gh auth status
   
   # リポジトリ情報の取得
   gh repo view --json name,owner,url
   ```

5. 接続が確認できたら、以下のステアリング文書を`.mc/steering/README.md`として作成してください：

```markdown
# Project Steering Document

## プロジェクト概要
[プロジェクトの簡潔な説明]

## ビジョン
[長期的な目標とビジョン]

## 主要な目標
- [ ] [目標1]
- [ ] [目標2]
- [ ] [目標3]

## 技術方針
### アーキテクチャ
[採用するアーキテクチャパターン]

### 技術スタック
- 言語: [使用する言語]
- フレームワーク: [使用するフレームワーク]
- ツール: [開発ツール]

## 開発プロセス
- 仕様書駆動開発（Spec-Driven Development）
- GitHub Actions統合によるタスク自動実行
- PRベースのレビュープロセス

## 品質基準
- コードカバレッジ: [目標%]
- パフォーマンス基準: [基準]
- セキュリティ要件: [要件]

## GitHub設定
- リポジトリ: [owner/repo]
- デフォルトブランチ: [branch]
- Claude Code App: [接続状態]

## 作成日
[YYYY-MM-DD]

## 最終更新日
[YYYY-MM-DD]
```

6. 必要に応じてユーザーに以下を案内：
   - GitHub App未接続の場合: `/install-github-app`コマンドの実行を推奨
   - リモートリポジトリ未設定の場合: GitHubでのリポジトリ作成手順

すべてのステップを完了したら、プロジェクトのGitHub環境設定が完了したことを報告してください。