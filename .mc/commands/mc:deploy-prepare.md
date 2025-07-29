# /mc:deploy-prepare

デプロイメントの準備を行い、環境別のリリースプロセスを管理します。

## 使用方法

```bash
/mc:deploy-prepare [environment] [options]
```

## 引数

- `environment`: デプロイ対象環境（dev/staging/prod）

## オプション

- `--version [tag]`: バージョンタグ（省略時は自動生成）
- `--features [spec-names]`: デプロイする機能（カンマ区切り）
- `--rollback-plan`: ロールバック計画を含める
- `--dry-run`: 実際のデプロイは行わず確認のみ
- `--auto-changelog`: CHANGELOG.mdを自動更新
- `--release-notes`: リリースノートを自動生成

## プロンプト

AIアシスタントへの指示：

### 1. デプロイ準備チェックリスト

```bash
# 完了したPRを収集
gh pr list --state merged --label "spec-driven" --search "merged:>=$(date -d '7 days ago' -I)"

# 関連するIssueの状態確認
gh issue list --state closed --label "spec-driven" --milestone "current-sprint"

# テスト実行状態の確認
gh run list --workflow "CI" --limit 10 --json conclusion,headBranch,createdAt

# 現在のタグを確認
git tag --sort=-v:refname | head -10
```

### 2. デプロイ対象の特定

```markdown
## デプロイ候補

### 含まれる機能
| 仕様 | PR | マージ日 | テスト状態 | リスク |
|------|-----|----------|------------|--------|
| [spec] | #[pr] | [date] | ✅ Pass | Low |

### 含まれる修正
| Issue | タイプ | PR | 重要度 |
|-------|--------|-----|--------|
| #[num] | bug | #[pr] | High |

### 依存関係チェック
- [ ] データベースマイグレーション: [有/無]
- [ ] 環境変数の変更: [有/無]
- [ ] 外部API変更: [有/無]
- [ ] 破壊的変更: [有/無]
```

### 3. バージョン番号の決定

```bash
# 現在のバージョンを取得
current_version=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")

# セマンティックバージョニングに基づく提案
# - 破壊的変更がある場合: メジャーバージョンアップ
# - 新機能がある場合: マイナーバージョンアップ
# - バグ修正のみ: パッチバージョンアップ
```

### 4. 環境別の準備

#### Development環境
```yaml
deploy:
  environment: development
  auto_merge: true
  rollback_enabled: true
  health_check_url: https://dev.example.com/health
  notification_channel: "#dev-deploys"
```

#### Staging環境
```yaml
deploy:
  environment: staging
  approval_required: true
  smoke_test_suite: "staging-smoke-tests"
  performance_baseline: true
  notification_channel: "#staging-deploys"
```

#### Production環境
```yaml
deploy:
  environment: production
  approval_required: true
  canary_deployment: true
  canary_percentage: 10
  monitoring_alerts: enhanced
  rollback_plan: mandatory
  notification_channel: "#prod-deploys"
```

### 5. デプロイメントマニフェストの生成

```yaml
# .mc/deploys/[environment]-[version].yaml
version: [version]
environment: [environment]
timestamp: [ISO-8601]
deployer: [user]

features:
  - spec: [spec-name]
    pr: [pr-number]
    issues: [issue-numbers]
    
changes:
  added:
    - [description]
  changed:
    - [description]
  fixed:
    - [description]
  removed:
    - [description]

dependencies:
  database_migration: [true/false]
  config_changes:
    - [change]
  
pre_deploy_checks:
  - name: "All tests passing"
    status: [pass/fail]
  - name: "Security scan"
    status: [pass/fail]
  - name: "Performance baseline"
    status: [pass/fail]

rollback_plan:
  trigger: [automatic/manual]
  conditions:
    - error_rate > 5%
    - response_time > 2000ms
  steps:
    - [step1]
    - [step2]

monitoring:
  dashboards:
    - [dashboard-url]
  alerts:
    - [alert-name]
  sla_targets:
    - availability: 99.9%
    - response_time: < 200ms
```

