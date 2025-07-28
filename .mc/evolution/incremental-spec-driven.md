# Incremental Spec-Driven Development
## 「動く仕様」から始める開発

### コアコンセプト: Executable Specifications

仕様自体が実行可能で、即座に動作確認できる形式で記述します。

### 1. Executable Spec Format

```yaml
# .mc/specs/user-api/executable/001-create-user.yml
executable_spec:
  id: "001"
  title: "最小限のユーザー作成API"
  
  # 10分以内に実装可能な最小スコープ
  minimal_implementation:
    endpoint: "POST /api/users"
    request:
      content_type: "application/json"
      body: |
        {
          "email": "test@example.com"
        }
    response:
      status: 201
      body: |
        {
          "id": "any-string",
          "email": "test@example.com"
        }
  
  # この仕様を満たす最小実装例
  reference_implementation: |
    app.post('/api/users', (req, res) => {
      res.status(201).json({
        id: Date.now().toString(),
        email: req.body.email
      });
    });
  
  # 動作確認用のテストコマンド
  verification:
    setup: "npm run dev"
    test: |
      curl -X POST http://localhost:3000/api/users \
        -H "Content-Type: application/json" \
        -d '{"email":"test@example.com"}'
    teardown: "pkill -f 'npm run dev'"
  
  # 次のインクリメント
  next_increments:
    - id: "002"
      title: "メールバリデーション追加"
      estimated_time: "10 minutes"
    - id: "003" 
      title: "重複チェック追加"
      estimated_time: "15 minutes"
```

### 2. Incremental Spec Runner

```typescript
// .mc/lib/incremental-spec-runner.ts

class IncrementalSpecRunner {
  async runSpec(specPath: string) {
    const spec = await this.loadSpec(specPath);
    
    console.log(`🚀 Running: ${spec.title}`);
    console.log(`⏱️  Target time: ${spec.minimal_implementation.estimated_time || '10 minutes'}`);
    
    // 1. 参考実装を表示
    console.log('\n📝 Reference implementation:');
    console.log(spec.reference_implementation);
    
    // 2. 実装タイマー開始
    const startTime = Date.now();
    
    // 3. ファイル変更を監視
    const watcher = this.watchImplementation(spec);
    
    // 4. 変更があるたびに自動テスト
    watcher.on('change', async () => {
      const result = await this.verifyImplementation(spec);
      
      if (result.success) {
        const elapsed = Date.now() - startTime;
        console.log(`✅ Spec satisfied in ${elapsed / 1000}s!`);
        
        // 次のインクリメントを提案
        this.suggestNextIncrement(spec);
      } else {
        console.log(`❌ Not yet: ${result.error}`);
        console.log(`💡 Hint: ${result.hint}`);
      }
    });
  }
  
  async verifyImplementation(spec: ExecutableSpec) {
    try {
      // サーバーを起動
      await this.runCommand(spec.verification.setup);
      
      // テストを実行
      const output = await this.runCommand(spec.verification.test);
      
      // レスポンスを検証
      return this.validateResponse(output, spec.minimal_implementation.response);
    } finally {
      // クリーンアップ
      await this.runCommand(spec.verification.teardown);
    }
  }
}
```

### 3. Progressive Spec Layers

```yaml
# .mc/specs/user-api/layers/layer-stack.yml

layers:
  # Layer 1: 最小動作（5分で実装）
  - id: "L1-minimal"
    specs: ["001-create-user", "002-get-user"]
    goal: "APIが起動し、基本的なCRUDが動く"
    verification: "curl tests pass"
    
  # Layer 2: バリデーション（+10分）
  - id: "L2-validation"
    specs: ["003-email-validation", "004-required-fields"]
    goal: "不正なデータを弾く"
    verification: "validation tests pass"
    
  # Layer 3: 永続化（+15分）
  - id: "L3-persistence"
    specs: ["005-save-to-db", "006-unique-constraint"]
    goal: "データが永続化される"
    verification: "db integration tests pass"
    
  # Layer 4: 認証（+20分）
  - id: "L4-authentication"
    specs: ["007-jwt-auth", "008-protected-routes"]
    goal: "認証が必要なエンドポイントが保護される"
    verification: "auth tests pass"

# 各レイヤーは前のレイヤーが動作している前提で追加
```

### 4. Live Spec Dashboard

