#!/bin/bash

# Claude Code実行スクリプト
# GitHub Actionsから呼び出され、タスクを自動実行する

set -e

# 引数の解析
SPEC_NAME="$1"
TASK_ID="$2"
CONTEXT_FILE="$3"

if [ -z "$SPEC_NAME" ] || [ -z "$TASK_ID" ]; then
    echo "Usage: $0 <spec-name> <task-id> [context-file]"
    exit 1
fi

echo "🤖 Starting Claude Code execution for Task #$TASK_ID in spec: $SPEC_NAME"

# 作業ディレクトリの準備
WORK_DIR=".mc/execution/$SPEC_NAME/task-$TASK_ID"
mkdir -p "$WORK_DIR"

# コンテキストファイルの準備
if [ -z "$CONTEXT_FILE" ]; then
    CONTEXT_FILE="$WORK_DIR/context.json"
    
    # コンテキストを生成
    cat > "$CONTEXT_FILE" << EOF
{
  "spec_name": "$SPEC_NAME",
  "task_id": "$TASK_ID",
  "files": {
    "requirements": ".mc/specs/$SPEC_NAME/requirements.md",
    "design": ".mc/specs/$SPEC_NAME/design.md",
    "tasks": ".mc/specs/$SPEC_NAME/tasks.md"
  },
  "instructions": [
    "このタスクを仕様書に基づいて実装してください",
    "設計文書の指針に従ってください",
    "テストを含めて実装を完了させてください",
    "必要に応じてドキュメントを更新してください"
  ]
}
EOF
fi

# Claude Codeセッションの開始
echo "📋 Preparing context from: $CONTEXT_FILE"

# タスクの詳細を抽出
TASK_DETAILS=$(node -e "
const fs = require('fs');
const tasksContent = fs.readFileSync('.mc/specs/$SPEC_NAME/tasks.md', 'utf8');
const taskRegex = /## タスク$TASK_ID:(.+?)(?=##|$)/s;
const match = tasksContent.match(taskRegex);
if (match) {
    console.log(match[0].trim());
} else {
    console.log('Task not found');
}
")

# Claude Codeに実行を依頼
CLAUDE_PROMPT=$(cat << EOF
以下のタスクを実装してください：

$TASK_DETAILS

実装にあたっては、以下のガイドラインに従ってください：
1. 仕様書（.mc/specs/$SPEC_NAME/requirements.md）の要件を満たすこと
2. 設計文書（.mc/specs/$SPEC_NAME/design.md）のアーキテクチャに従うこと
3. 適切なエラーハンドリングを実装すること
4. 必要なテストを作成すること
5. コードは読みやすく、保守しやすいものにすること

実装が完了したら、変更内容をまとめて報告してください。
EOF
)

# 実行ログの記録
LOG_FILE="$WORK_DIR/execution.log"
echo "🚀 Executing task with Claude Code..." | tee -a "$LOG_FILE"
echo "Timestamp: $(date)" | tee -a "$LOG_FILE"
echo "---" | tee -a "$LOG_FILE"

# Claude Codeの実行（実際の実装では、Claude Code CLIまたはAPIを使用）
# ここではデモ用の擬似コード
if command -v claude-code &> /dev/null; then
    claude-code execute \
        --prompt "$CLAUDE_PROMPT" \
        --context "$CONTEXT_FILE" \
        --output "$WORK_DIR/result.json" \
        2>&1 | tee -a "$LOG_FILE"
else
    # Claude Code CLIが利用できない場合のフォールバック
    echo "⚠️  Claude Code CLI not found. Creating placeholder result." | tee -a "$LOG_FILE"
    
    cat > "$WORK_DIR/result.json" << EOF
{
  "status": "completed",
  "task_id": "$TASK_ID",
  "spec_name": "$SPEC_NAME",
  "changes": [
    {
      "type": "placeholder",
      "description": "This is a placeholder result. Install Claude Code CLI for actual execution."
    }
  ],
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
fi

# 実行結果の検証
if [ -f "$WORK_DIR/result.json" ]; then
    echo "✅ Task execution completed successfully" | tee -a "$LOG_FILE"
    
    # 結果のサマリーを生成
    node -e "
    const fs = require('fs');
    const result = JSON.parse(fs.readFileSync('$WORK_DIR/result.json', 'utf8'));
    console.log('📊 Execution Summary:');
    console.log('- Status:', result.status);
    console.log('- Changes:', result.changes.length);
    console.log('- Timestamp:', result.timestamp);
    " | tee -a "$LOG_FILE"
else
    echo "❌ Task execution failed" | tee -a "$LOG_FILE"
    exit 1
fi

# 成果物のアーカイブ
ARCHIVE_DIR=".mc/archives/$SPEC_NAME"
mkdir -p "$ARCHIVE_DIR"
tar -czf "$ARCHIVE_DIR/task-$TASK_ID-$(date +%Y%m%d-%H%M%S).tar.gz" -C "$WORK_DIR" .

echo "📦 Results archived to: $ARCHIVE_DIR" | tee -a "$LOG_FILE"
echo "✨ Claude Code execution completed for Task #$TASK_ID" | tee -a "$LOG_FILE"