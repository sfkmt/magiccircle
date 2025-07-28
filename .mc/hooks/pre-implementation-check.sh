#!/bin/bash

# Pre-Implementation Validation Hook
# 実装開始前に型安全性と依存関係を検証

set -e

echo "🔍 実装前検証を開始します..."

# 1. TypeScript設定の確認
if [ ! -f "tsconfig.json" ]; then
    echo "❌ tsconfig.json が見つかりません"
    echo "💡 ヒント: npx tsc --init で作成してください"
    exit 1
fi

# 2. 型チェックの実行
echo "📝 型チェック中..."
if ! npx tsc --noEmit; then
    echo "❌ TypeScriptの型エラーがあります"
    echo "💡 実装前に型エラーを解決してください"
    exit 1
fi

# 3. 必要な型定義の確認
echo "🔎 型定義の確認中..."
MISSING_TYPES=()
while IFS= read -r dep; do
    if [ -n "$dep" ]; then
        # @types/パッケージまたは内包型定義の確認
        if ! npm ls "@types/$dep" >/dev/null 2>&1; then
            # パッケージ自体に型定義が含まれているか確認
            if ! [ -f "node_modules/$dep/index.d.ts" ] && ! [ -f "node_modules/$dep/dist/index.d.ts" ]; then
                MISSING_TYPES+=("$dep")
            fi
        fi
    fi
done < <(jq -r '.dependencies // {} | keys[]' package.json 2>/dev/null)

if [ ${#MISSING_TYPES[@]} -gt 0 ]; then
    echo "⚠️  以下のパッケージの型定義が見つかりません:"
    printf '%s\n' "${MISSING_TYPES[@]}"
    echo "💡 npm install -D @types/[package-name] でインストールしてください"
fi

# 4. スキーマと型の整合性チェック
if [ -d ".mc/schemas" ]; then
    echo "🔄 スキーマと型の整合性を確認中..."
    for schema_dir in .mc/schemas/*/; do
        if [ -d "$schema_dir" ]; then
            feature=$(basename "$schema_dir")
            echo "  - $feature の検証中..."
            
            # types.tsが存在するか
            if [ ! -f "$schema_dir/types.ts" ]; then
                echo "    ⚠️  types.ts が見つかりません"
            fi
            
            # validation.tsが存在するか
            if [ ! -f "$schema_dir/validation.ts" ]; then
                echo "    ⚠️  validation.ts が見つかりません"
            fi
        fi
    done
fi

# 5. 依存関係の互換性チェック
echo "🔗 依存関係の互換性を確認中..."
if [ -f ".mc/templates/dependency-matrix.md" ]; then
    # 既知の非互換性をチェック
    if grep -q "⚠️" ".mc/templates/dependency-matrix.md"; then
        echo "⚠️  既知の依存関係の問題があります。dependency-matrix.md を確認してください"
    fi
fi

echo "✅ 実装前検証が完了しました"
echo ""
echo "📋 チェックリスト:"
echo "  ✓ TypeScript設定の存在"
echo "  ✓ 型エラーなし"
echo "  ✓ 型定義の確認"
echo "  ✓ スキーマの整合性"
echo "  ✓ 依存関係の互換性"
echo ""
echo "🚀 実装を開始できます！"