# GitHub イシュー自動作成コマンド

承認されたタスクから自動的にGitHubイシューを作成します。

## 使用方法
```
/mc:github-issue-create [spec-name]
```

## 動作
1. 指定された仕様のタスクフェーズが承認済みかチェック
2. tasks.mdからタスクリストを解析
3. 各タスクに対してGitHubイシューを作成
4. 依存関係をイシュー間でリンク
5. 適切なラベル（mc-task, spec-[name]）を付与

## 前提条件
- GitHub CLIがインストールされていること
- `gh auth login`で認証済みであること
- タスクフェーズが承認済みであること

## 実行例
```bash
/mc:github-issue-create user-auth
```

このコマンドを実行すると、user-auth仕様のすべてのタスクがGitHubイシューとして作成され、
Claude Code GitHub Actionsによる自動実行の準備が整います。