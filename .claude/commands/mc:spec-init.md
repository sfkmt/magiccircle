# Initialize Feature Specification

新しい機能の仕様書作成を開始します。このコマンドは、指定された機能名のディレクトリとspec.jsonファイルを作成します。

## 使用方法
```
/mc:spec-init [feature-name]
```

## 実行内容

1. `.gd/specs/[feature-name]/`ディレクトリを作成
2. `spec.json`ファイルを初期化（全フェーズ未承認状態）
3. 機能の基本情報を収集

## プロンプト

指定された機能名「{feature-name}」の仕様書作成を開始します。

1. `.gd/specs/{feature-name}/`ディレクトリを作成
2. 以下の内容で`spec.json`を作成：

```json
{
  "feature": "{feature-name}",
  "created_at": "{current-timestamp}",
  "phases": {
    "requirements": {
      "status": "pending",
      "approved": false,
      "approved_at": null
    },
    "design": {
      "status": "pending",
      "approved": false,
      "approved_at": null
    },
    "tasks": {
      "status": "pending",
      "approved": false,
      "approved_at": null
    }
  },
  "metadata": {
    "description": "",
    "priority": "medium",
    "estimated_effort": ""
  }
}
```

3. 機能の概要説明をユーザーに確認し、metadataに記録

これで仕様書作成の準備が整いました。次は`/mc:spec-requirements`で要件定義を開始してください。