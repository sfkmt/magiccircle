# /mc:spec-approve

仕様書のフェーズを承認します。

## 実行内容

1. 指定されたフェーズの内容を検証
2. 承認記録をspec.jsonに保存
3. 次のフェーズへの移行を準備
4. GitHub連携のトリガー

## 使用方法

```bash
/mc:spec-approve [phase] [feature-name]
```

## 引数

- `phase`: 承認するフェーズ（requirements/design/tasks）
- `feature-name`: 対象機能の名前（省略時は現在作業中の仕様書）

## プロンプト

AIアシスタントへの指示：

1. 承認対象の確認：
   ```bash
   # spec.jsonを読み込み
   cat .mc/specs/[feature-name]/spec.json
   
   # 対象フェーズの文書を表示
   cat .mc/specs/[feature-name]/[phase].md
   ```

2. 承認前チェックリスト：
   - **requirements承認時**:
     - [ ] すべての要件が明確で測定可能
     - [ ] ステアリング文書と整合性がある
     - [ ] 受け入れ条件が定義されている
   
   - **design承認時**:
     - [ ] すべての要件がカバーされている
     - [ ] 技術的に実現可能
     - [ ] セキュリティ考慮が含まれている
   
   - **tasks承認時**:
     - [ ] すべてのタスクが実行可能な粒度
     - [ ] 依存関係が明確
     - [ ] 見積もりが現実的

3. 承認処理：
   ```bash
   # spec.jsonを更新
   jq '.phases.[phase] = {
     "status": "approved",
     "approvedAt": "[ISO-8601 timestamp]",
     "approvedBy": "user"
   }' .mc/specs/[feature-name]/spec.json > temp.json
   mv temp.json .mc/specs/[feature-name]/spec.json
   ```

4. GitHub連携アクション：
   - **requirements承認後**:
     - 設計フェーズ開始の準備
     - プロジェクトボードの更新
   
   - **design承認後**:
     - タスク生成フェーズの準備
     - 技術レビューIssueの作成
   
   - **tasks承認後**:
     - GitHub Issuesの自動作成準備
     - CI/CDパイプラインの設定
     - デプロイメント計画の準備

5. 承認完了後の案内：
   ```markdown
   ## ✅ [Phase]フェーズが承認されました
   
   ### 承認情報
   - **承認日時**: [timestamp]
   - **承認者**: user
   
   ### 次のステップ
   [フェーズに応じた次のアクション]
   
   ### GitHub統合
   - [ ] Issue作成: `/mc:github-issue-create [feature-name]`
   - [ ] プロジェクトボード更新
   - [ ] マイルストーン設定
   
   ### イテレーション計画
   - [ ] スプリントへの割り当て
   - [ ] ストーリーポイントの設定
   
   ### デプロイ計画
   - [ ] ターゲット環境: [dev/staging/prod]
   - [ ] 予定リリース: [version]
   
   ### 推奨アクション
   1. [次のコマンド]
   2. [確認事項]
   ```

6. 承認履歴の記録：
   ```bash
   # 承認ログを追加
   echo "[timestamp] [phase] approved by user" >> .mc/specs/[feature-name]/approval.log
   
   # CHANGELOG.mdに記録
   echo "### Spec Approval\n- [feature-name]: [phase] phase approved" >> CHANGELOG.md
   
   # イテレーション計画の更新
   jq '.committed_issues += [{"spec": "[feature-name]", "phase": "[phase]"}]' .mc/iterations/current.json > temp.json
   mv temp.json .mc/iterations/current.json
   ```

7. デプロイパイプラインへの統合：
   ```bash
   # tasksフェーズ承認時のみ
   if [[ "[phase]" == "tasks" ]]; then
     # デプロイ候補として記録
     echo '{"spec": "[feature-name]", "status": "ready_for_deploy", "approved_at": "[timestamp]"}' >> .mc/deploys/candidates.jsonl
   fi
   ```

注意事項：
- 承認は取り消し不可（慎重に実施）
- 前のフェーズが承認済みであることを確認
- GitHub Issue駆動の開発フローと連携
- イテレーション計画に反映
- デプロイメントスケジュールを考慮
- CHANGELOG.mdを常に最新に保つ