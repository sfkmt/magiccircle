# Magic Circle - Goal-Oriented Self-Regulation Framework

Claude Codeに最適化されたゴール指向型自己制御フレームワーク「Magic Circle」です。

## 概要

Magic Circle（マジック・サークル）は、AIと人間の協調によるゴール指向型開発を実現するフレームワークです。仕様書駆動開発をベースに、プロジェクトのゴールを明確にし、自律的なフィードバックループを通じて継続的に改善する仕組みを提供します。

## 特徴

### コア機能
- **ゴール指向型開発**: プロジェクトのゴールを明確に定義し、達成に向けて自律的に進化
- **自己制御メカニズム**: フィードバックループを通じた継続的な改善
- **3段階承認プロセス**: 要件定義 → 技術設計 → タスク生成
- **AIと人間の協調**: Claude Codeによる自動生成と人間のレビュー

### 開発手法
- **仕様書駆動開発**: 明確な仕様を基にした実装
- **Iteration-Drivenアプローチ**: 小さな動作可能な単位での高速リリース
- **型駆動開発**: 型安全性を基盤とした堅牢な実装
- **常時デプロイ可能**: Progressive Rolloutによる安全なリリース

### 管理機能
- **ステアリング文書**: プロジェクトの方向性を継続的に管理
- **SOW統合**: 各タスクに対する精密な作業指示書を生成
- **差分管理**: 仕様変更の影響を可視化
- **コンテキスト最適化**: AIへの入力を最適化して精度向上

### 自動化機能
- **GitHub Actions統合**: 自動実装とPR作成
- **品質チェック**: リリース前の包括的な品質確認
- **フックシステム**: カスタマイズ可能なワークフロー

## クイックスタート

### 1. プロジェクトへの統合

以下の2つをあなたのプロジェクトにコピーするだけです：

```bash
# .claude/commands/ ディレクトリをコピー
cp -r .claude/commands/ /path/to/your/project/.claude/commands/

# CLAUDE.md ファイルをコピー
cp CLAUDE.md /path/to/your/project/
```

### 2. 基本的な使い方

```bash
# 1. ステアリング文書の初期化（推奨）
/mc:steering-init

# 2. 新機能の仕様書作成開始
/mc:spec-init feature-name

# 3. 要件定義の生成
/mc:spec-requirements

# 4. 要件の承認
/mc:spec-approve feature-name requirements

# 5. 技術設計の生成
/mc:spec-design

# 6. 設計の承認
/mc:spec-approve feature-name design

# 7. タスクの生成
/mc:spec-tasks

# 8. タスクの承認
/mc:spec-approve feature-name tasks

# 9. 進捗確認
/mc:spec-status
```

## ディレクトリ構造

```
your-project/
├── .claude/
│   └── commands/          # スラッシュコマンド定義
│       ├── mc:steering-init.md
│       ├── mc:steering-update.md
│       ├── mc:spec-init.md
│       ├── mc:spec-requirements.md
│       ├── mc:spec-design.md
│       ├── mc:spec-tasks.md
│       ├── mc:spec-status.md
│       └── mc:spec-approve.md
├── .mc/
│   ├── steering/          # ステアリング文書
│   │   └── README.md
│   ├── specs/            # 機能仕様書
│   │   └── [feature-name]/
│   │       ├── spec.json       # フェーズ承認状態
│   │       ├── requirements.md # 要件定義
│   │       ├── design.md      # 技術設計
│   │       └── tasks.md       # 実装タスク
│   ├── sows/             # Statement of Work
│   │   └── [feature-name]/
│   │       └── [task-id].md    # タスク別SOW
│   ├── iteration/        # Iteration-Driven開発
│   │   ├── README.md          # アプローチの説明
│   │   ├── iteration-driven-features.md
│   │   ├── github-driven-workflow.md
│   │   ├── incremental-spec-driven.md
│   │   └── always-deployable.md
│   ├── hooks/            # 自動化フック
│   │   └── pre-implementation-check.sh
│   ├── scripts/          # ユーティリティスクリプト
│   │   └── analyze-dependencies.js
│   └── templates/        # 各種テンプレート
│       ├── dependency-matrix.md
│       ├── quality-gates.md
│       └── schema-first-workflow.md
└── CLAUDE.md             # Claude Code設定
```

## スラッシュコマンド一覧

### 基本コマンド

