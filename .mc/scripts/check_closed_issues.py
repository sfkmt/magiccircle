#!/usr/bin/env python3
"""
Magic Circle - 手動でクローズされたIssueをチェック
最近クローズされたIssueを検出してプロジェクト状態を更新
"""

import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path

def check_recently_closed_issues(hours=24):
    """指定時間内にクローズされたIssueをチェック"""
    try:
        # 最近クローズされたIssueを取得
        result = subprocess.run(
            ['gh', 'issue', 'list', '--state', 'closed', '--json', 'number,title,closedAt', '--limit', '50'],
            capture_output=True,
            text=True,
            check=True
        )
        issues = json.loads(result.stdout)
        
        # 指定時間内にクローズされたものをフィルタ
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_closed = []
        
        for issue in issues:
            if issue.get('closedAt'):
                closed_time = datetime.strptime(issue['closedAt'][:19], '%Y-%m-%dT%H:%M:%S')
                if closed_time > cutoff_time:
                    recent_closed.append(issue)
        
        if recent_closed:
            print(f"🔍 Found {len(recent_closed)} issue(s) closed in the last {hours} hours:")
            for issue in recent_closed:
                print(f"  - #{issue['number']}: {issue['title']}")
            
            # プロジェクト状態を更新
            update_script = Path('.mc/scripts/update_project_state.py')
            if update_script.exists():
                print("\n📊 Updating project state...")
                subprocess.run(['python3', str(update_script)])
                print("✅ Project state updated")
        else:
            print(f"ℹ️  No issues were closed in the last {hours} hours")
            
    except subprocess.CalledProcessError:
        print("❌ Failed to check GitHub issues. Make sure you're authenticated with: gh auth login")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    hours = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    check_recently_closed_issues(hours)