### 6. CHANGELOG.mdの自動更新

```bash
# CHANGELOG.mdに追記
cat >> CHANGELOG.md << EOF

## [${version}] - $(date -I)

### Added
$([新機能のリスト])

### Changed
$([変更のリスト])

### Fixed
$([修正のリスト])

### Removed
$([削除のリスト])

### Deployment
- Environment: ${environment}
- Sprint: Sprint-${sprint_number}
- Deploy Time: $(date -Iseconds)
EOF

# 変更をコミット
git add CHANGELOG.md
git commit -m "chore: update CHANGELOG for ${version}"
```

### 7. リリースノートの生成

```markdown
# Release Notes - [version]

## 🎉 Highlights
[主要な新機能や改善点のサマリー]

## ✨ New Features
[ユーザー向けの新機能説明]

## 🐛 Bug Fixes
[修正されたバグのリスト]

## 🔧 Improvements
[パフォーマンス改善やUX向上]

## 📝 Documentation
[ドキュメントの更新]

## 🔄 Migration Guide
[必要な場合のみ：移行手順]

## 📊 Metrics
- Features delivered: [count]
- Bugs fixed: [count]
- Performance improvement: [percentage]%

## 🙏 Contributors
[コントリビューターのリスト]

---
Generated with Claude Code Spec-Driven Development
```

### 8. デプロイスクリプトの生成

```bash
#!/bin/bash
# deploy-[environment]-[version].sh

echo "🚀 Deploying version ${version} to ${environment}"

# Pre-deployment checks
echo "Running pre-deployment checks..."
[checks]

# Create deployment tag
git tag -a "${version}" -m "Deploy to ${environment}: ${version}"
git push origin "${version}"

# Trigger deployment
case "${environment}" in
  "dev")
    [dev deployment commands]
    ;;
  "staging")
    [staging deployment commands]
    ;;
  "prod")
    [production deployment commands]
    ;;
esac

# Post-deployment verification
echo "Running post-deployment verification..."
[verification commands]

# Update deployment record
echo '{
  "version": "'${version}'",
  "environment": "'${environment}'",
  "timestamp": "'$(date -Iseconds)'",
  "status": "success"
}' >> .mc/deploys/history.jsonl
```

### 9. GitHub Releaseの作成

```bash
# リリースノートをGitHub Releaseとして作成
gh release create "${version}" \
  --title "Release ${version}" \
  --notes-file ".mc/releases/${version}-notes.md" \
  --target "${target_branch}" \
  --prerelease=$([[ $environment == "prod" ]] && echo "false" || echo "true")
```

### 10. 通知とドキュメント

```bash
# Slack通知（環境変数が設定されている場合）
if [[ -n "$SLACK_WEBHOOK_URL" ]]; then
  curl -X POST $SLACK_WEBHOOK_URL \
    -H 'Content-type: application/json' \
    -d '{
      "text": "🚀 Deployment Prepared",
      "blocks": [{
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Version:* '${version}'\n*Environment:* '${environment}'\n*Features:* '${features}'"
        }
      }]
    }'
fi

# デプロイメントWikiの更新
echo "- [${version}] - $(date -I) - ${environment} - [Release Notes](releases/${version}-notes.md)" >> .mc/wiki/deployments.md
```

### エラーハンドリング

- テスト失敗時はデプロイを中止
- 依存関係の問題を検出して警告
- ロールバック計画の妥当性を検証

### 統合機能

- **GitHub Actions**: デプロイワークフローのトリガー
- **監視ツール**: デプロイ後の自動監視設定
- **通知**: 関係者への自動通知
- **ドキュメント**: 自動的に更新される履歴

注意事項：
- 環境ごとに異なる承認プロセスを遵守
- ロールバック計画は必須（特に本番環境）
- すべてのデプロイは追跡可能にする
- CHANGELOGとリリースノートは自動生成だが人間のレビューが必要