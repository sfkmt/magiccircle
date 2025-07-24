#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * GitHubイシューを自動作成するスクリプト
 * タスク文書から自動的にイシューを作成し、適切なラベルを付与
 */
class GitHubIssueCreator {
  constructor(specName) {
    this.specName = specName;
    this.specPath = path.join('.mc', 'specs', specName);
    this.tasksFile = path.join(this.specPath, 'tasks.md');
    this.specFile = path.join(this.specPath, 'spec.json');
  }

  /**
   * タスク文書を解析してタスクリストを抽出
   */
  parseTasks() {
    const content = fs.readFileSync(this.tasksFile, 'utf8');
    const tasks = [];
    let currentTask = null;
    let inTaskSection = false;

    const lines = content.split('\n');
    for (const line of lines) {
      // タスクセクションの開始を検出
      if (line.match(/^##\s+タスク\d+:/)) {
        if (currentTask) {
          tasks.push(currentTask);
        }
        const taskMatch = line.match(/^##\s+タスク(\d+):\s+(.+)/);
        currentTask = {
          id: taskMatch[1],
          title: taskMatch[2],
          description: '',
          dependencies: [],
          labels: ['mc-task', `spec-${this.specName}`]
        };
        inTaskSection = true;
      } else if (currentTask && inTaskSection) {
        // 依存関係の抽出
        if (line.includes('依存:')) {
          const deps = line.replace('依存:', '').trim();
          if (deps && deps !== 'なし') {
            currentTask.dependencies = deps.split(',').map(d => d.trim());
          }
        } else if (line.startsWith('##')) {
          // 次のセクションに到達
          inTaskSection = false;
        } else {
          // タスクの説明を追加
          currentTask.description += line + '\n';
        }
      }
    }

    if (currentTask) {
      tasks.push(currentTask);
    }

    return tasks;
  }

  /**
   * GitHubイシューを作成
   */
  createIssue(task) {
    const issueBody = `
## 概要
${task.description.trim()}

## 仕様書
- Spec: ${this.specName}
- Task: タスク${task.id}

## 依存関係
${task.dependencies.length > 0 ? task.dependencies.map(d => `- ${d}`).join('\n') : 'なし'}

## 実装方法
このイシューは自動的にClaude Code GitHub Actionsによって処理されます。
ラベル \`mc-task\` が付与されると、自動実行が開始されます。

## チェックリスト
- [ ] 要件の理解
- [ ] 実装
- [ ] テスト
- [ ] ドキュメント更新（必要な場合）

---
*このイシューは仕様書駆動開発システムによって自動生成されました*
`;

    const labels = task.labels.join(',');
    
    try {
      const result = execSync(
        `gh issue create --title "${task.title}" --body "${issueBody.replace(/"/g, '\\"')}" --label "${labels}"`,
        { encoding: 'utf8' }
      );
      
      // イシュー番号を抽出
      const issueNumber = result.match(/\/issues\/(\d+)/)[1];
      console.log(`✅ Created issue #${issueNumber} for ${task.title}`);
      
      return { taskId: task.id, issueNumber };
    } catch (error) {
      console.error(`❌ Failed to create issue for ${task.title}:`, error.message);
      return null;
    }
  }

  /**
   * 依存関係に基づいてイシューをリンク
   */
  linkDependencies(taskMappings) {
    for (const task of this.parseTasks()) {
      if (task.dependencies.length > 0) {
        const currentIssue = taskMappings.find(m => m.taskId === task.id);
        if (!currentIssue) continue;

        for (const dep of task.dependencies) {
          const depTaskId = dep.match(/タスク(\d+)/)?.[1];
          if (depTaskId) {
            const depIssue = taskMappings.find(m => m.taskId === depTaskId);
            if (depIssue) {
              // イシューにコメントを追加して依存関係を明示
              execSync(
                `gh issue comment ${currentIssue.issueNumber} --body "⚡ このタスクは #${depIssue.issueNumber} に依存しています"`,
                { encoding: 'utf8' }
              );
            }
          }
        }
      }
    }
  }

  /**
   * メイン処理
   */
  async run() {
    console.log(`🚀 Creating GitHub issues for spec: ${this.specName}`);
    
    // 仕様書の承認状態を確認
    const spec = JSON.parse(fs.readFileSync(this.specFile, 'utf8'));
    if (spec.phases.tasks.status !== 'approved') {
      console.error('❌ Tasks phase is not approved yet');
      process.exit(1);
    }

    const tasks = this.parseTasks();
    console.log(`📋 Found ${tasks.length} tasks`);

    const taskMappings = [];
    
    // 各タスクのイシューを作成
    for (const task of tasks) {
      const mapping = this.createIssue(task);
      if (mapping) {
        taskMappings.push(mapping);
      }
    }

    // 依存関係をリンク
    this.linkDependencies(taskMappings);

    // マッピング情報を保存
    const mappingFile = path.join(this.specPath, 'issue-mappings.json');
    fs.writeFileSync(mappingFile, JSON.stringify(taskMappings, null, 2));
    
    console.log(`✅ Created ${taskMappings.length} issues successfully`);
    console.log(`📁 Issue mappings saved to ${mappingFile}`);
  }
}

// CLIとして実行
if (require.main === module) {
  const specName = process.argv[2];
  if (!specName) {
    console.error('Usage: node create-github-issues.js <spec-name>');
    process.exit(1);
  }

  const creator = new GitHubIssueCreator(specName);
  creator.run().catch(console.error);
}

module.exports = GitHubIssueCreator;