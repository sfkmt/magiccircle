# Claude Code Spec-Driven Development

このプロジェクトは、Claude Codeを使用した仕様書駆動開発（Spec-Driven Development）を実践します。

## 概要

このプロジェクトでは、以下の3段階承認プロセスを通じて、品質の高いソフトウェア開発を実現します：

1. **要件定義フェーズ** - 機能の要件を明確に定義
2. **技術設計フェーズ** - 実装方法の技術的な設計
3. **タスク生成フェーズ** - 実装に必要なタスクの生成

## ディレクトリ構造

```
.mc/
├── steering/          # プロジェクトのステアリング文書
│   └── README.md      # プロジェクトの方向性と目的
└── specs/            # 機能仕様書
    └── [feature-name]/
        ├── spec.json       # フェーズ承認状態の追跡
        ├── requirements.md # 機能要件
        ├── design.md      # 技術設計
        └── tasks.md       # 実装タスク
```

## 利用可能なスラッシュコマンド

### 基本コマンド
- `/mc:steering-init` - ステアリング文書の初期化
- `/mc:steering-update` - ステアリング文書の更新
- `/mc:spec-init` - 新機能の仕様書作成開始
- `/mc:spec-requirements` - 要件定義文書の生成
- `/mc:spec-design` - 技術設計文書の作成
- `/mc:spec-tasks` - 実装タスクの生成
- `/mc:spec-status` - 現在のプロジェクト進捗確認
- `/mc:spec-approve` - フェーズの承認

### SOW統合コマンド
- `/mc:sow-create` - 作業用SOWの生成
- `/mc:task-execute` - SOWベースのタスク実行
- `/mc:spec-diff` - 仕様書の差分表示
- `/mc:context-optimize` - AIコンテキストの最適化

## 開発フロー

1. **ステアリング文書の作成**（推奨）
   - `/mc:steering-init`を実行してプロジェクトの方向性を定義

2. **機能仕様の作成**
   - `/mc:spec-init [feature-name]`で新機能の仕様書作成を開始
   - 各フェーズでAIが文書を生成し、人間がレビュー・承認

3. **実装**
   - 承認されたタスクに基づいて実装を進める
   - 定期的に`/mc:spec-status`で進捗を確認

## 重要な原則

- **フェーズをスキップしない** - 各フェーズは順番に完了させる
- **人間によるレビュー必須** - AIが生成した文書は必ず人間がレビュー
- **承認の明示的な記録** - spec.jsonで各フェーズの承認状態を管理

## 注意事項

- 仕様書は`.mc/specs/`ディレクトリに自動的に整理されます
- 各機能の承認状態は`spec.json`で追跡されます
- ステアリング文書は定期的に更新し、プロジェクトの方向性を維持します