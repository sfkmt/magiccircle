# Magic Circle Framework - Iteration-Driven Approach

## 概要

Magic Circleフレームワークの進化版です。従来の仕様駆動開発の良さを保ちながら、より**アジャイル**で**継続的**な開発を可能にします。

## コアコンセプト

### Iteration-Driven Development（反復駆動開発）
- 仕様と実装が相互に反復しながら改善される
- 小さな動作可能な単位で開発が進む
- 変更が自動的に記録され、仕様に反映される

## 4つの駆動原理

### 1. **GitHub-Driven**
- すべての仕様がGitHub Issueとして管理
- 自動実装とPR作成
- 45分で本番デプロイ可能

### 2. **Iteration-Driven**
- コードの変更を自動的に仕様として記録
- コンフリクトを含んだまま進行可能
- 履歴の完全な保持と反復の追跡

### 3. **Type-Driven**
- 型カバレッジ95%以上を維持
- 破壊的変更の自動検出
- 段階的な型移行サポート

### 4. **Deployment-Driven**
- 常にデプロイ可能な状態を維持
- Progressive Rolloutによる安全なリリース
- リアルタイムの健全性監視

## 従来のMagic Circleとの違い

### 従来のアプローチ
```
要件定義（1週間）→ 設計（1週間）→ タスク生成（3日）→ 実装（2週間）
= 約1ヶ月で機能リリース
```

### Iteration-Drivenアプローチ
```
マイクロ仕様（10分）→ 型定義（5分）→ 実装（30分）→ 自動デプロイ（5分）
= 50分で型安全な機能が本番へ

これを1日に10回繰り返す → 継続的な価値提供
```

## 主な機能

### 1. Executable Specifications（実行可能な仕様）
仕様自体が実行可能で、即座に動作確認できます。

### 2. Continuous Spec Iteration（継続的な仕様反復）
実装の変更に応じて仕様が自動的に更新されます。

### 3. Progressive Type Migration（段階的型移行）
破壊的変更を避けながら、型定義を段階的に改善できます。

### 4. Always Deployable Architecture（常時デプロイ可能アーキテクチャ）
どの時点でも本番環境にデプロイ可能な状態を維持します。

## 導入方法

既存のMagic Circleプロジェクトに段階的に適用できます：

```bash
# Iteration-Driven機能を有効化
mc enable-iteration --progressive

# 最初のマイクロ仕様を作成
mc create-micro-spec "簡単なヘルスチェックAPI"

# 自動反復を開始
mc start-iteration-daemon
```

## まとめ

Magic CircleのIteration-Drivenアプローチにより、仕様駆動開発の堅実さとアジャイル開発のスピードを両立できます。「型は嘘をつかない」原則のもと、常に安全で、常に動き、常に反復改善し続ける開発が実現されます。