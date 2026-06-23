"""
包括的テストランナー
すべてのテストを統合して実行
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_framework import TestSuite, TestFramework
from test_models import run_model_tests
from test_services import run_service_tests
from test_utils import run_utils_tests
from test_event_handling import run_event_handling_tests
from test_functional_operations import run_functional_operation_tests
from test_interactive_events import run_interactive_event_tests

def run_all_tests():
    """すべてのテストを実行"""
    print("=" * 80)
    print("包括的テストスイート実行開始")
    print("=" * 80)
    
    # テストフレームワークを初期化
    framework = TestFramework()
    
    # 各テストスイートを実行
    test_suites = [
        ("データモデルテスト", run_model_tests),
        ("サービステスト", run_service_tests),
        ("ユーティリティテスト", run_utils_tests),
        ("イベント処理テスト", run_event_handling_tests),
        ("機能操作テスト", run_functional_operation_tests),
        ("インタラクティブイベントテスト", run_interactive_event_tests)
    ]
    
    total_passed = 0
    total_failed = 0
    total_tests = 0
    
    for suite_name, test_function in test_suites:
        print(f"\n{'=' * 60}")
        print(f"実行中: {suite_name}")
        print(f"{'=' * 60}")
        
        try:
            result = test_function()
            if result:
                passed = result.get('passed', 0)
                failed = result.get('failed', 0)
                total_passed += passed
                total_failed += failed
                total_tests += passed + failed
                
                print(f"✅ {suite_name} 完了: {passed} 成功, {failed} 失敗")
            else:
                print(f"❌ {suite_name} 実行失敗")
                total_failed += 1
                total_tests += 1
                
        except Exception as e:
            print(f"❌ {suite_name} 実行中にエラー: {str(e)}")
            total_failed += 1
            total_tests += 1
    
    # 最終結果を表示
    print(f"\n{'=' * 80}")
    print("テスト実行完了")
    print(f"{'=' * 80}")
    print(f"総テスト数: {total_tests}")
    print(f"成功: {total_passed}")
    print(f"失敗: {total_failed}")
    print(f"成功率: {(total_passed / total_tests * 100):.1f}%" if total_tests > 0 else "0%")
    
    if total_failed == 0:
        print("🎉 すべてのテストが成功しました！")
        return True
    else:
        print(f"⚠️  {total_failed} 個のテストが失敗しました。")
        return False

def run_quick_tests():
    """クイックテスト（基本的なテストのみ）"""
    print("=" * 80)
    print("クイックテストスイート実行開始")
    print("=" * 80)
    
    # 基本的なテストのみを実行
    test_suites = [
        ("データモデルテスト", run_model_tests),
        ("サービステスト", run_service_tests),
        ("イベント処理テスト", run_event_handling_tests)
    ]
    
    total_passed = 0
    total_failed = 0
    total_tests = 0
    
    for suite_name, test_function in test_suites:
        print(f"\n{'=' * 60}")
        print(f"実行中: {suite_name}")
        print(f"{'=' * 60}")
        
        try:
            result = test_function()
            if result:
                passed = result.get('passed', 0)
                failed = result.get('failed', 0)
                total_passed += passed
                total_failed += failed
                total_tests += passed + failed
                
                print(f"✅ {suite_name} 完了: {passed} 成功, {failed} 失敗")
            else:
                print(f"❌ {suite_name} 実行失敗")
                total_failed += 1
                total_tests += 1
                
        except Exception as e:
            print(f"❌ {suite_name} 実行中にエラー: {str(e)}")
            total_failed += 1
            total_tests += 1
    
    # 最終結果を表示
    print(f"\n{'=' * 80}")
    print("クイックテスト実行完了")
    print(f"{'=' * 80}")
    print(f"総テスト数: {total_tests}")
    print(f"成功: {total_passed}")
    print(f"失敗: {total_failed}")
    print(f"成功率: {(total_passed / total_tests * 100):.1f}%" if total_tests > 0 else "0%")
    
    if total_failed == 0:
        print("🎉 すべてのクイックテストが成功しました！")
        return True
    else:
        print(f"⚠️  {total_failed} 個のクイックテストが失敗しました。")
        return False

def run_ui_tests():
    """UIテスト（ウィンドウ作成とレイアウトテスト）"""
    print("=" * 80)
    print("UIテストスイート実行開始")
    print("=" * 80)
    
    # UI関連のテストのみを実行
    test_suites = [
        ("機能操作テスト", run_functional_operation_tests),
        ("インタラクティブイベントテスト", run_interactive_event_tests)
    ]
    
    total_passed = 0
    total_failed = 0
    total_tests = 0
    
    for suite_name, test_function in test_suites:
        print(f"\n{'=' * 60}")
        print(f"実行中: {suite_name}")
        print(f"{'=' * 60}")
        
        try:
            result = test_function()
            if result:
                passed = result.get('passed', 0)
                failed = result.get('failed', 0)
                total_passed += passed
                total_failed += failed
                total_tests += passed + failed
                
                print(f"✅ {suite_name} 完了: {passed} 成功, {failed} 失敗")
            else:
                print(f"❌ {suite_name} 実行失敗")
                total_failed += 1
                total_tests += 1
                
        except Exception as e:
            print(f"❌ {suite_name} 実行中にエラー: {str(e)}")
            total_failed += 1
            total_tests += 1
    
    # 最終結果を表示
    print(f"\n{'=' * 80}")
    print("UIテスト実行完了")
    print(f"{'=' * 80}")
    print(f"総テスト数: {total_tests}")
    print(f"成功: {total_passed}")
    print(f"失敗: {total_failed}")
    print(f"成功率: {(total_passed / total_tests * 100):.1f}%" if total_tests > 0 else "0%")
    
    if total_failed == 0:
        print("🎉 すべてのUIテストが成功しました！")
        return True
    else:
        print(f"⚠️  {total_failed} 個のUIテストが失敗しました。")
        return False

def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="包括的テストランナー")
    parser.add_argument("--mode", choices=["all", "quick", "ui"], default="all",
                       help="テストモードを選択 (all: 全テスト, quick: クイックテスト, ui: UIテスト)")
    
    args = parser.parse_args()
    
    if args.mode == "all":
        success = run_all_tests()
    elif args.mode == "quick":
        success = run_quick_tests()
    elif args.mode == "ui":
        success = run_ui_tests()
    else:
        print("無効なモードが指定されました。")
        success = False
    
    # 終了コードを設定
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()