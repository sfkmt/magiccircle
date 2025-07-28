# Schema-First Development Workflow

## 概要
型定義とスキーマを起点とした開発フローを確立し、実装前に型の整合性を保証します。

## ワークフロー

### 1. データモデル定義フェーズ
```bash
# スキーマ定義の作成
/mc:schema-define [feature-name]
```

**生成物:**
- `.mc/schemas/[feature-name]/`
  - `database.sql` - DBスキーマ定義
  - `types.ts` - TypeScript型定義
  - `validation.ts` - バリデーションスキーマ
  - `mock-data.ts` - テスト用モックデータ

### 2. 型検証フェーズ
```bash
# 型の整合性チェック
/mc:type-validate [feature-name]
```

**チェック項目:**
- [ ] DB スキーマとTypeScript型の一致
- [ ] APIインターフェースの整合性
- [ ] 依存関係の型互換性
- [ ] モックデータの型適合性

### 3. 実装前レビュー
```bash
# 実装可能性の確認
/mc:pre-implementation-review [feature-name]
```

**確認事項:**
- 全ての型定義が完成しているか
- 外部依存の互換性が確認されているか
- テストシナリオが型安全か

## 型駆動開発の原則

1. **型は仕様書である**
   - 型定義を先に作成し、実装はそれに従う
   - 型の変更は仕様変更として扱う

2. **コンパイルエラーゼロが前提**
   - 各タスク完了時に `tsc --noEmit` が成功すること
   - 型エラーは技術的負債として即座に解消

3. **Progressive Type Safety**
   - 最初は `strict: false` から始めても良い
   - 段階的に厳密性を上げていく
   - 最終的に `strict: true` を目指す