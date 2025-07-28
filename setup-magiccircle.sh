#!/bin/bash
# setup-magiccircle.sh - Magic Circleフレームワークのセットアップスクリプト

set -e

echo "Magic Circle Framework Setup"
echo "============================"

# カラー定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# プロジェクトのルートディレクトリか確認
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}警告: 現在のディレクトリはGitリポジトリのルートではありません${NC}"
    echo "続行しますか？ (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "セットアップを中止しました"
        exit 1
    fi
fi

# 既存の.claudeディレクトリをチェック
if [ -d ".claude" ]; then
    echo -e "${YELLOW}警告: .claudeディレクトリが既に存在します${NC}"
    echo "上書きしますか？ (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "セットアップを中止しました"
        exit 1
    fi
fi

# Magic Circleをダウンロード
echo "Magic Circleをダウンロード中..."
if command -v curl &> /dev/null; then
    curl -L https://github.com/sfkmt/magiccircle/archive/main.tar.gz -o magiccircle.tar.gz
elif command -v wget &> /dev/null; then
    wget https://github.com/sfkmt/magiccircle/archive/main.tar.gz -O magiccircle.tar.gz
else
    echo -e "${RED}エラー: curlまたはwgetが必要です${NC}"
    exit 1
fi

# 展開とコピー
echo "ファイルを展開中..."
tar -xzf magiccircle.tar.gz

# 必要なファイルをコピー
echo "Magic Circleをプロジェクトに追加中..."
cp -r magiccircle-main/.claude ./
cp magiccircle-main/CLAUDE.md ./

# クリーンアップ
rm -rf magiccircle-main magiccircle.tar.gz

# .mcディレクトリの作成
if [ ! -d ".mc" ]; then
    echo ".mcディレクトリを作成中..."
    mkdir -p .mc/specs
    mkdir -p .mc/steering
    mkdir -p .mc/iteration
    mkdir -p .mc/hooks
    mkdir -p .mc/scripts
    mkdir -p .mc/templates
fi

echo -e "${GREEN}✓ Magic Circleのセットアップが完了しました！${NC}"
echo ""
echo "次のステップ:"
echo "1. Claude Codeを開く"
echo "2. /mc:steering-init を実行してプロジェクトを初期化"
echo "3. /mc:spec-init [feature-name] で最初の機能仕様を作成"
echo ""
echo "詳細は https://github.com/sfkmt/magiccircle を参照してください"