# /mc:github-issue-create

承認されたタスクから自動的にGitHubイシューを作成し、イテレーション計画と統合します。

## 使用方法

```bash
/mc:github-issue-create [spec-name] [options]
```

## オプション

- `--sprint [number]`: 割り当てるスプリント番号
- `--milestone [name]`: GitHubマイルストーン名
- `--deploy-target [env]`: デプロイ環境（dev/staging/prod）
- `--priority [level]`: 優先度（high/medium/low）
- `--batch-size [number]`: バッチサイズ（並列実行用）
- `--dry-run`: 実際に作成せずプレビュー

## プロンプト

AIアシスタントへの指示：

1. 前提条件の確認：
   ```bash
   # タスクフェーズが承認済みか確認
   cat .mc/specs/[spec-name]/spec.json | jq '.phases.tasks.status'
   
   # 現在のスプリント情報を取得
   cat .mc/iterations/current.json 2>/dev/null || echo "No active sprint"
   
   # GitHub認証状態確認
   gh auth status
   ```

2. タスクの解析と分類：
   ```bash
   # tasks.mdを読み込み
   cat .mc/specs/[spec-name]/tasks.md
   ```
   
   各タスクを以下のタイプに自動分類：
   - ✨ `feature`: 新機能の実装
   - 🐛 `bug`: バグ修正
   - 🔧 `refactor`: リファクタリング
   - 📚 `docs`: ドキュメント更新
   - 🧪 `test`: テストの追加・修正
   - 🏗️ `infra`: インフラ・設定変更

3. ストーリーポイントの自動計算：
   - 見積時間 1-2時間: 1ポイント
   - 見積時間 3-4時間: 2ポイント
   - 見積時間 5-8時間: 3ポイント
   - 見積時間 8時間以上: 5ポイント

4. 各タスクに対してGitHub Issueを作成：
   ```bash
   gh issue create \
     --title "[TASK-XXX] [タスク名]" \
     --body "[詳細な説明]" \
     --label "spec-driven,type:[type],priority:[priority],sp:[points]" \
     --milestone "[milestone]" \
     --project "[project-board]" \
     --assignee "@me"
   ```

5. 依存関係の設定：
   ```bash
   # 依存関係をコメントで記録
   gh issue comment [issue-number] --body "Depends on #[dep-issue]"
   ```

6. スプリント割り当て：
   ```bash
   # プロジェクトボードに追加
   gh project item-add [project-id] --owner [owner] --url [issue-url]
   ```

7. デプロイ情報の記録：
   ```bash
   # カスタムフィールドに環境を設定
   gh api graphql -f query='mutation {
     updateProjectV2ItemFieldValue(
       input: {
         projectId: "[project-id]"
         itemId: "[item-id]"
         fieldId: "[deploy-field-id]"
         value: { text: "[deploy-target]" }
       }
     ) { projectV2Item { id } }
   }'
   ```

8. 実行結果のサマリー生成：
   ```markdown
   ## GitHub Issues 作成完了
   
   ### 作成されたIssue
   | タスクID | Issue番号 | タイプ | SP | スプリント | デプロイ対象 |
   |----------|-----------|--------|----|-----------|--------------|
   | TASK-001 | #123 | feature | 3 | Sprint-5 | staging |
   
   ### スプリント情報更新
   - 追加されたストーリーポイント: [total]
   - 現在のスプリント総SP: [current]
   - スプリントキャパシティ: [capacity]
   
   ### 次のステップ
   - [ ] プロジェクトボードで優先順位を調整
   - [ ] 各Issueにアサイニーを設定
   - [ ] CI/CDワークフローの設定
   ```

9. イテレーション記録の更新：
   ```bash
   # iterations/current.jsonを更新
   jq '.issues += [新しいIssue情報]' .mc/iterations/current.json > temp.json
   mv temp.json .mc/iterations/current.json
   ```

10. CHANGELOG.mdへの記録：
    ```bash
    # 新機能として記録
    echo "### Added\n- [spec-name]: GitHub Issues created for implementation (#[first-issue]-#[last-issue])" >> CHANGELOG.md
    ```

## 統合機能

### タイプ駆動の自動分類
- コミットメッセージ規約に従ったプレフィックス
- 自動的に適切なラベルとテンプレートを選択

### イテレーション駆動の管理
- スプリントキャパシティの自動計算
- バーンダウンチャート用データの生成
- ベロシティトラッキング

### デプロイ駆動の連携
- 環境別のデプロイパイプライン設定
- リリースノートの自動準備
- ステージング→本番のプロモーションフロー

## エラーハンドリング
- API制限に達した場合は自動的に待機
- 重複Issue作成の防止
- 失敗したIssueのリトライ機能