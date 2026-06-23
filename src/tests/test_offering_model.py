"""
供物モデルのテストケース
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_framework import TestSuite, assert_equal, assert_true, assert_false
from models.offering_model import OfferingModel


def _valid_model():
    """最低限有効なモデルを返すヘルパー"""
    m = OfferingModel()
    m.number = 1
    m.offering_type = "果物"
    m.quantity = 1
    return m


# --- 初期化 ---

def test_offering_model_creation():
    """OfferingModel: 初期値の確認"""
    m = OfferingModel()
    assert_equal(m.number, 0, "初期番号は0")
    assert_equal(m.offering_type, "", "初期供物種類は空文字")
    assert_equal(m.quantity, 0, "初期数量は0")
    assert_equal(m.unit, "", "初期単位は空文字")
    assert_equal(m.notes, "", "初期備考は空文字")
    assert_false(m.check, "初期チェックはFalse")
    assert_equal(m.id, None, "初期IDはNone")
    return True


# --- validate ---

def test_offering_model_validate_number_zero():
    """OfferingModel.validate: 番号0はエラー"""
    m = OfferingModel()
    m.number = 0
    errors = m.validate()
    assert_true(any("番号" in e for e in errors), "番号0はエラー")
    return True


def test_offering_model_validate_number_negative():
    """OfferingModel.validate: 負の番号はエラー"""
    m = OfferingModel()
    m.number = -1
    errors = m.validate()
    assert_true(any("番号" in e for e in errors), "負の番号はエラー")
    return True


def test_offering_model_validate_valid_data():
    """OfferingModel.validate: 有効データはエラーなし"""
    m = _valid_model()
    m.unit = "箱"
    assert_equal(len(m.validate()), 0, "有効データはエラーなし")
    return True


def test_offering_model_validate_offering_type_too_long():
    """OfferingModel.validate: 51文字の供物種類はエラー"""
    m = _valid_model()
    m.offering_type = "あ" * 51
    errors = m.validate()
    assert_true(any("供物の種類" in e and "50文字" in e for e in errors),
                "51文字の供物種類はエラー")
    return True


def test_offering_model_validate_quantity_negative():
    """OfferingModel.validate: 負の数量はエラー"""
    m = _valid_model()
    m.quantity = -1
    errors = m.validate()
    assert_true(any("数量" in e and "0以上" in e for e in errors), "負の数量はエラー")
    return True


def test_offering_model_validate_quantity_over_limit():
    """OfferingModel.validate: 1001個はエラー"""
    m = _valid_model()
    m.quantity = 1001
    errors = m.validate()
    assert_true(any("数量" in e and "1,000個" in e for e in errors), "1001個はエラー")
    return True


def test_offering_model_validate_quantity_boundary():
    """OfferingModel.validate: 0個・1000個は有効"""
    m = _valid_model()
    m.quantity = 0
    assert_equal(len(m.validate()), 0, "0個は有効")
    m.quantity = 1000
    assert_equal(len(m.validate()), 0, "1000個は有効")
    return True


def test_offering_model_validate_unit_too_long():
    """OfferingModel.validate: 21文字の単位はエラー"""
    m = _valid_model()
    m.unit = "あ" * 21
    errors = m.validate()
    assert_true(any("単位" in e and "20文字" in e for e in errors), "21文字の単位はエラー")
    return True


def test_offering_model_validate_forbidden_chars_in_type():
    """OfferingModel.validate: 供物種類に禁止文字が含まれるとエラー"""
    m = _valid_model()
    for char in ['<', '>', '&']:
        m.offering_type = f"果物{char}"
        errors = m.validate()
        assert_true(any("供物の種類" in e and "使用できない文字" in e for e in errors),
                    f"供物種類の禁止文字 '{char}' はエラー")
    return True


def test_offering_model_validate_forbidden_chars_in_unit():
    """OfferingModel.validate: 単位に禁止文字が含まれるとエラー"""
    m = _valid_model()
    m.unit = "箱/個"
    errors = m.validate()
    assert_true(any("単位" in e and "使用できない文字" in e for e in errors),
                "単位の禁止文字はエラー")
    return True


# --- is_valid ---

def test_offering_model_is_valid():
    """OfferingModel.is_valid: 有効/無効の切り替え"""
    m = OfferingModel()
    assert_false(m.is_valid(), "番号0の空モデルは無効")
    m.number = 1
    assert_true(m.is_valid(), "番号設定後は有効")
    return True


# --- get_display_name ---

def test_offering_model_get_display_name_with_unit():
    """OfferingModel.get_display_name: 種類あり・単位あり"""
    m = _valid_model()
    m.unit = "箱"
    assert_equal(m.get_display_name(), "果物 (1箱)", "種類と数量単位が表示")
    return True


def test_offering_model_get_display_name_without_unit():
    """OfferingModel.get_display_name: 種類あり・単位なし"""
    m = _valid_model()
    assert_equal(m.get_display_name(), "果物 (1)", "単位なしは数量のみ")
    return True


def test_offering_model_get_display_name_no_type():
    """OfferingModel.get_display_name: 種類なしはデフォルト文字列"""
    m = OfferingModel()
    m.number = 2
    assert_equal(m.get_display_name(), "供物 #2", "種類なし → 番号表示")
    return True


# --- get_summary ---

def test_offering_model_get_summary_full():
    """OfferingModel.get_summary: No.・種類・数量単位を含む"""
    m = _valid_model()
    m.quantity = 3
    m.unit = "個"
    result = m.get_summary()
    assert_true("No.1" in result, "No.が含まれる")
    assert_true("果物" in result, "種類が含まれる")
    assert_true("3個" in result, "数量単位が含まれる")
    return True


def test_offering_model_get_summary_no_type():
    """OfferingModel.get_summary: 種類なしはNo.のみ"""
    m = OfferingModel()
    m.number = 4
    result = m.get_summary()
    assert_equal(result, "No.4", "種類なしはNo.のみ")
    return True


def test_offering_model_get_summary_zero_quantity():
    """OfferingModel.get_summary: 数量0は数量部分を含まない"""
    m = OfferingModel()
    m.number = 1
    m.offering_type = "線香"
    m.quantity = 0
    result = m.get_summary()
    assert_true("線香" in result, "種類が含まれる")
    assert_false("(0" in result, "数量0は数量部分を含まない")
    return True


# --- get_quantity_display ---

def test_offering_model_get_quantity_display_with_unit():
    """OfferingModel.get_quantity_display: 単位ありは数量+単位"""
    m = _valid_model()
    m.quantity = 5
    m.unit = "本"
    assert_equal(m.get_quantity_display(), "5本", "数量+単位")
    return True


def test_offering_model_get_quantity_display_without_unit():
    """OfferingModel.get_quantity_display: 単位なしは数量のみ"""
    m = _valid_model()
    m.quantity = 3
    assert_equal(m.get_quantity_display(), "3", "単位なしは数量のみ")
    return True


# --- is_valid_quantity ---

def test_offering_model_is_valid_quantity_true():
    """OfferingModel.is_valid_quantity: 1〜1000はTrue"""
    m = _valid_model()
    m.quantity = 1
    assert_true(m.is_valid_quantity(), "1はTrue")
    m.quantity = 1000
    assert_true(m.is_valid_quantity(), "1000はTrue")
    return True


def test_offering_model_is_valid_quantity_false():
    """OfferingModel.is_valid_quantity: 0・1001はFalse"""
    m = _valid_model()
    m.quantity = 0
    assert_false(m.is_valid_quantity(), "0はFalse")
    m.quantity = 1001
    assert_false(m.is_valid_quantity(), "1001はFalse")
    return True


# --- is_empty ---

def test_offering_model_is_empty_true():
    """OfferingModel.is_empty: 種類・数量・単位が空はTrue"""
    m = OfferingModel()
    m.number = 1
    assert_true(m.is_empty(), "全フィールド空はTrue")
    return True


def test_offering_model_is_empty_false_type():
    """OfferingModel.is_empty: 種類があればFalse"""
    m = _valid_model()
    m.quantity = 0
    m.unit = ""
    assert_false(m.is_empty(), "種類があればFalse")
    return True


def test_offering_model_is_empty_false_quantity():
    """OfferingModel.is_empty: 数量があればFalse"""
    m = OfferingModel()
    m.number = 1
    m.quantity = 1
    assert_false(m.is_empty(), "数量があればFalse")
    return True


# --- clear ---

def test_offering_model_clear():
    """OfferingModel.clear: フィールドがリセットされる"""
    m = _valid_model()
    m.unit = "箱"
    m.notes = "備考テスト"
    m.check = True
    m.clear()
    assert_equal(m.offering_type, "", "供物種類がクリア")
    assert_equal(m.quantity, 0, "数量が0にリセット")
    assert_equal(m.unit, "", "単位がクリア")
    assert_equal(m.notes, "", "備考がクリア")
    assert_false(m.check, "チェックがFalseにリセット")
    return True


# --- to_excel_row / from_excel_row ---

def test_offering_model_to_excel_row():
    """OfferingModel.to_excel_row: 正しい列順で返る"""
    m = _valid_model()
    m.unit = "箱"
    m.check = True
    row = m.to_excel_row()
    assert_equal(row[0], 1, "0列目: 番号")
    assert_equal(row[1], "果物", "1列目: 供物種類")
    assert_equal(row[2], 1, "2列目: 数量")
    assert_equal(row[3], "箱", "3列目: 単位")
    assert_equal(row[4], "○", "4列目: チェック=○")
    return True


def test_offering_model_to_excel_row_no_check():
    """OfferingModel.to_excel_row: チェックなしは空文字"""
    m = _valid_model()
    row = m.to_excel_row()
    assert_equal(row[4], "", "チェックなしは空文字")
    return True


def test_offering_model_from_excel_row():
    """OfferingModel.from_excel_row: 行データから正しく設定される"""
    m = OfferingModel()
    m.from_excel_row([2, "線香", 10, "本", "○"])
    assert_equal(m.number, 2, "番号が設定される")
    assert_equal(m.offering_type, "線香", "供物種類が設定される")
    assert_equal(m.quantity, 10, "数量が設定される")
    assert_equal(m.unit, "本", "単位が設定される")
    assert_true(m.check, "チェックが設定される")
    return True


def test_offering_model_from_excel_row_no_check():
    """OfferingModel.from_excel_row: チェックなし行"""
    m = OfferingModel()
    m.from_excel_row([1, "果物", 1, "", ""])
    assert_false(m.check, "空文字はFalse")
    return True


# --- to_dict / from_dict (BaseModel継承) ---

def test_offering_model_to_dict():
    """OfferingModel.to_dict: 辞書変換"""
    m = _valid_model()
    m.unit = "個"
    data = m.to_dict()
    assert_equal(data["offering_type"], "果物", "供物種類が含まれる")
    assert_equal(data["quantity"], 1, "数量が含まれる")
    assert_equal(data["unit"], "個", "単位が含まれる")
    assert_true("created_at" in data, "created_atが含まれる")
    return True


def test_offering_model_from_dict():
    """OfferingModel.from_dict: 辞書から復元"""
    m = OfferingModel()
    m.from_dict({"number": 3, "offering_type": "菓子", "quantity": 2, "unit": "箱"})
    assert_equal(m.number, 3, "番号が設定される")
    assert_equal(m.offering_type, "菓子", "供物種類が設定される")
    assert_equal(m.quantity, 2, "数量が設定される")
    assert_equal(m.unit, "箱", "単位が設定される")
    return True


def test_offering_model_to_json_from_json():
    """OfferingModel.to_json/from_json: JSON往復テスト"""
    m = _valid_model()
    m.unit = "箱"

    json_str = m.to_json()

    m2 = OfferingModel()
    m2.from_json(json_str)
    assert_equal(m2.offering_type, "果物", "JSON往復で供物種類が保持")
    assert_equal(m2.unit, "箱", "JSON往復で単位が保持")
    return True


def run_offering_model_tests():
    """供物モデルテストを実行"""
    suite = TestSuite("供物モデルテスト")

    suite.add_test(test_offering_model_creation)
    suite.add_test(test_offering_model_validate_number_zero)
    suite.add_test(test_offering_model_validate_number_negative)
    suite.add_test(test_offering_model_validate_valid_data)
    suite.add_test(test_offering_model_validate_offering_type_too_long)
    suite.add_test(test_offering_model_validate_quantity_negative)
    suite.add_test(test_offering_model_validate_quantity_over_limit)
    suite.add_test(test_offering_model_validate_quantity_boundary)
    suite.add_test(test_offering_model_validate_unit_too_long)
    suite.add_test(test_offering_model_validate_forbidden_chars_in_type)
    suite.add_test(test_offering_model_validate_forbidden_chars_in_unit)
    suite.add_test(test_offering_model_is_valid)
    suite.add_test(test_offering_model_get_display_name_with_unit)
    suite.add_test(test_offering_model_get_display_name_without_unit)
    suite.add_test(test_offering_model_get_display_name_no_type)
    suite.add_test(test_offering_model_get_summary_full)
    suite.add_test(test_offering_model_get_summary_no_type)
    suite.add_test(test_offering_model_get_summary_zero_quantity)
    suite.add_test(test_offering_model_get_quantity_display_with_unit)
    suite.add_test(test_offering_model_get_quantity_display_without_unit)
    suite.add_test(test_offering_model_is_valid_quantity_true)
    suite.add_test(test_offering_model_is_valid_quantity_false)
    suite.add_test(test_offering_model_is_empty_true)
    suite.add_test(test_offering_model_is_empty_false_type)
    suite.add_test(test_offering_model_is_empty_false_quantity)
    suite.add_test(test_offering_model_clear)
    suite.add_test(test_offering_model_to_excel_row)
    suite.add_test(test_offering_model_to_excel_row_no_check)
    suite.add_test(test_offering_model_from_excel_row)
    suite.add_test(test_offering_model_from_excel_row_no_check)
    suite.add_test(test_offering_model_to_dict)
    suite.add_test(test_offering_model_from_dict)
    suite.add_test(test_offering_model_to_json_from_json)

    return suite.run_tests()


if __name__ == "__main__":
    run_offering_model_tests()
