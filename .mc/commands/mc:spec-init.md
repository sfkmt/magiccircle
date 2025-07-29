# /mc:spec-init

新機能の仕様書作成を開始します。

## 実行内容

1. 新しい機能のディレクトリ構造を作成
2. spec.jsonファイルを初期化
3. 初期テンプレートを生成

## 使用方法

```bash
/mc:spec-init [feature-name]
```

## 引数

- `feature-name`: 機能の名前（英数字とハイフンのみ）

## プロンプト

AIアシスタントへの指示：

1. 機能名の検証：
   - 英数字とハイフンのみで構成されているか確認
   - 既存の仕様書と重複していないか確認

2. ディレクトリ構造の作成：
   ```bash
   mkdir -p .mc/specs/[feature-name]
   ```

3. spec.jsonの初期化：
   ```json
   {
     "feature": "[feature-name]",
     "created": "[ISO-8601 timestamp]",
     "phases": {
       "requirements": {
         "status": "pending",
         "approvedAt": null,
         "approvedBy": null
       },
       "design": {
         "status": "pending",
         "approvedAt": null,
         "approvedBy": null
       },
       "tasks": {
         "status": "pending",
         "approvedAt": null,
         "approvedBy": null
       }
     },
     "metadata": {
       "description": "[1行の機能説明]",
       "priority": "medium",
       "estimatedEffort": null,
       "tags": []
     }
   }
   ```

4. 各フェーズのテンプレートファイルを作成：
   - requirements.md
   - design.md
   - tasks.md

5. ユーザーに次のステップを案内：
   - `/mc:spec-requirements`で要件定義を開始
   - 機能の概要を簡単に説明してもらう

注意事項：
- 機能名は明確で簡潔にする
- 既存の仕様書との整合性を保つ
- プロジェクトのステアリング文書と矛盾しないようにする