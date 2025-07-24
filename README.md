# Claude Code Spec-Driven Development

Claude Codeに最適化された仕様書駆動開発（Spec-Driven Development）フレームワークです。

## 概要

このプロジェクトは、[Kiro](https://kiro.io/)の仕様書駆動開発プロセスをClaude Codeのスラッシュコマンドで再現したものです。AIによる文書生成と人間によるレビューを組み合わせて、高品質なソフトウェア開発を実現します。

## 特徴

- 🎯 **3段階承認プロセス**: 要件定義 → 技術設計 → タスク生成
- 🤖 **AI支援**: Claude Codeが各フェーズの文書を自動生成
- 👥 **人間のレビュー必須**: 各フェーズで人間による承認が必要
- 📁 **整理された構造**: 仕様書は自動的に整理・管理
- 🔄 **ステアリング文書**: プロジェクトの方向性を継続的に管理

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
/kiro:steering-init

# 2. 新機能の仕様書作成開始
/kiro:spec-init feature-name

# 3. 要件定義の生成
/kiro:spec-requirements

# 4. 要件の承認
/kiro:spec-approve feature-name requirements

# 5. 技術設計の生成
/kiro:spec-design

# 6. 設計の承認
/kiro:spec-approve feature-name design

# 7. タスクの生成
/kiro:spec-tasks

# 8. タスクの承認
/kiro:spec-approve feature-name tasks

# 9. 進捗確認
/kiro:spec-status
```

## ディレクトリ構造

```
your-project/
├── .claude/
│   └── commands/          # スラッシュコマンド定義
│       ├── kiro:steering-init.md
│       ├── kiro:steering-update.md
│       ├── kiro:spec-init.md
│       ├── kiro:spec-requirements.md
│       ├── kiro:spec-design.md
│       ├── kiro:spec-tasks.md
│       ├── kiro:spec-status.md
│       └── kiro:spec-approve.md
├── .kiro/
│   ├── steering/          # ステアリング文書
│   │   └── README.md
│   └── specs/            # 機能仕様書
│       └── [feature-name]/
│           ├── spec.json       # フェーズ承認状態
│           ├── requirements.md # 要件定義
│           ├── design.md      # 技術設計
│           └── tasks.md       # 実装タスク
└── CLAUDE.md             # Claude Code設定
```

## スラッシュコマンド一覧

| コマンド | 説明 |
|---------|------|
| `/kiro:steering-init` | プロジェクトのステアリング文書を初期化 |
| `/kiro:steering-update` | ステアリング文書を更新 |
| `/kiro:spec-init [name]` | 新機能の仕様書作成を開始 |
| `/kiro:spec-requirements` | 要件定義文書を生成 |
| `/kiro:spec-design` | 技術設計文書を生成 |
| `/kiro:spec-tasks` | 実装タスクを生成 |
| `/kiro:spec-approve [name] [phase]` | 指定フェーズを承認 |
| `/kiro:spec-status` | プロジェクト全体の進捗確認 |

## ワークフロー

### 1. 要件定義フェーズ
- AIが機能要件と非機能要件を整理
- ユーザーストーリーと受け入れ基準を定義
- 人間がレビューして承認

### 2. 技術設計フェーズ
- アーキテクチャとデータモデルを設計
- API仕様とコンポーネント構成を定義
- テスト戦略とデプロイ計画を策定

### 3. タスク生成フェーズ
- 実装可能な単位にタスクを分割
- 依存関係と見積もり時間を設定
- 実装順序の推奨を提供

## ベストプラクティス

1. **フェーズをスキップしない**: 各フェーズは重要な役割があります
2. **承認は慎重に**: 一度承認したら基本的に戻さない
3. **ステアリング文書を活用**: プロジェクトの方向性を定期的に確認
4. **spec.jsonを信頼**: フェーズの状態管理はシステムに任せる

## 貢献

Issues や Pull Requests を歓迎します。新しいスラッシュコマンドの提案や改善案があれば、ぜひお知らせください。

## ライセンス

MIT License

## 謝辞

このプロジェクトは[Kiro](https://kiro.io/)の仕様書駆動開発の概念に基づいています。