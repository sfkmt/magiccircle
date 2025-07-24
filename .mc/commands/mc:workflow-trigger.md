# GitHub Actions ワークフロートリガーコマンド

仕様駆動開発のGitHub Actionsワークフローを手動でトリガーします。

## 使用方法
```
/mc:workflow-trigger [spec-name] [phase]
```

## パラメータ
- `spec-name`: 処理する仕様の名前
- `phase`: 実行するフェーズ（requirements, design, tasks, execute）

## 動作
1. 指定された仕様とフェーズでGitHub Actionsワークフローを起動
2. Claude Codeが自動的にタスクを処理
3. 結果はPRとして作成される

## 実行例
```bash
# タスク実行フェーズをトリガー
/mc:workflow-trigger user-auth execute

# 要件検証フェーズをトリガー
/mc:workflow-trigger payment-system requirements
```

## 注意事項
- GitHub Actionsが有効になっている必要があります
- サブスクリプションプランのClaude Codeが必要です
- 並列実行により複数のPRが作成される場合があります