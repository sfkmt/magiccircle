# View Iteration Status

Goal-Oriented Self-Regulation Frameworkにおける現在のイテレーション状態と
プロジェクト全体の進化を可視化します。

## 前提条件
- プロジェクトが初期化されていること

## 実行内容

1. 現在のイテレーション状態を表示
2. 過去のイテレーション履歴を集計
3. ゴールへの進捗を可視化
4. 次のステップの提案

## プロンプト

Goal-Oriented Self-Regulation Frameworkの状態を確認します。

1. `.mc/specs/*/iteration-history.md`を読み込み
2. `.mc/specs/*/tasks.md`から現在のイテレーション情報を取得
3. 以下の形式で状態レポートを生成：

```markdown
# Goal-Oriented Self-Regulation Status Report

## プロジェクトゴール
[最終目標の明確な記述]

## 現在のイテレーション
- **番号**: イテレーション #[n]
- **状態**: [計画中/実行中/フィードバック待ち]
- **開始日**: [日付]
- **目標**: [このイテレーションの目標]

### 進行中のタスク
- [ ] [タスク名] - [進捗%]
- [x] [完了タスク] - 完了

## イテレーション履歴
| # | 期間 | 目標 | 結果 | 学習事項 |
|---|------|------|------|----------|
| 1 | [期間] | [目標] | [結果] | [学び] |
| 2 | [期間] | [目標] | [結果] | [学び] |

## 進捗メトリクス
- **全体進捗**: [%]
- **完了イテレーション**: [n]回
- **平均サイクルタイム**: [時間]
- **デプロイ成功率**: [%]

## フィードバックループ分析
### 頻出する課題
1. [パターン化された問題]

### 成功パターン
1. [効果的だったアプローチ]

## 次のステップ（推奨）
Based on feedback patterns:
1. [推奨アクション1]
2. [推奨アクション2]

## ゴールまでの推定
- **残りイテレーション**: 約[n]回
- **推定完了時期**: [予測]
- **リスク要因**: [特定されたリスク]
```

**可視化のポイント**:
- 各イテレーションの成果を明確に示す
- フィードバックから得られたパターンを抽出
- ゴールへの道筋を常に意識させる
- 継続的改善のサイクルを可視化