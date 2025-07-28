# 段階的品質ゲート（Progressive Quality Gates）

## 概要
各開発フェーズで満たすべき品質基準を定義し、段階的に品質を向上させます。

## フェーズ別品質ゲート

### Phase 1: 基盤構築（Foundation）
**目標**: 最低限のビルド可能性を確保

```yaml
quality_gates:
  phase1:
    - typescript_build: "tsc --noEmit が成功"
    - basic_lint: "eslint . --max-warnings 100"
    - dependencies: "npm install が成功"
    - structure: "必要なディレクトリ構造が存在"
```

### Phase 2: 型安全性（Type Safety）
**目標**: 型エラーゼロを達成

```yaml
quality_gates:
  phase2:
    - strict_types: "tsconfig.json で strict: true"
    - no_any: "型定義に any を使用しない"
    - schema_types: "DB スキーマから型を自動生成"
    - api_contracts: "OpenAPI/GraphQL スキーマ定義"
```

### Phase 3: テスト可能性（Testability）
**目標**: テストカバレッジ80%以上

```yaml
quality_gates:
  phase3:
    - unit_tests: "各モジュールにテスト存在"
    - coverage: "カバレッジ 80% 以上"
    - integration: "E2Eテストの実装"
    - mocks: "型安全なモックの使用"
```

### Phase 4: 本番品質（Production Ready）
**目標**: 本番環境へのデプロイ可能

```yaml
quality_gates:
  phase4:
    - performance: "レスポンスタイム < 200ms"
    - security: "セキュリティ監査パス"
    - monitoring: "ログとメトリクス実装"
    - documentation: "APIドキュメント完備"
```

## 実装タスクテンプレート

```markdown
### T00X: [タスク名]

#### 実装内容
- [ ] 機能の実装
- [ ] 型定義の作成/更新
- [ ] ユニットテストの作成

#### 品質ゲート（Phase X）
- [ ] TypeScriptビルド成功 `npm run build`
- [ ] 型チェック通過 `npm run type-check`
- [ ] Lintエラーなし `npm run lint`
- [ ] テスト通過 `npm test`

#### 完了条件
- [ ] コードレビュー承認
- [ ] CI/CDパイプライン通過
- [ ] ドキュメント更新
```

## 自動チェックスクリプト

```bash
#!/bin/bash
# .mc/scripts/check-quality-gate.sh

PHASE=${1:-1}

echo "🎯 Phase $PHASE の品質ゲートチェック"

case $PHASE in
  1)
    npm run build || exit 1
    npm run lint -- --max-warnings 100 || exit 1
    ;;
  2)
    npm run type-check || exit 1
    # any使用のチェック
    if grep -r "any" --include="*.ts" --include="*.tsx" src/; then
      echo "❌ 'any' 型の使用が検出されました"
      exit 1
    fi
    ;;
  3)
    npm test -- --coverage || exit 1
    # カバレッジ閾値のチェック
    ;;
  4)
    npm run build:prod || exit 1
    npm run security-check || exit 1
    ;;
esac

echo "✅ Phase $PHASE の品質ゲートをクリアしました！"
```

## 段階的導入戦略

1. **既存プロジェクトへの適用**
   - Phase 1 から開始
   - 技術的負債を段階的に解消
   - 各Phaseクリア後に次へ進む

2. **新規プロジェクトへの適用**
   - Phase 2 から開始（型安全性重視）
   - 最初から strict モードを有効化
   - テストファーストアプローチ

3. **チーム全体での運用**
   - PRマージ条件に品質ゲートを設定
   - 定期的な品質レビュー会の実施
   - 成功パターンの共有とドキュメント化