```html
<!-- .mc/dashboard/index.html -->
<!DOCTYPE html>
<html>
<head>
  <title>Live Spec Progress</title>
  <script src="https://cdn.jsdelivr.net/npm/vue@3"></script>
</head>
<body>
  <div id="app">
    <h1>🎯 Current Spec Progress</h1>
    
    <!-- 現在のレイヤー -->
    <div class="current-layer">
      <h2>Layer {{ currentLayer.id }}: {{ currentLayer.goal }}</h2>
      <div class="progress-bar">
        <div class="progress" :style="{width: progress + '%'}"></div>
      </div>
    </div>
    
    <!-- 実行中の仕様 -->
    <div class="running-specs">
      <div v-for="spec in runningSpecs" :key="spec.id" class="spec-card">
        <h3>{{ spec.title }}</h3>
        <div class="status" :class="spec.status">
          {{ spec.status }}
        </div>
        <pre v-if="spec.lastTest">{{ spec.lastTest }}</pre>
      </div>
    </div>
    
    <!-- ライブログ -->
    <div class="live-log">
      <h3>Live Output</h3>
      <pre>{{ liveLog }}</pre>
    </div>
  </div>
  
  <script>
    // WebSocketで進捗をリアルタイム更新
    const ws = new WebSocket('ws://localhost:8080/spec-progress');
    
    const app = Vue.createApp({
      data() {
        return {
          currentLayer: {},
          runningSpecs: [],
          progress: 0,
          liveLog: ''
        };
      },
      mounted() {
        ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          this.updateProgress(data);
        };
      },
      methods: {
        updateProgress(data) {
          this.currentLayer = data.currentLayer;
          this.runningSpecs = data.runningSpecs;
          this.progress = data.progress;
          this.liveLog += data.log + '\n';
        }
      }
    });
    
    app.mount('#app');
  </script>
</body>
</html>
```

### 5. Micro-Feedback Loop

```bash
#!/bin/bash
# .mc/scripts/micro-feedback.sh

# 5分ごとに自動的にフィードバックを収集

while true; do
  # 現在の実装状態をチェック
  CURRENT_STATE=$(mc check-implementation)
  
  # 仕様との差分を検出
  SPEC_DIFF=$(mc spec-diff --current)
  
  if [ -n "$SPEC_DIFF" ]; then
    # 小さな改善提案を生成
    mc suggest-micro-improvement > improvement.md
    
    # GitHub Issueとして作成（5分で実装可能なもののみ）
    gh issue create \
      --title "Micro: $(head -1 improvement.md)" \
      --body "$(cat improvement.md)" \
      --label "micro-improvement,5-minutes"
  fi
  
  sleep 300 # 5分待機
done
```

### 6. Instant Deployment Pipeline

```yaml
# .github/workflows/instant-deploy.yml
name: Instant Deploy on Spec Pass

on:
  push:
    branches: [main, develop]

jobs:
  verify-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Run Executable Specs
        run: |
          # 実行可能な仕様をすべて実行
          mc run-executable-specs --parallel
          
      - name: Deploy to Preview
        if: success()
        run: |
          # 成功したらすぐにプレビュー環境へ
          mc deploy --env preview --instant
          
          # プレビューURLを出力
          echo "🚀 Deployed to: $PREVIEW_URL"
          
      - name: Run Smoke Tests
        run: |
          # プレビュー環境で最小限の動作確認
          mc smoke-test --url $PREVIEW_URL
          
      - name: Auto-Promote
        if: success()
        run: |
          # スモークテストが通ったら本番へ自動昇格
          mc promote --from preview --to production --auto
```

## 実践シナリオ: 30分でAPIを本番へ

```bash
# 1. 最初の実行可能仕様を作成（2分）
mc create-executable-spec "GET /health returns ok"

# 2. 最小実装（3分）
echo 'app.get("/health", (req, res) => res.json({status: "ok"}))' >> src/app.js

# 3. 自動検証が成功 → 自動デプロイ（2分）
# ✅ Spec satisfied!
# 🚀 Deploying to preview...
# ✅ Deployed to https://preview-abc123.example.com

# 4. 次の仕様を追加（2分）
mc add-increment "Add timestamp to health check"

# 5. 実装を更新（3分）
# エディタで実装を修正

# 6. 再度自動検証・デプロイ（2分）
# ✅ All specs passing!
# 🚀 Promoting to production...

# 7. 本番で動作確認（1分）
curl https://api.example.com/health
# {"status":"ok","timestamp":"2024-01-15T10:30:00Z"}

# トータル: 15分で本番稼働 🎉
```

## まとめ

この「小さな動作確認を組み込んだ仕様駆動開発」により：

1. **即座のフィードバック**: 書いたコードがすぐに動く
2. **段階的な複雑性**: 簡単なものから徐々に機能追加
3. **常に動く状態**: 各段階で動作するものがある
4. **低リスク**: 小さな変更なので問題があってもすぐ戻せる
5. **高速な価値提供**: 15-30分で新機能が本番へ