# AIコンテキスト最適化コマンド

Claude Codeへ提供するコンテキストを最適化し、実行効率と精度を向上させます。

## 使用方法
```
/mc:context-optimize [spec-name] [--task-id <id>] [--strategy <strategy>] [--analyze]
```

## オプション
- `--task-id`: 特定タスクのコンテキストのみ最適化
- `--strategy`: 最適化戦略（minimal|balanced|comprehensive）デフォルト: balanced
- `--analyze`: 最適化前にコンテキスト分析レポートを生成

## 最適化戦略

### minimal（最小限）
- タスク実行に必須の情報のみ含める
- トークン使用量を最小化
- 高速実行が必要な場合に最適

### balanced（バランス）
- 必要な情報と関連コンテキストを含める
- パフォーマンスと理解度のバランス
- 通常の開発タスクに推奨

### comprehensive（包括的）
- 広範囲の関連情報を含める
- 複雑なリファクタリングや設計変更に最適
- より正確な実装が期待できる

## 主要機能

### 1. 動的コンテキスト選択
```bash
/mc:context-optimize user-auth --task-id task-001
```
- タスクの種類に応じて必要なファイルを自動選択
- 依存関係グラフから関連コードを抽出
- 不要なコメントや空白を除去

### 2. コンテキスト分析
```bash
/mc:context-optimize user-auth --analyze
```
出力例：
```
Context Analysis Report: user-auth
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Files: 45
Relevant Files: 12
Token Estimate: 8,500

File Relevance Score:
- src/auth/auth.controller.ts    [████████████] 95%
- src/auth/auth.service.ts       [███████████ ] 90%
- src/models/user.model.ts       [██████████  ] 85%
- src/utils/jwt.utils.ts         [████████    ] 70%
- tests/auth.test.ts             [██████      ] 60%

Optimization Suggestions:
✓ Remove unused imports in auth.service.ts (-200 tokens)
✓ Extract interface definitions to separate file (-350 tokens)
✓ Use file summaries for test files (-1,200 tokens)
```

### 3. コンテキストキャッシング
- 頻繁に使用されるコンテキストをキャッシュ
- ファイル変更を自動検知してキャッシュ更新
- 実行時間を最大50%短縮

## 高度な最適化技術

### セマンティック圧縮
```bash
/mc:context-optimize user-auth --strategy minimal --semantic-compress
```
- コードの意味を保持しながら圧縮
- 型定義の簡略化
- 重複コードの参照化

### 段階的コンテキスト拡張
```bash
/mc:context-optimize user-auth --progressive
```
- 初回は最小コンテキストで実行
- エラー時に関連コンテキストを追加
- 成功するまで段階的に拡張

### パターンベース最適化
```bash
/mc:context-optimize user-auth --learn-patterns
```
- 過去の実行から最適なコンテキストパターンを学習
- 類似タスクに対して学習済みパターンを適用
- プロジェクト固有の最適化ルールを生成

## 統合使用例

### SOWベース実行との連携
```bash
# SOW生成時にコンテキストを最適化
/mc:sow-create user-auth | /mc:context-optimize --strategy balanced

# 最適化されたコンテキストで実行
/mc:task-execute user-auth --use-optimized-context
```

### CI/CD環境での使用
```yaml
- name: Optimize Context for Speed
  run: |
    /mc:context-optimize $SPEC_NAME --strategy minimal
    /mc:task-execute $SPEC_NAME --mode automated
```

### デバッグモード
```bash
# 最適化プロセスの詳細ログ
MC_DEBUG=true /mc:context-optimize user-auth --verbose
```

## パフォーマンス指標
```
Optimization Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Original Context Size: 45,000 tokens
Optimized Context Size: 12,000 tokens
Reduction: 73%

Execution Time Comparison:
- Without optimization: 4m 30s
- With optimization: 1m 45s
- Speed improvement: 61%

Accuracy Metrics:
- Test pass rate: 100%
- Type check pass: 100%
- Lint warnings: 0
```