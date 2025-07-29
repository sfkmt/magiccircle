# /mc:spec-status

プロジェクトの現在地を正確に把握し、Claude Codeの再起動時でも確実に同じ地点から再開できるようにします。

## 実行内容

1. CLAUDE.mdの最新状態を確認
2. すべての仕様書の承認状態を集計
3. GitHub Issues/PRのリアルタイム状態を取得
4. 現在のスプリント情報を確認
5. 総合的な現在地レポートを生成
6. CLAUDE.mdに最新状態を記録

## 使用方法

```bash
/mc:spec-status [options]
```

## オプション

- `--sync`: GitHubと完全同期して最新状態を取得
- `--resume`: 再開用のコンテキスト情報を生成
- `--detailed`: 詳細な進捗情報を表示
- `--feature [name]`: 特定機能の詳細状態を表示

## プロンプト

AIアシスタントへの指示：

1. **現在地の完全な把握**：
   ```bash
   # CLAUDE.mdから最新ステータスを読み込み
   grep -A 20 "## 現在のステータス" CLAUDE.md || echo "Status section not found"
   
   # すべてのspec.jsonを検索して状態を集約
   find .mc/specs -name "spec.json" -type f -exec cat {} \; | jq -s '.'
   
   # 現在のスプリント情報
   cat .mc/iterations/current.json 2>/dev/null || echo "No active sprint"
   ```

2. **GitHubリアルタイム同期**：
   ```bash
   # すべてのspec-driven Issueを取得
   gh issue list --label "spec-driven" --limit 1000 --json number,title,state,labels,assignees,milestone,updatedAt,closedAt
   
   # すべてのspec-driven PRを取得
   gh pr list --label "spec-driven" --limit 1000 --json number,title,state,labels,mergedAt,updatedAt
   
   # 最近のアクティビティ
   gh api /repos/{owner}/{repo}/events --paginate | jq '[.[] | select(.type == "IssuesEvent" or .type == "PullRequestEvent")][:20]'
   ```

3. **状態マッピングの作成**：
   各仕様書とGitHub Issueを結び付け、以下の情報をまとめる：
   - 仕様書のフェーズ状態
   - 対応するIssueの状態
   - PRのマージ状態
   - 最終更新日時

4. **現在地レポートの生成**：

```markdown
# 📍 プロジェクト現在地レポート

## 🔄 最終同期
- **同期日時**: [ISO-8601 timestamp]
- **Claude Codeセッション ID**: [session-id]
- **Gitコミット**: [commit-hash]

## 🎯 現在のフォーカス
- **アクティブな仕様**: [spec-name]
- **現在のフェーズ**: [phase]
- **次のアクション**: [recommended-command]
- **ブロッカー**: [blockers]

## 📋 全体サマリー
- **アクティブな仕様書**: [数]
- **完了した機能**: [数]
- **進行中のタスク**: [数]
- **オープンなIssue**: [数]
- **オープンなPR**: [数]

## 📂 仕様書ステータス

### ✅ 完了した機能
| 機能名 | 完了日 | Issue数 | PR数 | デプロイ |
|--------|--------|---------|------|----------|
| [name] | [date] | [count] | [count] | [env] |

### 🚀 進行中の機能
| 機能名 | フェーズ | GitHub状態 | 次のステップ | 最終更新 |
|--------|----------|------------|--------------|----------|
| [name] | [phase] | [issue-status] | [next-action] | [updated] |

### 📋 計画中の機能
| 機能名 | 優先度 | 見積もり | 次のアクション |
|--------|--------|----------|----------------|
| [name] | [priority] | [effort] | [action] |

## GitHub統合状態

### Issues分析
- **タイプ別分布**:
  - 🐛 バグ: [数]
  - ✨ 機能: [数]
  - 📚 ドキュメント: [数]
  - 🔧 リファクタリング: [数]

### イテレーション進捗
- **現在のスプリント**: [Sprint X]
- **完了したストーリーポイント**: [数]
- **残りのストーリーポイント**: [数]
- **ベロシティ**: [数]

### デプロイメント状態
- **最新デプロイ**: [環境] - [日時]
- **待機中のデプロイ**: [数]
- **デプロイ頻度**: [回/週]

## 品質メトリクス
- **コードカバレッジ**: [%]
- **自動テスト成功率**: [%]
- **平均PR承認時間**: [時間]
- **平均Issue解決時間**: [日]

## 推奨アクション
1. [優先度の高いアクション]
2. [ブロッカーの解決策]
3. [次のイテレーションの計画]

## 🔧 再開用情報

### 推奨コマンド
```bash
# 現在のフォーカスに基づいた推奨アクション
[recommended-command]
```

### 重要なコンテキスト
- **作業中spec**: `.mc/specs/[spec-name]/`
- **関連Issue**: #[numbers]
- **アクティブPR**: #[numbers]

### 環境情報
- **ブランチ**: [branch-name]
- **未コミット変更**: [uncommitted-changes]
- **スプリント**: Sprint-[number] (Day [n]/[total])

## 📦 生成日時
[YYYY-MM-DD HH:MM:SS]
```

5. **CLAUDE.mdの更新**：
   ```bash
   # 現在のステータスセクションを更新
   # 既存のセクションがあれば置換、なければ追加
   ```

   CLAUDE.mdに追加する内容：
   ```markdown
   ## 現在のステータス
   _最終更新: [timestamp]_
   
   ### アクティブな作業
   - **仕様**: [spec-name]
   - **フェーズ**: [phase]
   - **GitHub Issue**: #[number]
   - **次のアクション**: `[command]`
   
   ### スプリント情報
   - **現在**: Sprint-[number]
   - **進捗**: [completed]/[total] SP
   - **終了予定**: [date]
   ```

6. **キャッシュの保存**：
   ```bash
   # 現在状態をキャッシュに保存
   mkdir -p .mc/cache
   echo '{"timestamp": "[ISO-8601]", "status": [current-status]}' > .mc/cache/last-status.json
   ```

7. **--resumeオプションの処理**：
   ```markdown
   ## 🎯 Claude Code再開用コンテキスト
   
   ### 即座に実行すべきコマンド
   ```bash
   # 1. 最新状態の確認
   /mc:spec-status --sync
   
   # 2. 推奨アクション
   [specific-command-based-on-current-state]
   ```
   
   ### 現在のコンテキスト
   - 作業中: [what-was-being-worked-on]
   - 待機中: [what-is-waiting]
   - ブロッカー: [what-is-blocking]
   
   ### 関連ファイル
   - [file-path-1]: [why-relevant]
   - [file-path-2]: [why-relevant]
   ```

8. **エラーハンドリング**：
   - GitHub APIが失敗した場合はローカル情報のみでレポート
   - ネットワークエラー時はキャッシュから情報を取得
   - 不整合がある場合は警告を表示

重要な注意事項：
- **再現性**: 同じコマンドを実行すれば同じ現在地が得られる
- **永続性**: CLAUDE.mdとキャッシュに状態を保存
- **完全性**: GitHubとローカルの両方の情報を統合
- **実用性**: 次のアクションを明確に提示