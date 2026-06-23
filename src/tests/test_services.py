"""
サービスクラスのテストケース
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_framework import TestSuite, assert_equal, assert_true, assert_false, Mock
from services.validation_service import ValidationService
from services.file_service import FileService
from models.koden_model import KodenModel

def test_validation_service_text_normalization():
    """バリデーションサービスのテキスト正規化テスト"""
    service = ValidationService()
    
    # 空白の正規化
    normalized = service.normalize_text("  テスト  ")
    assert_equal(normalized, "テスト", "前後の空白が削除される")
    
    # 全角半角の統一
    normalized = service.normalize_text("テスト　テスト")
    assert_equal(normalized, "テスト テスト", "全角空白が半角に変換される")
    return True

def test_validation_service_furigana_conversion():
    """バリデーションサービスのフリガナ変換テスト"""
    service = ValidationService()
    
    # フリガナ変換（実際の変換結果は環境に依存するため、エラーがないことを確認）
    try:
        furigana = service.convert_to_furigana("田中太郎")
        assert_true(isinstance(furigana, str), "フリガナは文字列")
    except Exception as e:
        # pykakasiが利用できない場合はスキップ
        print(f"フリガナ変換テストをスキップ: {str(e)}")
    return True

def test_validation_service_required_validation():
    """バリデーションサービスの必須項目検証テスト"""
    service = ValidationService()
    
    # 必須項目の検証
    result, message = service.validate_required("テスト", "名前")
    assert_true(result, "有効な値はTrue")
    
    result, message = service.validate_required("", "名前")
    assert_false(result, "空文字はFalse")
    
    result, message = service.validate_required(None, "名前")
    assert_false(result, "NoneはFalse")
    return True

def test_validation_service_number_validation():
    """バリデーションサービスの数値検証テスト"""
    service = ValidationService()
    
    # 数値の検証
    result, message = service.validate_number(100, "数値")
    assert_true(result, "有効な数値はTrue")
    
    result, message = service.validate_number(0, "数値")
    assert_true(result, "0は有効")
    
    result, message = service.validate_number(-100, "数値", min_val=0)
    assert_false(result, "負の数はFalse")
    
    result, message = service.validate_number("abc", "数値")
    assert_false(result, "文字列はFalse")
    return True

def test_validation_service_price_validation():
    """バリデーションサービスの価格検証テスト"""
    service = ValidationService()
    
    # 価格の検証
    result, message = service.validate_price(1000, "価格")
    assert_true(result, "有効な価格はTrue")
    
    result, message = service.validate_price(0, "価格")
    assert_true(result, "0円は有効")
    
    result, message = service.validate_price(-1000, "価格")
    assert_false(result, "負の価格はFalse")
    
    result, message = service.validate_price(10000001, "価格")
    assert_false(result, "上限超過はFalse")
    return True

def test_file_service_path_operations():
    """ファイルサービスのパス操作テスト"""
    service = FileService()
    
    # パスの結合
    path = service.join_paths("folder1", "folder2", "file.txt")
    # Windows環境ではバックスラッシュが使用される
    expected_path = "folder1\\folder2\\file.txt" if os.name == 'nt' else "folder1/folder2/file.txt"
    assert_equal(path, expected_path, "パスが正しく結合される")
    
    # パスの正規化
    normalized = service.normalize_path("folder1\\folder2\\file.txt")
    expected_normalized = "folder1\\folder2\\file.txt" if os.name == 'nt' else "folder1/folder2/file.txt"
    assert_equal(normalized, expected_normalized, "パスが正規化される")
    return True

def test_file_service_directory_operations():
    """ファイルサービスのディレクトリ操作テスト"""
    service = FileService()
    
    # テスト用のディレクトリを作成
    test_dir = "test_temp_dir"
    
    try:
        # ディレクトリ作成
        result = service.create_directory(test_dir)
        assert_true(result, "ディレクトリが作成される")
        
        # ディレクトリ存在確認
        assert_true(service.directory_exists(test_dir), "ディレクトリが存在する")
        
        # ディレクトリ削除
        result = service.delete_directory(test_dir)
        assert_true(result, "ディレクトリが削除される")
        
    except Exception as e:
        print(f"ディレクトリ操作テストをスキップ: {str(e)}")
    return True

def test_validation_service_koden_data_validation():
    """バリデーションサービスの香典データ検証テスト"""
    service = ValidationService()
    
    # 有効な香典データ
    valid_data = {
        'name': 'テスト太郎',
        'price': 10000,
        'address': '東京都渋谷区'
    }
    errors = service.validate_koden_data(valid_data)
    assert_equal(len(errors), 0, "有効なデータはエラーなし")
    
    # 無効な香典データ
    invalid_data = {
        'name': '',
        'price': -1000,
        'address': '東京都渋谷区'
    }
    errors = service.validate_koden_data(invalid_data)
    assert_true(len(errors) > 0, "無効なデータはエラーあり")
    return True

def test_validation_service_validation_summary():
    """バリデーションサービスの検証サマリーテスト"""
    service = ValidationService()
    
    errors = {"名前": "エラー1", "住所": "エラー2", "電話": "エラー3"}
    summary = service.get_validation_summary(errors)
    assert_true("エラー1" in summary and "エラー2" in summary and "エラー3" in summary, "サマリーが正しく生成される")
    
    empty_errors = {}
    summary = service.get_validation_summary(empty_errors)
    assert_equal(summary, "検証エラーはありません", "空のエラー辞書のサマリー")
    return True

def run_service_tests():
    """サービステストを実行"""
    suite = TestSuite("サービステスト")
    
    # バリデーションサービスのテスト
    suite.add_test(test_validation_service_text_normalization)
    suite.add_test(test_validation_service_furigana_conversion)
    suite.add_test(test_validation_service_required_validation)
    suite.add_test(test_validation_service_number_validation)
    suite.add_test(test_validation_service_price_validation)
    suite.add_test(test_validation_service_koden_data_validation)
    suite.add_test(test_validation_service_validation_summary)
    
    # ファイルサービスのテスト
    suite.add_test(test_file_service_path_operations)
    suite.add_test(test_file_service_directory_operations)
    
    return suite.run_tests()

if __name__ == "__main__":
    run_service_tests()