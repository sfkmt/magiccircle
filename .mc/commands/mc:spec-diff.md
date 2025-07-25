# 仕様書差分表示コマンド

仕様書の変更履歴と実装との差分を視覚的に表示します。

## 使用方法
```
/mc:spec-diff [spec-name] [--phase <phase>] [--compare-with <ref>] [--format <format>]
```

## オプション
- `--phase`: 特定フェーズのみ比較（requirements|design|tasks|all）デフォルト: all
- `--compare-with`: 比較対象（implementation|previous-version|branch:<name>）
- `--format`: 出力形式（unified|side-by-side|github|summary）デフォルト: unified

## 主要機能

### 1. 仕様と実装の差分検出
```bash
/mc:spec-diff user-auth --compare-with implementation
```
- 承認された仕様と実際のコードの差異を検出
- 未実装の要件をハイライト
- 仕様にない実装を警告

### 2. バージョン間の差分表示
```bash
/mc:spec-diff user-auth --compare-with previous-version
```
- 仕様書の変更履歴を表示
- 各フェーズの変更点を時系列で追跡
- 承認者と承認日時を表示

### 3. ブランチ間の仕様比較
```bash
/mc:spec-diff user-auth --compare-with branch:feature/oauth
```
- 異なるブランチの仕様を比較
- マージ時の仕様衝突を事前検出

## 出力例

### unified形式
```diff
=== Requirements Phase ===
@@ -10,6 +10,8 @@ ## 機能要件
 - ユーザーはメールアドレスとパスワードでログイン可能
 - セッションは24時間有効
 - パスワードは最低8文字必要
+- 2要素認証をサポート
+- ソーシャルログイン（Google, GitHub）対応

=== Implementation Status ===
✓ メールアドレスとパスワードでログイン: 実装済み (auth.controller.ts:45)
✓ セッション管理: 実装済み (session.service.ts:23)
✓ パスワード検証: 実装済み (validation.ts:67)
⚠ 2要素認証: 未実装
⚠ ソーシャルログイン: 部分実装 (Google のみ)
```

### summary形式
```
Specification Compliance Report: user-auth
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase          | Defined | Implemented | Coverage
---------------|---------|-------------|----------
Requirements   |      12 |           9 |      75%
Design         |       8 |           8 |     100%
Tasks          |      15 |          12 |      80%

Missing Implementations:
- 2要素認証の実装
- GitHubソーシャルログイン
- パスワードリセット機能

Undocumented Features:
- カスタムエラーハンドリング (auth.middleware.ts)
- レート制限機能 (rate-limiter.ts)
```

## 高度な使用法

### CI/CD統合
```bash
# 実装が仕様に準拠しているかチェック
/mc:spec-diff user-auth --compare-with implementation --format github > compliance.md
gh pr comment $PR_NUMBER -F compliance.md
```

### 仕様レビュー自動化
```bash
# 仕様変更の影響分析
/mc:spec-diff user-auth --phase requirements --compare-with branch:main | \
  /mc:context-optimize --analyze-impact
```

### 監査証跡の生成
```bash
# 全仕様の準拠状況レポート
for spec in $(ls .mc/specs/); do
  echo "=== $spec ===" >> compliance-report.md
  /mc:spec-diff $spec --format summary >> compliance-report.md
done
```

## 統合ポイント
- `mc:spec-approve`実行時に自動で差分チェック
- PRマージ時にGitHub Actionsで仕様準拠を検証
- `mc:feedback-analyze`と連携して差分から改善点を抽出