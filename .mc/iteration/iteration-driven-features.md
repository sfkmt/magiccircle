# Iteration-Driven Magic Circle Features

## Working Copy as Living Spec（作業コピーが生きた仕様）

### 1. Automatic Spec Snapshots
```bash
# .mc/daemon/spec-watcher.js
const chokidar = require('chokidar');
const { execSync } = require('child_process');

// コード変更を監視し、自動的に仕様を生成
class SpecWatcher {
  constructor() {
    this.watcher = chokidar.watch(['src/**/*.ts', 'src/**/*.js'], {
      persistent: true,
      ignoreInitial: true
    });
  }

  start() {
    this.watcher.on('change', (path) => {
      console.log(`📸 Auto-capturing spec for ${path}`);
      this.captureSpec(path);
    });
  }

  captureSpec(filePath) {
    // TypeScriptのASTから仕様を推測
    const spec = this.analyzeCode(filePath);
    
    // 仕様のスナップショットを作成
    const snapshot = {
      timestamp: new Date().toISOString(),
      file: filePath,
      inferred_behavior: spec.behavior,
      types: spec.types,
      dependencies: spec.dependencies,
      tests_needed: spec.suggestedTests
    };

    // .mc/working/ に保存（作業中の変更を継続的に記録）
    fs.writeFileSync(
      `.mc/working/${Date.now()}.json`,
      JSON.stringify(snapshot, null, 2)
    );
  }
}
```

### 2. Operation Log（操作ログ）
```yaml
# .mc/oplog/operations.yml
# 操作履歴の自動記録

operations:
  - id: op-001
    timestamp: 2024-01-15T10:00:00Z
    type: spec_created
    description: "Created micro-spec for user authentication"
    changes:
      - added: .mc/specs/auth/micro-001.yml
    
  - id: op-002
    timestamp: 2024-01-15T10:30:00Z
    type: implementation_generated
    description: "Auto-generated implementation from spec"
    changes:
      - added: src/auth/login.ts
      - added: tests/auth/login.test.ts
    parent: op-001
    
  - id: op-003
    timestamp: 2024-01-15T11:00:00Z
    type: spec_evolved
    description: "Spec evolved based on implementation feedback"
    changes:
      - modified: .mc/specs/auth/micro-001.yml
    parent: op-002
```

### 3. Spec Conflicts as First-Class Citizens
```typescript
// .mc/lib/spec-conflict-resolver.ts

interface SpecConflict {
  id: string;
  specs: MicroSpec[];
  resolution?: ConflictResolution;
}

class SpecConflictResolver {
  // コンフリクトを含んだまま進行可能
  async mergeWithConflicts(specs: MicroSpec[]): Promise<MergedSpec> {
    const conflicts = this.detectConflicts(specs);
    
    return {
      base: specs[0],
      alternatives: specs.slice(1),
      conflicts: conflicts,
      // 実行時に解決
      resolver: `
        if (process.env.FEATURE_VERSION === 'A') {
          return implementationA();
        } else {
          return implementationB();
        }
      `
    };
  }

  // 後から解決
  async resolveConflict(conflictId: string, resolution: ConflictResolution) {
    const conflict = await this.getConflict(conflictId);
    
    // 解決方法を記録
    await this.recordResolution(conflict, resolution);
    
    // 新しい統合仕様を生成
    return this.generateMergedSpec(conflict, resolution);
  }
}
```

### 4. Change-Based Spec Evolution
```bash
#!/bin/bash
# .mc/scripts/evolve-spec.sh

# 変更追跡ID
CHANGE_ID=$(date +%s | sha256sum | cut -c1-12)

# 現在の実装状態をキャプチャ
capture_current_state() {
  echo "🔄 Capturing current state as change-$CHANGE_ID"
  
  # 実行中のエンドポイントを記録
  curl -s http://localhost:3000/api/_health/endpoints > \
    .mc/changes/$CHANGE_ID/endpoints.json
  
  # 型カバレッジを記録
  npx typescript-coverage-report > \
    .mc/changes/$CHANGE_ID/type-coverage.json
  
  # テスト結果を記録
  npm test -- --json > \
    .mc/changes/$CHANGE_ID/test-results.json
}

# 変更から新しい仕様を生成
generate_spec_from_change() {
  mc generate-spec \
    --from-change $CHANGE_ID \
    --output .mc/specs/evolved/spec-$CHANGE_ID.yml
}
```

