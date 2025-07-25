# SOW (Statement of Work) 生成コマンド

承認済みのタスクから詳細な作業指示書（SOW）を自動生成します。

## 使用方法
```
/mc:sow-create [spec-name] [--task-id <id>] [--output-format <format>]
```

## オプション
- `--task-id`: 特定のタスクIDのSOWのみ生成
- `--output-format`: 出力形式（markdown|json|claude-xml）デフォルト: claude-xml

## 動作
1. 指定された仕様のタスクフェーズが承認済みかチェック
2. tasks.mdからタスクを解析
3. requirements.mdとdesign.mdから関連コンテキストを抽出
4. 各タスクに対して以下を含むSOWを生成：
   - 明確な成功基準
   - 実装に必要な技術的詳細
   - 依存関係と前提条件
   - テストケースと検証手順
   - エラーハンドリング要件

## 出力例
```xml
<sow task-id="task-001" spec="user-auth">
  <objective>ユーザー認証エンドポイントの実装</objective>
  <success-criteria>
    <criterion>POST /api/auth/loginエンドポイントが正常に動作</criterion>
    <criterion>JWTトークンが正しく生成・返却される</criterion>
    <criterion>無効な認証情報で401エラーが返される</criterion>
  </success-criteria>
  <technical-requirements>
    <requirement>Express.jsミドルウェアとして実装</requirement>
    <requirement>bcryptでパスワードハッシュ化</requirement>
    <requirement>jsonwebtokenでJWT生成</requirement>
  </technical-requirements>
  <dependencies>
    <dependency>User モデルが実装済み</dependency>
    <dependency>データベース接続が確立済み</dependency>
  </dependencies>
  <test-cases>
    <test>正常なログイン: メールとパスワードでトークン取得</test>
    <test>無効なメール: 401エラー返却</test>
    <test>無効なパスワード: 401エラー返却</test>
  </test-cases>
  <error-handling>
    <error code="401">認証失敗</error>
    <error code="500">サーバーエラー</error>
  </error-handling>
</sow>
```

## 統合ポイント
- `mc:task-execute`コマンドがこのSOWを使用して自動実装
- GitHub ActionsワークフローでSOWベースの実行をサポート
- Claude Code APIで直接SOWを処理可能

## 使用例
```bash
# 全タスクのSOWを生成
/mc:sow-create user-auth

# 特定タスクのSOWのみ生成
/mc:sow-create user-auth --task-id task-001

# JSON形式で出力
/mc:sow-create user-auth --output-format json
```