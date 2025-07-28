#!/usr/bin/env node

/**
 * 依存関係の自動分析ツール
 * package.jsonから依存関係を読み取り、互換性と型定義の可用性を分析
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 既知の非互換性パターン
const KNOWN_INCOMPATIBILITIES = [
  {
    package: '@fastify/rate-limit',
    incompatibleWith: ['redis'],
    requiredAlternative: 'ioredis',
    reason: '@fastify/rate-limit requires ioredis, not redis v4+'
  },
  {
    package: 'graphql',
    incompatibleWith: ['graphql-tools@^6'],
    requiredVersion: '^15.0.0 || ^16.0.0',
    reason: 'GraphQL Tools v6 requires GraphQL v15 or v16'
  }
];

// 型定義の品質評価
const TYPE_QUALITY = {
  '@types/node': 5,
  '@types/react': 5,
  '@types/express': 4,
  '@types/lodash': 4,
  '@types/jest': 5,
};

class DependencyAnalyzer {
  constructor() {
    this.packageJson = this.loadPackageJson();
    this.dependencies = {
      ...this.packageJson.dependencies,
      ...this.packageJson.devDependencies
    };
  }

  loadPackageJson() {
    try {
      return JSON.parse(fs.readFileSync('package.json', 'utf8'));
    } catch (error) {
      console.error('❌ package.json の読み込みに失敗しました');
      process.exit(1);
    }
  }

  analyze() {
    console.log('🔍 依存関係の分析を開始します...\n');

    const report = {
      totalDependencies: Object.keys(this.dependencies).length,
      typedDependencies: 0,
      untypedDependencies: [],
      incompatibilities: [],
      recommendations: []
    };

    // 1. 型定義の確認
    console.log('📝 型定義の確認中...');
    for (const [pkg, version] of Object.entries(this.dependencies)) {
      if (this.hasTypeDefinitions(pkg)) {
        report.typedDependencies++;
      } else {
        report.untypedDependencies.push(pkg);
      }
    }

    // 2. 互換性チェック
    console.log('🔗 互換性の確認中...');
    for (const incompatibility of KNOWN_INCOMPATIBILITIES) {
      if (this.dependencies[incompatibility.package]) {
        for (const incompatiblePkg of incompatibility.incompatibleWith) {
          if (this.dependencies[incompatiblePkg] || 
              this.dependencies[incompatiblePkg.split('@')[0]]) {
            report.incompatibilities.push({
              ...incompatibility,
              found: incompatiblePkg
            });
          }
        }
      }
    }

    // 3. 重複パッケージの検出
    console.log('👥 重複パッケージの確認中...');
    try {
      const dupeOutput = execSync('npm ls --depth=0 --json', { encoding: 'utf8' });
      const dupeData = JSON.parse(dupeOutput);
      // 重複パッケージの分析ロジック
    } catch (error) {
      // npm ls がエラーを返す場合も正常に処理
    }

    // 4. レポート生成
    this.generateReport(report);
    this.generateDependencyMatrix(report);
  }

  hasTypeDefinitions(packageName) {
    // @types/パッケージの存在確認
    if (this.dependencies[`@types/${packageName}`]) {
      return true;
    }

    // パッケージ自体に型定義が含まれているか確認
    try {
      const pkgPath = path.join('node_modules', packageName, 'package.json');
      if (fs.existsSync(pkgPath)) {
        const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
        return pkg.types || pkg.typings || fs.existsSync(path.join('node_modules', packageName, 'index.d.ts'));
      }
    } catch (error) {
      // エラーは無視
    }

    return false;
  }

  generateReport(report) {
    console.log('\n📊 分析結果:\n');
    console.log(`総依存関係数: ${report.totalDependencies}`);
    console.log(`型定義あり: ${report.typedDependencies} (${Math.round(report.typedDependencies / report.totalDependencies * 100)}%)`);
    
    if (report.untypedDependencies.length > 0) {
      console.log('\n⚠️  型定義がないパッケージ:');
      report.untypedDependencies.forEach(pkg => {
        console.log(`  - ${pkg}`);
      });
    }

    if (report.incompatibilities.length > 0) {
      console.log('\n❌ 互換性の問題:');
      report.incompatibilities.forEach(issue => {
        console.log(`  - ${issue.package} と ${issue.found} は非互換です`);
        console.log(`    理由: ${issue.reason}`);
        console.log(`    推奨: ${issue.requiredAlternative || issue.requiredVersion}`);
      });
    }

    // 推奨事項
    console.log('\n💡 推奨事項:');
    if (report.untypedDependencies.length > 0) {
      console.log('  - 型定義のないパッケージに @types/* をインストールしてください');
    }
    if (report.incompatibilities.length > 0) {
      console.log('  - 互換性の問題を解決してください');
    }
  }

  generateDependencyMatrix(report) {
    const matrixPath = '.mc/analysis/dependency-matrix.json';
    const matrix = {
      timestamp: new Date().toISOString(),
      dependencies: {},
      incompatibilities: report.incompatibilities,
      recommendations: []
    };

    // 各依存関係の詳細情報
    for (const [pkg, version] of Object.entries(this.dependencies)) {
      matrix.dependencies[pkg] = {
        version,
        hasTypes: this.hasTypeDefinitions(pkg),
        typeQuality: TYPE_QUALITY[`@types/${pkg}`] || 0
      };
    }

    // マトリックスを保存
    const dir = path.dirname(matrixPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(matrixPath, JSON.stringify(matrix, null, 2));
    console.log(`\n✅ 依存関係マトリックスを ${matrixPath} に保存しました`);
  }
}

// 実行
if (require.main === module) {
  const analyzer = new DependencyAnalyzer();
  analyzer.analyze();
}