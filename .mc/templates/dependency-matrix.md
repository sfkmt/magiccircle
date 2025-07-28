# Dependency Management Matrix Template

## 依存関係分析チェックリスト

### 1. 互換性マトリックス
| パッケージ | バージョン | 依存先 | 互換性 | 注意事項 |
|-----------|-----------|--------|---------|----------|
| Example: | | | | |
| @fastify/rate-limit | ^9.0.0 | ioredis | ✅ | redis v4は非互換 |
| redis | ^4.0.0 | - | ⚠️ | カスタムアダプター必要 |

### 2. 型定義の可用性
| パッケージ | 型定義 | 品質 | 備考 |
|-----------|--------|------|------|
| fastify | @types/fastify | ⭐⭐⭐⭐⭐ | 公式型定義 |
| custom-lib | 内包 | ⭐⭐⭐ | 要確認 |

### 3. バージョン固定戦略
```json
{
  "overrides": {
    "redis": "4.6.5",
    "ioredis": "5.3.2"
  }
}
```

### 4. 依存関係の検証スクリプト
```bash
#!/bin/bash
# .mc/scripts/validate-dependencies.sh

echo "🔍 依存関係の検証中..."

# 1. 重複パッケージのチェック
npm ls --depth=0 | grep -E "deduped|UNMET"

# 2. 型定義の存在確認
for pkg in $(jq -r '.dependencies | keys[]' package.json); do
  if ! npm ls "@types/$pkg" >/dev/null 2>&1; then
    echo "⚠️  $pkg の型定義が見つかりません"
  fi
done

# 3. peer dependenciesの充足確認
npm ls >/dev/null 2>&1 || echo "❌ 未解決の依存関係があります"
```

## 使用方法

1. 新しい依存関係を追加する前に、このマトリックスを更新
2. 既知の非互換性を事前に文書化
3. 回避策やアダプターの必要性を明記
4. チーム全体で共有し、同じ問題の再発を防ぐ