### 5. Immutable Spec History
```typescript
// .mc/lib/spec-history.ts

class SpecHistory {
  // すべての仕様変更は不変
  private readonly history: Map<string, SpecVersion> = new Map();
  
  // 新しいバージョンは常に新しいIDで作成
  async createVersion(spec: MicroSpec): Promise<string> {
    const versionId = this.generateVersionId();
    const version: SpecVersion = {
      id: versionId,
      spec: Object.freeze(spec),
      timestamp: new Date(),
      parent: spec.parentId,
      metadata: {
        author: process.env.USER,
        source: 'manual' | 'auto-generated' | 'evolved'
      }
    };
    
    this.history.set(versionId, version);
    return versionId;
  }
  
  // 履歴の書き換えではなく、新しい解釈を追加
  async reinterpret(versionId: string, newInterpretation: any) {
    const original = this.history.get(versionId);
    return this.createVersion({
      ...original.spec,
      reinterpretation: newInterpretation,
      parentId: versionId
    });
  }
}
```

### 6. Parallel Spec Development
```yaml
# .mc/specs/parallel-development.yml

# 複数の仕様を並行して開発
parallel_specs:
  - branch: feature/auth-jwt
    spec: micro-auth-jwt.yml
    status: implementing
    
  - branch: feature/auth-oauth
    spec: micro-auth-oauth.yml
    status: testing
    
  # 両方の実装を保持したまま本番へ
  merge_strategy:
    type: "feature_flag"
    flag: "AUTH_STRATEGY"
    default: "jwt"
```

## Continuous Spec Sync

### Auto-sync Daemon
```javascript
// .mc/daemon/auto-sync.js

class SpecAutoSync {
  constructor() {
    this.interval = 5000; // 5秒ごと
  }
  
  async start() {
    setInterval(async () => {
      // 実装の現状を取得
      const currentState = await this.captureImplementationState();
      
      // 仕様との差分を検出
      const drift = await this.detectSpecDrift(currentState);
      
      if (drift.detected) {
        // 自動的に仕様を更新（新しいバージョンとして）
        const newSpecId = await this.evolveSpec(drift);
        
        // GitHub Issueにコメント
        await this.notifySpecEvolution(newSpecId, drift);
      }
    }, this.interval);
  }
  
  async captureImplementationState() {
    return {
      endpoints: await this.scanEndpoints(),
      types: await this.extractTypes(),
      tests: await this.analyzeTests(),
      performance: await this.measurePerformance()
    };
  }
}
```

## 実践例: Login機能の進化

```bash
# 1. 最初の仕様スナップショット
mc snapshot
# => .mc/snapshots/001-initial.json

# 2. 簡単なログイン実装
echo "app.post('/login', (req, res) => res.json({ok: true}))" >> src/auth.js

# 3. 自動的に仕様が進化
# => .mc/working/002-login-endpoint.json が自動生成

# 4. テストを追加
echo "test('login returns ok', ...)" >> tests/auth.test.js

# 5. 仕様が再度進化
# => .mc/working/003-login-with-test.json

# 6. 型定義を追加
echo "interface LoginRequest { ... }" >> src/types.ts

# 7. 仕様が型情報を含むように進化
# => .mc/working/004-typed-login.json

# 8. すべての進化を統合した仕様を生成
mc consolidate-specs --from .mc/working/
# => .mc/specs/auth/login-consolidated.yml
```

## Magic Circle Iteration = Continuous Spec Iteration

この統合により実現できること：

1. **仕様の自動追従**: コードが変わると仕様も自動的に反復改善
2. **並行開発**: 複数の仕様/実装を同時に試せる
3. **履歴の保持**: すべての変更と反復の過程が記録される
4. **コンフリクトの受容**: 矛盾する仕様も一時的に共存可能
5. **継続的な動作**: 常に何かしらが動いている状態を維持