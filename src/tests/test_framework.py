"""
テストフレームワーク
単体テストと統合テストの基盤
"""
import unittest
import sys
import os
from typing import Any, Dict, List, Optional
import time
from datetime import datetime

# プロジェクトのルートディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestResult:
    """テスト結果クラス"""
    
    def __init__(self, test_name: str, passed: bool, message: str = "", execution_time: float = 0):
        self.test_name = test_name
        self.passed = passed
        self.message = message
        self.execution_time = execution_time
        self.timestamp = datetime.now()
    
    def __str__(self):
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {self.test_name} ({self.execution_time:.4f}s) - {self.message}"

class TestSuite:
    """テストスイートクラス"""
    
    def __init__(self, name: str):
        self.name = name
        self.tests = []
        self.results = []
    
    def add_test(self, test_func, *args, **kwargs):
        """テストを追加"""
        self.tests.append({
            'function': test_func,
            'args': args,
            'kwargs': kwargs
        })
    
    def run_tests(self) -> Dict[str, Any]:
        """テストを実行"""
        print(f"テストスイート '{self.name}' を実行中...")
        
        for test in self.tests:
            test_name = test['function'].__name__
            start_time = time.time()
            
            try:
                # テストを実行
                result = test['function'](*test['args'], **test['kwargs'])
                execution_time = time.time() - start_time
                
                if result is True or result is None:
                    test_result = TestResult(test_name, True, "テスト成功", execution_time)
                else:
                    test_result = TestResult(test_name, False, f"テスト失敗: {result}", execution_time)
                
            except Exception as e:
                execution_time = time.time() - start_time
                test_result = TestResult(test_name, False, f"例外発生: {str(e)}", execution_time)
            
            self.results.append(test_result)
            print(test_result)
        
        # 辞書形式で結果を返す
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)
        failed_tests = total_tests - passed_tests
        total_time = sum(r.execution_time for r in self.results)
        
        return {
            'results': self.results,
            'total': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'total_time': total_time
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """テスト結果のサマリーを取得"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)
        failed_tests = total_tests - passed_tests
        total_time = sum(r.execution_time for r in self.results)
        
        return {
            'total': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'total_time': total_time
        }

class TestFramework:
    """テストフレームワークのメインクラス"""
    
    def __init__(self):
        self.suites = []
        self.global_setup = None
        self.global_teardown = None
    
    def add_suite(self, suite: TestSuite):
        """テストスイートを追加"""
        self.suites.append(suite)
    
    def set_global_setup(self, setup_func):
        """グローバルセットアップを設定"""
        self.global_setup = setup_func
    
    def set_global_teardown(self, teardown_func):
        """グローバルティアダウンを設定"""
        self.global_teardown = teardown_func
    
    def run_all_tests(self) -> Dict[str, Any]:
        """すべてのテストを実行"""
        print("=" * 50)
        print("テストフレームワーク開始")
        print("=" * 50)
        
        # グローバルセットアップ
        if self.global_setup:
            try:
                self.global_setup()
                print("グローバルセットアップ完了")
            except Exception as e:
                print(f"グローバルセットアップエラー: {str(e)}")
                return {'error': str(e)}
        
        all_results = []
        suite_summaries = []
        
        # 各テストスイートを実行
        for suite in self.suites:
            try:
                results = suite.run_tests()
                all_results.extend(results)
                summary = suite.get_summary()
                suite_summaries.append({
                    'suite_name': suite.name,
                    'summary': summary
                })
            except Exception as e:
                print(f"テストスイート '{suite.name}' でエラー: {str(e)}")
        
        # グローバルティアダウン
        if self.global_teardown:
            try:
                self.global_teardown()
                print("グローバルティアダウン完了")
            except Exception as e:
                print(f"グローバルティアダウンエラー: {str(e)}")
        
        # 全体のサマリー
        total_tests = len(all_results)
        passed_tests = sum(1 for r in all_results if r.passed)
        failed_tests = total_tests - passed_tests
        total_time = sum(r.execution_time for r in all_results)
        
        overall_summary = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'total_time': total_time,
            'suite_summaries': suite_summaries
        }
        
        # 結果を表示
        print("=" * 50)
        print("テスト結果サマリー")
        print("=" * 50)
        print(f"総テスト数: {total_tests}")
        print(f"成功: {passed_tests}")
        print(f"失敗: {failed_tests}")
        print(f"成功率: {overall_summary['success_rate']:.1f}%")
        print(f"総実行時間: {total_time:.4f}秒")
        
        return overall_summary

# デコレータ
def test_case(name: str = None):
    """テストケースデコレータ"""
    def decorator(func):
        func.test_name = name or func.__name__
        return func
    return decorator

def setup_test(func):
    """セットアップデコレータ"""
    func.is_setup = True
    return func

def teardown_test(func):
    """ティアダウンデコレータ"""
    func.is_teardown = True
    return func

# アサーション関数
def assert_equal(actual, expected, message: str = ""):
    """等価性をアサート"""
    if actual != expected:
        raise AssertionError(f"{message} - 期待値: {expected}, 実際の値: {actual}")
    return True

def assert_not_equal(actual, expected, message: str = ""):
    """非等価性をアサート"""
    if actual == expected:
        raise AssertionError(f"{message} - 値が等しい: {actual}")
    return True

def assert_true(condition, message: str = ""):
    """真をアサート"""
    if not condition:
        raise AssertionError(f"{message} - 条件が偽: {condition}")
    return True

def assert_false(condition, message: str = ""):
    """偽をアサート"""
    if condition:
        raise AssertionError(f"{message} - 条件が真: {condition}")
    return True

def assert_raises(exception_class, func, *args, **kwargs):
    """例外が発生することをアサート"""
    try:
        func(*args, **kwargs)
        raise AssertionError(f"例外 {exception_class.__name__} が発生しませんでした")
    except exception_class:
        return True
    except Exception as e:
        raise AssertionError(f"期待した例外 {exception_class.__name__} ではなく {type(e).__name__} が発生: {str(e)}")

# モッククラス
class Mock:
    """モックオブジェクトクラス"""
    
    def __init__(self, **kwargs):
        self._attributes = kwargs
        self._calls = []
    
    def __getattr__(self, name):
        if name in self._attributes:
            return self._attributes[name]
        return lambda *args, **kwargs: None
    
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._attributes[name] = value
    
    def called_with(self, *args, **kwargs):
        """指定された引数で呼び出されたかチェック"""
        call = {'args': args, 'kwargs': kwargs}
        return call in self._calls
    
    def call_count(self):
        """呼び出し回数を取得"""
        return len(self._calls)