#!/usr/bin/env python3
"""
フィードバックループアナライザー
実装結果を分析し、将来の開発に活かすためのパターンを抽出する
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class FeedbackAnalyzer:
    def __init__(self, spec_name: str):
        self.spec_name = spec_name
        self.base_path = Path('.mc')
        self.results_path = self.base_path / 'results' / spec_name
        self.patterns_path = self.base_path / 'patterns'
        self.feedback_path = self.base_path / 'feedback'
        
        # 必要なディレクトリを作成
        self.patterns_path.mkdir(parents=True, exist_ok=True)
        self.feedback_path.mkdir(parents=True, exist_ok=True)
    
    def analyze_implementation(self, pr_number: int) -> Dict[str, Any]:
        """PR から実装を分析してパターンを抽出"""
        analysis = {
            'pr_number': pr_number,
            'spec_name': self.spec_name,
            'timestamp': datetime.utcnow().isoformat(),
            'patterns': [],
            'insights': [],
            'recommendations': []
        }
        
        # タスク実行結果を収集
        task_results = self._collect_task_results()
        
        # コードパターンを分析
        code_patterns = self._analyze_code_patterns(task_results)
        analysis['patterns'].extend(code_patterns)
        
        # エラーパターンを分析
        error_patterns = self._analyze_error_patterns(task_results)
        analysis['patterns'].extend(error_patterns)
        
        # 成功パターンを分析
        success_patterns = self._analyze_success_patterns(task_results)
        analysis['patterns'].extend(success_patterns)
        
        # インサイトを生成
        analysis['insights'] = self._generate_insights(analysis['patterns'])
        
        # 推奨事項を生成
        analysis['recommendations'] = self._generate_recommendations(analysis['patterns'])
        
        # 分析結果を保存
        self._save_analysis(analysis)
        
        return analysis
    
    def _collect_task_results(self) -> List[Dict[str, Any]]:
        """タスク実行結果を収集"""
        results = []
        
        if self.results_path.exists():
            for result_file in self.results_path.glob('task-*/result.json'):
                with open(result_file, 'r') as f:
                    result = json.load(f)
                    result['file_path'] = str(result_file)
                    results.append(result)
        
        return results
    
    def _analyze_code_patterns(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """コードパターンを分析"""
        patterns = []
        
        # ファイル構造パターン
        file_patterns = {}
        for result in results:
            if 'changes' in result:
                for change in result['changes']:
                    if change.get('type') == 'file_created':
                        file_type = Path(change['path']).suffix
                        file_patterns[file_type] = file_patterns.get(file_type, 0) + 1
        
        if file_patterns:
            patterns.append({
                'type': 'file_structure',
                'description': 'よく使用されるファイルタイプ',
                'data': file_patterns,
                'confidence': 0.8
            })
        
        # インポートパターン
        import_patterns = self._analyze_imports(results)
        if import_patterns:
            patterns.append({
                'type': 'imports',
                'description': 'よく使用されるライブラリとモジュール',
                'data': import_patterns,
                'confidence': 0.9
            })
        
        return patterns
    
    def _analyze_imports(self, results: List[Dict[str, Any]]) -> Dict[str, int]:
        """インポートパターンを分析"""
        imports = {}
        
        for result in results:
            if 'code_snippets' in result:
                for snippet in result['code_snippets']:
                    # Python imports
                    for match in re.findall(r'^import\s+(\w+)', snippet, re.MULTILINE):
                        imports[match] = imports.get(match, 0) + 1
                    for match in re.findall(r'^from\s+(\w+)', snippet, re.MULTILINE):
                        imports[match] = imports.get(match, 0) + 1
                    
                    # JavaScript/TypeScript imports
                    for match in re.findall(r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]', snippet):
                        imports[match] = imports.get(match, 0) + 1
        
        return imports
    
    def _analyze_error_patterns(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """エラーパターンを分析"""
        patterns = []
        error_types = {}
        
        for result in results:
            if result.get('status') == 'failed' and 'error' in result:
                error_type = result['error'].get('type', 'unknown')
                error_types[error_type] = error_types.get(error_type, 0) + 1
        
        if error_types:
            patterns.append({
                'type': 'errors',
                'description': '頻出するエラータイプ',
                'data': error_types,
                'confidence': 0.95
            })
        
        return patterns
    
    def _analyze_success_patterns(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """成功パターンを分析"""
        patterns = []
        success_factors = {
            'test_coverage': [],
            'execution_time': [],
            'code_quality': []
        }
        
        for result in results:
            if result.get('status') == 'completed':
                if 'metrics' in result:
                    if 'test_coverage' in result['metrics']:
                        success_factors['test_coverage'].append(result['metrics']['test_coverage'])
                    if 'execution_time' in result['metrics']:
                        success_factors['execution_time'].append(result['metrics']['execution_time'])
                    if 'code_quality' in result['metrics']:
                        success_factors['code_quality'].append(result['metrics']['code_quality'])
        
        # 平均値を計算
        for factor, values in success_factors.items():
            if values:
                avg_value = sum(values) / len(values)
                patterns.append({
                    'type': 'success_factor',
                    'description': f'{factor}の平均値',
                    'data': {'average': avg_value, 'samples': len(values)},
                    'confidence': min(0.7 + len(values) * 0.05, 1.0)
                })
        
        return patterns
    
    def _generate_insights(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """パターンからインサイトを生成"""
        insights = []
        
        # ファイル構造に関するインサイト
        file_patterns = next((p for p in patterns if p['type'] == 'file_structure'), None)
        if file_patterns:
            most_common = max(file_patterns['data'].items(), key=lambda x: x[1])
            insights.append(f"最も頻繁に作成されるファイルタイプは {most_common[0]} です（{most_common[1]}回）")
        
        # エラーに関するインサイト
        error_patterns = next((p for p in patterns if p['type'] == 'errors'), None)
        if error_patterns:
            total_errors = sum(error_patterns['data'].values())
            insights.append(f"合計 {total_errors} 件のエラーが発生しました")
        
        # 成功要因に関するインサイト
        success_patterns = [p for p in patterns if p['type'] == 'success_factor']
        for pattern in success_patterns:
            if 'test_coverage' in pattern['description']:
                avg = pattern['data']['average']
                insights.append(f"平均テストカバレッジは {avg:.1f}% です")
        
        return insights
    
    def _generate_recommendations(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """パターンから推奨事項を生成"""
        recommendations = []
        
        # インポートに基づく推奨
        import_patterns = next((p for p in patterns if p['type'] == 'imports'), None)
        if import_patterns:
            top_imports = sorted(import_patterns['data'].items(), key=lambda x: x[1], reverse=True)[:3]
            recommendations.append(
                f"頻繁に使用されるライブラリ（{', '.join([i[0] for i in top_imports])}）は"
                f"プロジェクトテンプレートに含めることを検討してください"
            )
        
        # エラーに基づく推奨
        error_patterns = next((p for p in patterns if p['type'] == 'errors'), None)
        if error_patterns and error_patterns['data']:
            most_common_error = max(error_patterns['data'].items(), key=lambda x: x[1])
            recommendations.append(
                f"'{most_common_error[0]}' エラーが最も頻繁に発生しています。"
                f"このエラーを防ぐためのガイドラインを作成することを推奨します"
            )
        
        # 成功要因に基づく推奨
        success_patterns = [p for p in patterns if p['type'] == 'success_factor']
        for pattern in success_patterns:
            if 'test_coverage' in pattern['description'] and pattern['data']['average'] < 80:
                recommendations.append(
                    "テストカバレッジが80%未満です。品質基準を満たすため、"
                    "より包括的なテストの作成を推奨します"
                )
        
        return recommendations
    
    def _save_analysis(self, analysis: Dict[str, Any]):
        """分析結果を保存"""
        timestamp = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
        
        # 個別の分析結果を保存
        analysis_file = self.feedback_path / f'analysis-{self.spec_name}-{timestamp}.json'
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        # パターンデータベースを更新
        patterns_db_file = self.patterns_path / 'patterns-db.json'
        if patterns_db_file.exists():
            with open(patterns_db_file, 'r') as f:
                patterns_db = json.load(f)
        else:
            patterns_db = {'patterns': [], 'last_updated': None}
        
        # 新しいパターンを追加
        patterns_db['patterns'].extend(analysis['patterns'])
        patterns_db['last_updated'] = analysis['timestamp']
        
        with open(patterns_db_file, 'w') as f:
            json.dump(patterns_db, f, indent=2)
        
        print(f"✅ Analysis saved to {analysis_file}")
        print(f"📊 Patterns database updated")

def main():
    """CLI エントリーポイント"""
    import argparse
    
    parser = argparse.ArgumentParser(description='実装結果を分析してパターンを抽出')
    parser.add_argument('--spec', required=True, help='仕様名')
    parser.add_argument('--pr', type=int, required=True, help='PR番号')
    
    args = parser.parse_args()
    
    analyzer = FeedbackAnalyzer(args.spec)
    analysis = analyzer.analyze_implementation(args.pr)
    
    # 結果を表示
    print("\n📊 分析結果:")
    print(f"仕様: {analysis['spec_name']}")
    print(f"PR: #{analysis['pr_number']}")
    
    if analysis['insights']:
        print("\n💡 インサイト:")
        for insight in analysis['insights']:
            print(f"  - {insight}")
    
    if analysis['recommendations']:
        print("\n📝 推奨事項:")
        for rec in analysis['recommendations']:
            print(f"  - {rec}")

if __name__ == '__main__':
    main()