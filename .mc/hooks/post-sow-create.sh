#!/bin/bash
# Magic Circle Post-SOW-Create Hook
# SOW作成後に自動実行されるフック

SOW_TYPE="${MC_SOW_TYPE:-}"
SOW_TARGET="${MC_SOW_TARGET:-}"
SOW_FILE="${MC_SOW_FILE:-}"

echo "📄 SOW creation completed for $SOW_TYPE: $SOW_TARGET"

# プロジェクト状態を自動同期
echo "📊 Updating project documentation after SOW creation..."
if [ -f ".mc/scripts/update_project_state.py" ]; then
    python3 .mc/scripts/update_project_state.py
    echo "✅ Project state synchronized after SOW creation"
    
    # SOW作成の通知
    if [ -n "$SOW_FILE" ]; then
        echo "💡 SOW saved to: $SOW_FILE"
        echo "   Use '/mc:task-execute' to execute the SOW"
    fi
fi