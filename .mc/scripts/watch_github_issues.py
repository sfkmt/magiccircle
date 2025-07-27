#!/usr/bin/env python3
"""
Magic Circle - GitHub Issues監視スクリプト
Issueの状態変更を監視し、タスク完了時にプロジェクト状態を更新します
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Set

def get_current_issues_state() -> Dict[int, str]:
    """現在のIssueの状態を取得"""
    try:
        result = subprocess.run(
            ['gh', 'issue', 'list', '--state', 'all', '--json', 'number,state,title', '--limit', '100'],
            capture_output=True,
            text=True,
            check=True
        )
        issues = json.loads(result.stdout)
        return {issue['number']: issue['state'] for issue in issues}
    except:
        return {}

def load_previous_state() -> Dict[int, str]:
    """前回の状態を読み込み"""
    state_file = Path('.mc/.issue_state.json')
    if state_file.exists():
        with open(state_file, 'r') as f:
            return json.load(f)
    return {}

def save_current_state(state: Dict[int, str]):
    """現在の状態を保存"""
    state_file = Path('.mc/.issue_state.json')
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, 'w') as f:
        json.dump(state, f)

def trigger_post_task_complete(issue_numbers: list):
    """タスク完了フックをトリガー"""
    hook_path = Path('.mc/hooks/post-task-complete.sh')
    if hook_path.exists():
        for issue_num in issue_numbers:
            print(f"🎯 Issue #{issue_num} was closed. Triggering post-task-complete hook...")
            env = os.environ.copy()
            env['MC_ISSUE_NUMBER'] = str(issue_num)
            subprocess.run([str(hook_path)], env=env)

def watch_issues(interval: int = 60):
    """Issueの状態を監視"""
    print(f"👀 Watching GitHub Issues (checking every {interval} seconds)...")
    print("Press Ctrl+C to stop")
    
    previous_state = load_previous_state()
    
    try:
        while True:
            current_state = get_current_issues_state()
            
            if current_state:
                # 新たにクローズされたIssueを検出
                newly_closed = []
                for issue_num, state in current_state.items():
                    prev_state = previous_state.get(issue_num, 'OPEN')
                    if state == 'CLOSED' and prev_state == 'OPEN':
                        newly_closed.append(issue_num)
                
                if newly_closed:
                    print(f"\n✅ Detected {len(newly_closed)} newly closed issue(s): {newly_closed}")
                    trigger_post_task_complete(newly_closed)
                
                # 状態を保存
                save_current_state(current_state)
                previous_state = current_state
            
            # 進捗表示
            if current_state:
                closed = sum(1 for s in current_state.values() if s == 'CLOSED')
                total = len(current_state)
                if total > 0:
                    progress = (closed / total) * 100
                    print(f"\r📊 Progress: {closed}/{total} tasks completed ({progress:.0f}%)", end='', flush=True)
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n👋 Stopped watching GitHub Issues")
        sys.exit(0)

def main():
    """メイン処理"""
    # GitHub CLIの確認
    try:
        subprocess.run(['gh', 'auth', 'status'], capture_output=True, check=True)
    except:
        print("❌ GitHub CLI is not authenticated. Run: gh auth login")
        sys.exit(1)
    
    # 引数処理
    interval = 60  # デフォルト60秒
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except:
            print("Usage: python watch_github_issues.py [interval_seconds]")
            sys.exit(1)
    
    # 監視開始
    watch_issues(interval)

if __name__ == "__main__":
    main()