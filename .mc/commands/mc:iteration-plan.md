# /mc:iteration-plan

スプリント計画を作成・管理し、イテレーション駆動開発を実現します。

## 使用方法

```bash
/mc:iteration-plan [action] [options]
```

## アクション

- `create`: 新しいスプリントを作成
- `update`: 現在のスプリントを更新
- `close`: スプリントを終了し、レトロスペクティブを生成
- `status`: 現在のスプリント状況を表示

## オプション

- `--sprint-length [days]`: スプリント期間（デフォルト: 14日）
- `--capacity [points]`: チームキャパシティ（ストーリーポイント）
- `--goals [goals]`: スプリントゴール（カンマ区切り）
- `--team-members [members]`: チームメンバー（カンマ区切り）

## プロンプト

AIアシスタントへの指示：

### 1. create アクション

```bash
# 現在の仕様書とIssueから候補を収集
gh issue list --label "spec-driven" --state open --json number,title,labels,milestone

# 前回のスプリントデータを参照
cat .mc/iterations/sprint-*.json | jq -s 'sort_by(.sprint_number) | last'
```

新しいスプリントファイルを作成：
```json
{
  "sprint_number": [number],
  "name": "Sprint [number]",
  "start_date": "[ISO-8601]",
  "end_date": "[ISO-8601]",
  "goals": [
    "[ゴール1]",
    "[ゴール2]"
  ],
  "team": {
    "members": ["[member1]", "[member2]"],
    "capacity": [total_points],
    "velocity_average": [過去3スプリントの平均]
  },
  "committed_issues": [],
  "metrics": {
    "planned_points": 0,
    "completed_points": 0,
    "added_points": 0,
    "removed_points": 0
  },
  "risks": [],
  "status": "planning"
}
```

### 2. スプリント計画の自動提案

```markdown
## Sprint [number] 計画提案

### 推奨されるIssue
基準: 優先度、依存関係、チームキャパシティ

| Issue | タイトル | タイプ | SP | 優先度 | 依存関係 |
|-------|---------|--------|-----|--------|----------|
| #123 | [title] | feature | 3 | high | なし |

### キャパシティ分析
- チーム総キャパシティ: [capacity] SP
- 推奨コミット量: [capacity * 0.8] SP（バッファ20%）
- 提案された総SP: [total] SP

### リスク評価
- [ ] 大きなタスク（5SP以上）の分割検討
- [ ] 外部依存の確認
- [ ] 技術的不確実性の評価

### スプリントゴール案
1. [機能Xの基本実装を完了]
2. [既存バグの50%削減]
```

### 3. update アクション

現在のスプリント進捗を更新：
```bash
# 完了したIssueを収集
gh issue list --label "spec-driven" --state closed --search "closed:>=$(date -d 'sprint_start' -I)"

# 進行中のIssueを更新
gh issue list --label "spec-driven" --state open --milestone "Sprint-[number]"
```

更新内容：
- バーンダウンデータの記録
- ベロシティの再計算
- リスクの更新
- ブロッカーの記録

### 4. close アクション

スプリント終了処理：
```markdown
## Sprint [number] レトロスペクティブ

### 成果
- 計画SP: [planned]
- 完了SP: [completed]
- ベロシティ: [velocity]
- 完了率: [percentage]%

### 完了したIssue
[リスト]

### 未完了のIssue（次スプリントへ）
[リスト]

### 良かった点
- [成功要因1]
- [成功要因2]

### 改善点
- [課題1] → [改善アクション]
- [課題2] → [改善アクション]

### メトリクス
- サイクルタイム平均: [days]
- PR承認時間平均: [hours]
- バグ発生率: [rate]%

### 次スプリントへの申し送り
[重要事項]
```

### 5. status アクション

現在のスプリント状況を表示：
```markdown
## Sprint [number] ダッシュボード

### 進捗サマリー
- 日数: [経過日数]/[総日数]日
- 完了SP: [completed]/[planned] SP
- 進捗率: [percentage]%
- 予測完了率: [forecast]%

### バーンダウンチャート
```
SP |
40 |\\
35 | \\
30 |  \\___
25 |      \\___
20 |          \\___  実績
15 |              \\___
10 |                  \\___
 5 |                      \\___
 0 |__________________________|
   Day 1  3  5  7  9  11 13
```

### Issue状況
| 状態 | 件数 | SP |
|------|------|-----|
| 完了 | [n] | [sp] |
| 進行中 | [n] | [sp] |
| 未着手 | [n] | [sp] |
| ブロック | [n] | [sp] |

### チームベロシティ
- 現在: [current] SP/スプリント
- 3スプリント平均: [average] SP
- トレンド: [↑上昇/→維持/↓下降]

### アラート
- [ ] [リスク項目1]
- [ ] [注意事項2]

### 日次スタンドアップ用データ
最新の更新（過去24時間）：
- 完了: [completed issues]
- 新規: [new issues]
- ブロッカー: [blockers]
```

### 6. 自動化とGitHub連携

```bash
# GitHubプロジェクトボードと同期
gh project field-list [project-id] --owner [owner]
gh project item-list [project-id] --owner [owner]

# マイルストーンの自動作成
gh api repos/{owner}/{repo}/milestones \
  --method POST \
  -f title="Sprint-[number]" \
  -f due_on="[end_date]" \
  -f description="[sprint goals]"

# 自動ラベリング
gh label create "sprint-[number]" --color "0366d6"
```

### 7. データの永続化

```bash
# current.jsonの更新
cp .mc/iterations/sprint-[number].json .mc/iterations/current.json

# 履歴の保存
mkdir -p .mc/iterations/history
cp .mc/iterations/sprint-[number].json .mc/iterations/history/

# メトリクスの集計
jq -s '[.[] | select(.status == "closed")] | 
  {
    average_velocity: (map(.metrics.completed_points) | add / length),
    average_cycle_time: (map(.metrics.average_cycle_time) | add / length)
  }' .mc/iterations/history/*.json > .mc/iterations/metrics.json
```

### 8. CHANGELOG.mdへの記録

```bash
# スプリント開始時
echo "## Sprint [number] Started - $(date -I)" >> CHANGELOG.md
echo "- Goals: [goals]" >> CHANGELOG.md
echo "- Capacity: [capacity] SP" >> CHANGELOG.md

# スプリント終了時
echo "## Sprint [number] Completed - $(date -I)" >> CHANGELOG.md
echo "- Velocity: [velocity] SP" >> CHANGELOG.md
echo "- Completed Features: [list]" >> CHANGELOG.md
```

## 統合機能

### Slackへの通知（オプション）
```bash
# 環境変数SLACK_WEBHOOK_URLが設定されている場合
curl -X POST $SLACK_WEBHOOK_URL \
  -H 'Content-type: application/json' \
  -d "{\"text\":\"Sprint [number] started with [capacity] SP capacity\"}"
```

### CI/CDトリガー
- スプリント開始時に自動テストスイートを実行
- スプリント終了時にステージング環境へのデプロイを準備

注意事項：
- スプリント期間中の変更は慎重に行う
- ベロシティは参考値として使用し、無理な詰め込みは避ける
- レトロスペクティブの内容は必ずチームで共有する