| コマンド | 説明 |
|---------|------|
| `/mc:steering-init` | プロジェクトのステアリング文書を初期化 |
| `/mc:steering-update` | ステアリング文書を更新 |
| `/mc:spec-init [name]` | 新機能の仕様書作成を開始 |
| `/mc:spec-requirements` | 要件定義文書を生成 |
| `/mc:spec-design` | 技術設計文書を生成 |
| `/mc:spec-tasks` | 次のイテレーションのMVPタスクを生成 |
| `/mc:spec-approve [name] [phase]` | 指定フェーズを承認 |
| `/mc:spec-status` | プロジェクト全体の進捗確認 |
| `/mc:quality-check [path] [options]` | 品質チェックの実行 |
| `/mc:iteration-feedback` | イテレーションのフィードバック収集 |
| `/mc:iteration-status` | イテレーション履歴と進捗の可視化 |

### SOW統合コマンド

| コマンド | 説明 |
|---------|------|
| `/mc:sow-create [type] [target]` | 作業用SOWを生成 |
| `/mc:task-execute [feature] [task-id]` | SOWベースでタスクを実行 |
| `/mc:spec-diff [feature] [phase]` | 仕様書の差分を表示 |
| `/mc:context-optimize [target] [scope]` | AIコンテキストを最適化 |

## ワークフロー

### Goal-Oriented Self-Regulationフロー

フィードバック制御の原理に基づく継続的改善サイクル：

1. **Goal設定**: プロジェクトの最終目標を明確化
2. **Input評価**: 現在の状態と実装済み機能を把握
3. **Comparator**: ゴールと現状の差分を分析
4. **Output**: 次のMVP（最小デプロイ可能単位）を特定
5. **Effect**: 実装・デプロイを実施
6. **Feedback**: 結果を評価し次のイテレーションへ

#### 実施手順
```bash
# 1. ゴールと現状の確認
/mc:iteration-status

# 2. 次のMVPタスクの生成（最大4時間以内）
/mc:spec-tasks

# 3. タスクの承認と実装
/mc:spec-approve [name] tasks

# 4. デプロイ実施

# 5. フィードバック収集
/mc:iteration-feedback

# 6. 次のイテレーションへ（繰り返し）
```

### Iteration-Drivenアプローチ（高速実装モード）

Goal-Oriented Self-Regulationの一部として、特に高速な価値提供が必要な場合：

#### 1. マイクロ仕様（10分）
- 最小限の動作可能な仕様を定義
- 即座に実装可能なスコープに限定

#### 2. 型定義（5分）
- TypeScriptの型を先に定義
- 型カバレッジ95%以上を維持

#### 3. 実装（30分）
- 型に基づいた安全な実装
- 自動テスト付きで品質確保

#### 4. 自動デプロイ（5分）
- GitHub Actionsによる自動化
- Progressive Rolloutで安全にリリース

**結果: 50分で本番デプロイ可能な機能を実現**

### 従来の仕様駆動開発フロー（初期設計時）

大規模な機能や初期設計が必要な場合：

#### 1. 要件定義フェーズ
- AIが機能要件と非機能要件を整理
- ユーザーストーリーと受け入れ基準を定義
- 人間がレビューして承認

#### 2. 技術設計フェーズ
- アーキテクチャとデータモデルを設計
- API仕様とコンポーネント構成を定義
- テスト戦略とデプロイ計画を策定

#### 3. タスク生成フェーズ
- Goal-Oriented方式でMVP単位に分割
- 各イテレーションは4時間以内で完了可能に
- フィードバックループを組み込み

## ベストプラクティス

1. **フェーズをスキップしない**: 各フェーズは重要な役割があります
2. **承認は慎重に**: 一度承認したら基本的に戻さない
3. **ステアリング文書を活用**: プロジェクトの方向性を定期的に確認
4. **spec.jsonを信頼**: フェーズの状態管理はシステムに任せる
5. **SOWで精度向上**: タスク実行前にSOWを生成して指示を明確化
6. **差分を確認**: 仕様変更時は必ず影響範囲を確認
7. **コンテキスト最適化**: 大規模なプロジェクトではコンテキストを最適化

## 貢献

Issues や Pull Requests を歓迎します。新しいスラッシュコマンドの提案や改善案があれば、ぜひお知らせください。

## ライセンス

MIT License
