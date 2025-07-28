# mc:quality-check

開発したコードやシステムに対して、リリース前の品質チェックを実行します。

## 使用方法

```bash
mc:quality-check [target-path] [options]
```

### 使用例

```bash
# 基本的な品質チェック
mc:quality-check

# セキュリティチェックのみ実行（イシュー自動作成）
mc:quality-check --type security

# イシュー作成を無効化してチェックのみ実行
mc:quality-check --no-issues

# カスタムラベルを付けてイシュー作成
mc:quality-check --issue-labels "bug,security,priority-high"

# 自動修正を実行（イシューも自動作成）
mc:quality-check --fix --severity high

# CI/CDパイプラインでJSON出力（イシュー作成なし）
mc:quality-check --output json --no-issues --severity critical
```

## パラメータ

- `target-path`: チェック対象のディレクトリパス（デフォルト: カレントディレクトリ）

## オプション

- `--type`: チェックタイプを指定（security, performance, seo, accessibility, all）
- `--output`: 結果の出力形式（console, json, markdown）
- `--fix`: 自動修正可能な問題を修正
- `--severity`: 表示する問題の重要度（critical, high, medium, low）
- `--no-issues`: GitHubイシューの自動作成を無効化（デフォルトは自動作成）
- `--issue-labels`: イシュー作成時に付与するラベル（カンマ区切り）

## 実行内容

### セキュリティチェック

1. **Cookie設定の確認**
   - HttpOnly属性の設定確認
   - SameSite属性（Lax/Strict）の設定確認
   - Secure属性の設定確認（HTTPS環境）
   - Domain属性の適切な設定確認

2. **入力検証の確認**
   - サーバーサイドの入力検証実装確認
   - URL入力の制限（javascript:などの危険なプロトコル）
   - HTMLエスケープ処理の実装確認
   - SQLインジェクション対策の確認

3. **レスポンスヘッダーの確認**
   - Strict-Transport-Securityヘッダー
   - X-Frame-OptionsまたはCSP frame-ancestors
   - X-Content-Type-Options: nosniff
   - Content-Security-Policy設定

4. **認証・認可の確認**
   - メールアドレス所有権の確認フロー
   - アカウント列挙攻撃への対策
   - セッション管理の適切性

### パフォーマンスチェック

1. **コード最適化**
   - 不要なimportの検出
   - 重複コードの検出
   - 大きなバンドルサイズの警告

2. **画像最適化**
   - 画像フォーマットの確認
   - 画像サイズの最適化提案
   - lazy loading実装の確認

### SEOチェック

1. **メタタグの確認**
   - title, descriptionの存在確認
   - Open Graph (OGP)タグの設定確認
   - 構造化データの実装確認

2. **URLとリダイレクト**
   - 適切なURL構造
   - 301/302リダイレクトの適切な使用

### アクセシビリティチェック

1. **基本的なチェック**
   - alt属性の確認
   - ARIAラベルの適切な使用
   - キーボードナビゲーション対応
   - カラーコントラスト比

## 実装方法

1. 各チェック項目に対応する検証ロジックを実装
2. AST解析やパターンマッチングを使用してコードを検査
3. 設定ファイル（package.json, tsconfig.json等）も検査対象に含める
4. チェック結果を重要度別に分類して表示
5. 自動修正可能な項目については修正案を提示

## 出力例

```
🔍 品質チェック結果

✅ 成功: 15項目
⚠️  警告: 3項目
❌ エラー: 1項目

【重要度: Critical】
❌ セキュリティ: HttpOnly属性が設定されていないCookieが検出されました
   ファイル: src/auth/session.ts:45
   修正案: res.cookie('sessionId', token, { httpOnly: true, secure: true, sameSite: 'strict' })

【重要度: High】
⚠️ パフォーマンス: 未使用のimportが検出されました
   ファイル: src/components/Dashboard.tsx:3-5
   修正案: --fix オプションで自動削除可能

【重要度: Medium】
⚠️ SEO: meta descriptionが設定されていません
   ファイル: public/index.html
   修正案: <meta name="description" content="ページの説明文をここに記載">
```

## GitHubイシュー自動作成

デフォルトでは、検出された問題は自動的にGitHubイシューとして作成されます。この機能を無効化したい場合は`--no-issues`オプションを使用してください。

### イシュー作成の流れ

1. 品質チェック実行時に問題を検出
2. 重要度別にイシューを分類
3. 以下の情報を含むイシューを作成：
   - タイトル: `[Quality Check] {チェックタイプ}: {問題の概要}`
   - 本文: 
     - 問題の詳細説明
     - 該当ファイルと行番号
     - 修正提案（可能な場合）
     - 重要度レベル
   - ラベル: severity/critical, type/security等

### イシューテンプレート例

```markdown
## 🚨 品質チェックで問題が検出されました

**チェックタイプ**: セキュリティ
**重要度**: Critical
**検出日時**: 2025-07-28

### 問題の詳細
HttpOnly属性が設定されていないCookieが検出されました。これにより、XSS攻撃のリスクが高まります。

### 該当箇所
- ファイル: `src/auth/session.ts`
- 行番号: 45
- コード:
```typescript
res.cookie('sessionId', token)
```

### 修正提案
以下のように修正してください：
```typescript
res.cookie('sessionId', token, { 
  httpOnly: true, 
  secure: true, 
  sameSite: 'strict' 
})
```

### 参考情報
- [OWASP - HttpOnly](https://owasp.org/www-community/HttpOnly)
- [MDN - Set-Cookie](https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie)
```

## 統合ポイント

- CI/CDパイプラインに統合して自動チェック
- pre-commitフックでコミット前にチェック
- GitHub Actionsワークフローから呼び出し
- 仕様書のタスク完了時に自動実行
- PRレビュー時の自動品質チェック

## 設定ファイル

`.mc/quality-check.config.json`で詳細な設定が可能：

```json
{
  "rules": {
    "security": {
      "cookie-httponly": "error",
      "csp-header": "warning",
      "sql-injection": "error"
    },
    "performance": {
      "bundle-size": {
        "maxSize": "500KB",
        "severity": "warning"
      }
    }
  },
  "exclude": ["node_modules", "dist", "build"],
  "autoFix": true
}
```