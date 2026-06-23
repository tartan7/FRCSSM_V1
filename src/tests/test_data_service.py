"""
データサービスの統合テストケース
ExcelService はモックして I/O なしで検証する
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# test_base_controller.py がモジュールレベルで services.data_service を MagicMock に
# 置き換えるため、本物のモジュールを強制的に再ロードしてから import する
sys.modules.pop('services.data_service', None)

from unittest.mock import MagicMock, patch
from test_framework import TestSuite, assert_equal, assert_true, assert_false
from services.data_service import DataService
from models.flower_model import FlowerModel
from models.condolence_model import CondolenceModel
from models.incense_model import IncenseModel
from models.offering_model import OfferingModel


def _make_service():
    """DataService インスタンスを返す（ExcelService の Excel I/O はモック済み）"""
    service = DataService()
    service.excel_service = MagicMock()
    return service


# --- 初期化 ---

def test_data_service_creation():
    """DataService: 必要なサブサービスが初期化される"""
    service = DataService()
    assert_true(service.excel_service is not None, "excel_service が初期化される")
    assert_true(service.file_service is not None, "file_service が初期化される")
    assert_true(service.validation_service is not None, "validation_service が初期化される")
    assert_true(service.operations_service is not None, "operations_service が初期化される")
    return True


def test_data_service_has_methods():
    """DataService: 必要なメソッドが存在する"""
    service = DataService()
    assert_true(hasattr(service, 'get_koden_data'), "get_koden_data が存在する")
    assert_true(hasattr(service, 'save_koden_data'), "save_koden_data が存在する")
    assert_true(hasattr(service, 'get_funeral_data'), "get_funeral_data が存在する")
    assert_true(hasattr(service, 'save_funeral_data'), "save_funeral_data が存在する")
    assert_true(hasattr(service, 'get_flower_data'), "get_flower_data が存在する")
    assert_true(hasattr(service, 'save_flower_data'), "save_flower_data が存在する")
    assert_true(hasattr(service, 'get_condolence_data'), "get_condolence_data が存在する")
    assert_true(hasattr(service, 'save_condolence_data'), "save_condolence_data が存在する")
    assert_true(hasattr(service, 'get_offering_data'), "get_offering_data が存在する")
    assert_true(hasattr(service, 'get_incense_data'), "get_incense_data が存在する")
    assert_true(hasattr(service, 'cleanup'), "cleanup が存在する")
    return True


# --- スタブメソッド（現在 stub 実装のもの） ---

def test_data_service_get_funeral_data_returns_dict():
    """DataService.get_funeral_data: 辞書を返す"""
    service = DataService()
    result = service.get_funeral_data()
    assert_true(isinstance(result, dict), "get_funeral_data は辞書を返す")
    return True


def test_data_service_get_construction_data_returns_list():
    """DataService.get_construction_data: リストを返す"""
    service = DataService()
    result = service.get_construction_data()
    assert_true(isinstance(result, list), "get_construction_data はリストを返す")
    return True


def test_data_service_get_offering_data_returns_list():
    """DataService.get_offering_data: リストを返す"""
    service = DataService()
    result = service.get_offering_data()
    assert_true(isinstance(result, list), "get_offering_data はリストを返す")
    return True


def test_data_service_get_incense_data_returns_list():
    """DataService.get_incense_data: リストを返す"""
    service = DataService()
    result = service.get_incense_data()
    assert_true(isinstance(result, list), "get_incense_data はリストを返す")
    return True


def test_data_service_save_incense_data_returns_true():
    """DataService.save_incense_data: Trueを返す（stub）"""
    service = DataService()
    result = service.save_incense_data({})
    assert_true(result, "save_incense_data は True を返す")
    return True


def test_data_service_save_funeral_data_valid():
    """DataService.save_funeral_data: 有効データは True"""
    service = DataService()
    valid_data = {
        'deceased_name': '山田太郎',
        'family_name': '山田花子',
        'age': 80
    }
    result = service.save_funeral_data(valid_data)
    assert_true(result, "有効な葬儀データは True")
    return True


def test_data_service_save_funeral_data_invalid():
    """DataService.save_funeral_data: 禁止文字を含む故人名は False"""
    service = DataService()
    # validate_name は禁止文字(<)でエラーを返す
    invalid_data = {
        'deceased_name': '<script>xss</script>',
    }
    result = service.save_funeral_data(invalid_data)
    assert_false(result, "禁止文字を含む葬儀データは False")
    return True


def test_data_service_save_construction_data_valid():
    """DataService.save_construction_data: 有効データは True"""
    service = DataService()
    valid_data = {
        'service_type': '通常',
        'date': '令和6年4月15日',
        'venue': '〇〇斎場'
    }
    result = service.save_construction_data(valid_data)
    assert_true(result, "有効な施工データは True")
    return True


def test_data_service_save_offering_data_valid():
    """DataService.save_offering_data: 有効データは True"""
    service = DataService()
    valid_data = {
        'offering_type': '果物',
        'quantity': 1
    }
    result = service.save_offering_data(valid_data)
    assert_true(result, "有効な供物データは True")
    return True


# --- 香典データ ---

def test_data_service_get_koden_data_exception_returns_empty():
    """DataService.get_koden_data: 例外発生時は空辞書"""
    service = _make_service()
    service.excel_service.read_koden_data.side_effect = Exception("Excel error")
    result = service.get_koden_data(1)
    assert_equal(result, {}, "例外発生時は空辞書")
    return True


def test_data_service_get_koden_data_success():
    """DataService.get_koden_data: 正常時は ExcelService の結果を返す"""
    service = _make_service()
    expected = {'name': '田中太郎', 'price': 10000}
    service.excel_service.read_koden_data.return_value = expected
    result = service.get_koden_data(1)
    assert_equal(result, expected, "ExcelService の返却値をそのまま返す")
    return True


def test_data_service_save_koden_data_invalid():
    """DataService.save_koden_data: バリデーション失敗は False"""
    service = _make_service()
    invalid_data = {'name': '', 'price': -1000, 'address': ''}
    result = service.save_koden_data(1, invalid_data)
    assert_false(result, "無効な香典データは False")
    service.excel_service.update_koden_data.assert_not_called()
    return True


def test_data_service_save_koden_data_valid():
    """DataService.save_koden_data: 有効データは Excel に保存して True"""
    service = _make_service()
    service.excel_service.update_koden_data.return_value = None
    valid_data = {'name': '田中太郎', 'price': 10000, 'address': '東京都'}
    result = service.save_koden_data(1, valid_data)
    assert_true(result, "有効な香典データは True")
    assert_true(service.excel_service.update_koden_data.called,
                "update_koden_data が呼ばれる")
    return True


def test_data_service_save_koden_data_excel_exception():
    """DataService.save_koden_data: Excel 例外は False"""
    service = _make_service()
    service.excel_service.update_koden_data.side_effect = Exception("Excel error")
    valid_data = {'name': '田中太郎', 'price': 10000, 'address': '東京都'}
    result = service.save_koden_data(1, valid_data)
    assert_false(result, "Excel 例外発生時は False")
    return True


# --- 正規化ロジック ---

def test_data_service_normalize_koden_data_trims_spaces():
    """DataService._normalize_koden_data: 前後空白が除去される"""
    service = DataService()
    data = {'name': '  田中太郎  ', 'address': '  東京都  ', 'price': 5000}
    result = service._normalize_koden_data(data)
    assert_equal(result['name'], '田中太郎', "名前の空白が除去される")
    assert_equal(result['address'], '東京都', "住所の空白が除去される")
    assert_equal(result['price'], 5000, "価格はそのまま")
    return True


def test_data_service_normalize_koden_data_boolean_fields():
    """DataService._normalize_koden_data: receipt/check は bool に変換される"""
    service = DataService()
    data = {'receipt': 1, 'check': 0}
    result = service._normalize_koden_data(data)
    assert_true(isinstance(result['receipt'], bool), "receipt は bool")
    assert_true(isinstance(result['check'], bool), "check は bool")
    assert_true(result['receipt'], "receipt=1 は True")
    assert_false(result['check'], "check=0 は False")
    return True


def test_data_service_normalize_funeral_data_trims_spaces():
    """DataService._normalize_funeral_data: 文字列フィールドの空白が除去される"""
    service = DataService()
    data = {'deceased_name': '  山田太郎  ', 'age': 80}
    result = service._normalize_funeral_data(data)
    assert_equal(result['deceased_name'], '山田太郎', "故人名の空白が除去される")
    assert_equal(result['age'], 80, "数値フィールドはそのまま")
    return True


# --- 供花料データ ---

def test_data_service_get_flower_data_all_success():
    """DataService.get_flower_data: 全データを FlowerModel リストで返す"""
    service = _make_service()
    service.excel_service.read_all_flower_data.return_value = [
        [1, "テスト花屋", "東京都", 5000, "", False],
        [2, "鈴木花店", "大阪府", 3000, "", False],
    ]
    result = service.get_flower_data()
    assert_true(isinstance(result, list), "リストを返す")
    assert_equal(len(result), 2, "2件返る")
    assert_true(isinstance(result[0], FlowerModel), "FlowerModel のリスト")
    return True


def test_data_service_get_flower_data_exception_returns_empty():
    """DataService.get_flower_data: 例外発生時は空リスト"""
    service = _make_service()
    service.excel_service.read_all_flower_data.side_effect = Exception("error")
    result = service.get_flower_data()
    assert_equal(result, [], "例外発生時は空リスト")
    return True


def test_data_service_save_flower_data_valid():
    """DataService.save_flower_data: 有効モデルは Excel 保存して True"""
    service = _make_service()
    service.excel_service.update_flower_data.return_value = None
    flower = FlowerModel()
    flower.number = 1
    flower.name = "テスト花屋"
    flower.amount = 5000
    result = service.save_flower_data(flower)
    assert_true(result, "有効な供花料は True")
    assert_true(service.excel_service.update_flower_data.called,
                "update_flower_data が呼ばれる")
    return True


def test_data_service_save_flower_data_invalid():
    """DataService.save_flower_data: 無効モデルは False"""
    service = _make_service()
    flower = FlowerModel()
    flower.number = 0
    flower.amount = -100
    result = service.save_flower_data(flower)
    assert_false(result, "無効な供花料は False")
    service.excel_service.update_flower_data.assert_not_called()
    return True


def test_data_service_delete_flower_data_success():
    """DataService.delete_flower_data: 正常削除は True"""
    service = _make_service()
    service.excel_service.delete_flower_data.return_value = None
    result = service.delete_flower_data(1)
    assert_true(result, "正常削除は True")
    service.excel_service.delete_flower_data.assert_called_once_with(1)
    return True


def test_data_service_delete_flower_data_exception():
    """DataService.delete_flower_data: 例外発生は False"""
    service = _make_service()
    service.excel_service.delete_flower_data.side_effect = Exception("error")
    result = service.delete_flower_data(1)
    assert_false(result, "例外発生時は False")
    return True


# --- 弔辞弔電データ ---

def test_data_service_get_condolence_data_all_success():
    """DataService.get_condolence_data: 全データを CondolenceModel リストで返す"""
    service = _make_service()
    service.excel_service.read_all_condolence_data.return_value = [
        [1, "株式会社テスト", "弔辞テスト", "", False],
    ]
    result = service.get_condolence_data()
    assert_true(isinstance(result, list), "リストを返す")
    assert_equal(len(result), 1, "1件返る")
    assert_true(isinstance(result[0], CondolenceModel), "CondolenceModel のリスト")
    return True


def test_data_service_save_condolence_data_valid():
    """DataService.save_condolence_data: 有効モデルは Excel 保存して True"""
    service = _make_service()
    service.excel_service.update_condolence_data.return_value = None
    condolence = CondolenceModel()
    condolence.number = 1
    condolence.company_name = "株式会社テスト"
    result = service.save_condolence_data(condolence)
    assert_true(result, "有効な弔辞弔電は True")
    assert_true(service.excel_service.update_condolence_data.called,
                "update_condolence_data が呼ばれる")
    return True


def test_data_service_save_condolence_data_invalid():
    """DataService.save_condolence_data: 無効モデルは False"""
    service = _make_service()
    condolence = CondolenceModel()
    condolence.number = 0
    result = service.save_condolence_data(condolence)
    assert_false(result, "無効な弔辞弔電は False")
    service.excel_service.update_condolence_data.assert_not_called()
    return True


def test_data_service_delete_condolence_data_success():
    """DataService.delete_condolence_data: 正常削除は True"""
    service = _make_service()
    service.excel_service.delete_condolence_data.return_value = None
    result = service.delete_condolence_data(2)
    assert_true(result, "正常削除は True")
    service.excel_service.delete_condolence_data.assert_called_once_with(2)
    return True


# --- 設定関連 ---

def test_data_service_load_settings_returns_dict():
    """DataService.load_settings: 辞書を返す"""
    service = DataService()
    result = service.load_settings()
    assert_true(isinstance(result, dict), "辞書を返す")
    assert_true('current_path' in result, "current_path キーが含まれる")
    assert_true('vix_path' in result, "vix_path キーが含まれる")
    return True


def test_data_service_save_settings_no_path():
    """DataService.save_settings: パス設定なしは True（何もしない）"""
    service = DataService()
    result = service.save_settings({'other_setting': 'value'})
    assert_true(result, "パス設定なしでも True")
    return True


def test_data_service_save_settings_with_path():
    """DataService.save_settings: パス設定ありは True"""
    service = DataService()
    result = service.save_settings({'current_path': 'C:\\test', 'vix_path': None})
    assert_true(result, "パス設定ありでも True")
    return True


# --- クリーンアップ ---

def test_data_service_cleanup_calls_excel_close():
    """DataService.cleanup: excel_service.safe_close_excel を呼ぶ"""
    service = _make_service()
    service.cleanup()
    assert_true(service.excel_service.safe_close_excel.called,
                "safe_close_excel が呼ばれる")
    return True


def test_data_service_cleanup_on_exception():
    """DataService.cleanup: 例外が発生しても呼び出し元に伝播しない"""
    service = _make_service()
    service.excel_service.safe_close_excel.side_effect = Exception("close error")
    service.cleanup()  # 例外が漏れなければOK
    return True


def run_data_service_tests():
    """データサービステストを実行"""
    suite = TestSuite("データサービス統合テスト")

    suite.add_test(test_data_service_creation)
    suite.add_test(test_data_service_has_methods)
    suite.add_test(test_data_service_get_funeral_data_returns_dict)
    suite.add_test(test_data_service_get_construction_data_returns_list)
    suite.add_test(test_data_service_get_offering_data_returns_list)
    suite.add_test(test_data_service_get_incense_data_returns_list)
    suite.add_test(test_data_service_save_incense_data_returns_true)
    suite.add_test(test_data_service_save_funeral_data_valid)
    suite.add_test(test_data_service_save_funeral_data_invalid)
    suite.add_test(test_data_service_save_construction_data_valid)
    suite.add_test(test_data_service_save_offering_data_valid)
    suite.add_test(test_data_service_get_koden_data_exception_returns_empty)
    suite.add_test(test_data_service_get_koden_data_success)
    suite.add_test(test_data_service_save_koden_data_invalid)
    suite.add_test(test_data_service_save_koden_data_valid)
    suite.add_test(test_data_service_save_koden_data_excel_exception)
    suite.add_test(test_data_service_normalize_koden_data_trims_spaces)
    suite.add_test(test_data_service_normalize_koden_data_boolean_fields)
    suite.add_test(test_data_service_normalize_funeral_data_trims_spaces)
    suite.add_test(test_data_service_get_flower_data_all_success)
    suite.add_test(test_data_service_get_flower_data_exception_returns_empty)
    suite.add_test(test_data_service_save_flower_data_valid)
    suite.add_test(test_data_service_save_flower_data_invalid)
    suite.add_test(test_data_service_delete_flower_data_success)
    suite.add_test(test_data_service_delete_flower_data_exception)
    suite.add_test(test_data_service_get_condolence_data_all_success)
    suite.add_test(test_data_service_save_condolence_data_valid)
    suite.add_test(test_data_service_save_condolence_data_invalid)
    suite.add_test(test_data_service_delete_condolence_data_success)
    suite.add_test(test_data_service_load_settings_returns_dict)
    suite.add_test(test_data_service_save_settings_no_path)
    suite.add_test(test_data_service_save_settings_with_path)
    suite.add_test(test_data_service_cleanup_calls_excel_close)
    suite.add_test(test_data_service_cleanup_on_exception)

    return suite.run_tests()


if __name__ == "__main__":
    run_data_service_tests()
