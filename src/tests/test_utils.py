"""
ユーティリティクラスのテストケース
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_framework import TestSuite, assert_equal, assert_true, assert_false
from utils.performance_optimizer import PerformanceOptimizer
from utils.logger import Logger, ErrorHandler

def test_performance_optimizer_memory_monitoring():
    """パフォーマンス最適化のメモリ監視テスト"""
    optimizer = PerformanceOptimizer()
    
    # メモリ情報を取得
    memory_info = optimizer.monitor_memory()
    assert_true('rss' in memory_info, "RSSメモリ情報が含まれる")
    assert_true('vms' in memory_info, "VMSメモリ情報が含まれる")
    assert_true('percent' in memory_info, "使用率情報が含まれる")
    assert_true(memory_info['rss'] >= 0, "RSSメモリは0以上")
    return True

def test_performance_optimizer_memory_cleanup():
    """パフォーマンス最適化のメモリクリーンアップテスト"""
    optimizer = PerformanceOptimizer()
    
    # メモリクリーンアップを実行（エラーがないことを確認）
    try:
        optimizer.cleanup_memory()
        assert_true(True, "メモリクリーンアップが正常に実行される")
    except Exception as e:
        assert_false(True, f"メモリクリーンアップでエラー: {str(e)}")
    return True

def test_performance_optimizer_data_optimization():
    """パフォーマンス最適化のデータ構造最適化テスト"""
    optimizer = PerformanceOptimizer()
    
    # テストデータ
    test_data = {
        'name': '  テスト太郎  ',
        'items': ['  item1  ', '  item2  '],
        'nested': {
            'value': '  値  '
        }
    }
    
    optimized = optimizer.optimize_data_structures(test_data)
    assert_equal(optimized['name'], 'テスト太郎', "文字列の空白が削除される")
    assert_equal(optimized['items'][0], 'item1', "リスト内の文字列も最適化される")
    assert_equal(optimized['nested']['value'], '値', "ネストした値も最適化される")
    return True

def test_performance_optimizer_window_config_optimization():
    """パフォーマンス最適化のウィンドウ設定最適化テスト"""
    optimizer = PerformanceOptimizer()
    
    # テスト設定
    config = {
        'title': 'テストウィンドウ',
        'layout': [],
        'grab_anywhere': False,
        'keep_on_top': False,
        'modal': False
    }
    
    optimized = optimizer.optimize_window_creation(config)
    assert_equal(optimized['title'], 'テストウィンドウ', "タイトルは保持される")
    assert_true(optimized['resizable'], "resizableがデフォルトで設定される")
    assert_true(optimized['finalize'], "finalizeがデフォルトで設定される")
    assert_true('grab_anywhere' not in optimized, "不要な設定が削除される")
    return True

def test_logger_creation():
    """ロガーの作成テスト"""
    logger = Logger("test_logger")
    assert_equal(logger.name, "test_logger", "ロガー名が正しく設定される")
    return True

def test_logger_logging():
    """ロガーのログ出力テスト"""
    logger = Logger("test_logger")
    
    # 各レベルのログを出力（エラーがないことを確認）
    try:
        logger.debug("デバッグメッセージ")
        logger.info("情報メッセージ")
        logger.warning("警告メッセージ")
        logger.error("エラーメッセージ")
        logger.critical("致命的エラーメッセージ")
        assert_true(True, "すべてのログレベルが正常に出力される")
    except Exception as e:
        assert_false(True, f"ログ出力でエラー: {str(e)}")
    return True

def test_logger_performance_logging():
    """ロガーのパフォーマンスログテスト"""
    logger = Logger("test_logger")
    
    # パフォーマンスログを出力
    try:
        logger.log_performance("test_function", 1.5, 100.0, additional_info="テスト")
        assert_true(True, "パフォーマンスログが正常に出力される")
    except Exception as e:
        assert_false(True, f"パフォーマンスログでエラー: {str(e)}")
    return True

def test_logger_user_action_logging():
    """ロガーのユーザーアクションログテスト"""
    logger = Logger("test_logger")
    
    # ユーザーアクションログを出力
    try:
        logger.log_user_action("button_click", {"button": "test_button"})
        assert_true(True, "ユーザーアクションログが正常に出力される")
    except Exception as e:
        assert_false(True, f"ユーザーアクションログでエラー: {str(e)}")
    return True

def test_error_handler_exception_handling():
    """エラーハンドラーの例外処理テスト"""
    logger = Logger("test_logger")
    error_handler = ErrorHandler(logger)
    
    # テスト用の例外
    test_exception = ValueError("テストエラー")
    
    # 例外処理を実行
    try:
        message = error_handler.handle_exception(test_exception, {"context": "test"})
        assert_true(isinstance(message, str), "エラーメッセージが文字列で返される")
        assert_true("入力値が正しくありません。" in message, "ValueErrorに対応するメッセージが返される")
    except Exception as e:
        assert_false(True, f"エラーハンドリングでエラー: {str(e)}")
    return True

def test_error_handler_safe_execute():
    """エラーハンドラーの安全実行テスト"""
    logger = Logger("test_logger")
    error_handler = ErrorHandler(logger)
    
    # 正常な関数の実行
    def normal_function():
        return "success"
    
    result = error_handler.safe_execute(normal_function)
    assert_equal(result, "success", "正常な関数は結果を返す")
    
    # 例外を発生させる関数の実行
    def error_function():
        raise ValueError("テストエラー")
    
    result, error = error_handler.safe_execute(error_function)
    assert_equal(result, None, "エラー時は結果がNone")
    assert_true("入力値が正しくありません。" in error, "ValueErrorに対応するメッセージが返される")
    return True

def run_utils_tests():
    """ユーティリティテストを実行"""
    suite = TestSuite("ユーティリティテスト")
    
    # パフォーマンス最適化のテスト
    suite.add_test(test_performance_optimizer_memory_monitoring)
    suite.add_test(test_performance_optimizer_memory_cleanup)
    suite.add_test(test_performance_optimizer_data_optimization)
    suite.add_test(test_performance_optimizer_window_config_optimization)
    
    # ロガーのテスト
    suite.add_test(test_logger_creation)
    suite.add_test(test_logger_logging)
    suite.add_test(test_logger_performance_logging)
    suite.add_test(test_logger_user_action_logging)
    
    # エラーハンドラーのテスト
    suite.add_test(test_error_handler_exception_handling)
    suite.add_test(test_error_handler_safe_execute)
    
    return suite.run_tests()

if __name__ == "__main__":
    run_utils_tests()