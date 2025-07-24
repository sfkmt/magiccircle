# Approve Specification Phase

仕様書の特定フェーズを承認します。承認により、次のフェーズに進むことができます。

## 使用方法
```
/gd:spec-approve [feature-name] [phase]
```

## パラメータ
- `feature-name`: 機能名
- `phase`: 承認するフェーズ（requirements | design | tasks）

## 実行内容

1. 指定されたフェーズの文書が存在することを確認
2. spec.jsonの該当フェーズを承認済みに更新
3. 承認日時を記録

## プロンプト

指定されたフェーズを承認します。

1. `.gd/specs/[feature-name]/spec.json`を読み込み
2. 指定されたフェーズの文書が存在し、statusが"draft"であることを確認
3. 以下の確認をユーザーに促す：
   - 文書の内容を十分にレビューしたか
   - 承認する準備ができているか

4. 確認が取れたら、spec.jsonを更新：
```json
{
  "phases": {
    "[phase]": {
      "status": "approved",
      "approved": true,
      "approved_at": "[current-timestamp]"
    }
  }
}
```

5. 承認完了メッセージを表示：
   - requirementsが承認された場合：「次は`/gd:spec-design`で技術設計を開始できます」
   - designが承認された場合：「次は`/gd:spec-tasks`でタスク生成を開始できます」
   - tasksが承認された場合：「仕様書が完成しました！実装を開始できます」

注意：一度承認したフェーズは、明示的な理由なく取り消すべきではありません。