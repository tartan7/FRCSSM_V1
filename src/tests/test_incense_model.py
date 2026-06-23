"""
焼香順モデルのテストケース
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_framework import TestSuite, assert_equal, assert_true, assert_false
from models.incense_model import IncenseModel


def _valid_model():
    """最低限有効なモデルを返すヘルパー"""
    m = IncenseModel()
    m.number = 1
    m.name = "田中太郎"
    return m


# --- 初期化 ---

def test_incense_model_creation():
    """IncenseModel: 初期値の確認"""
    m = IncenseModel()
    assert_equal(m.number, 0, "初期番号は0")
    assert_equal(m.name, "", "初期名前は空文字")
    assert_equal(m.relationship, "", "初期続柄は空文字")
    assert_equal(m.furigana, "", "初期フリガナは空文字")
    assert_equal(m.notes, "", "初期備考は空文字")
    assert_false(m.check, "初期チェックはFalse")
    assert_equal(m.id, None, "初期IDはNone")
    return True


# --- validate ---

def test_incense_model_validate_number_zero():
    """IncenseModel.validate: 番号0はエラー"""
    m = IncenseModel()
    m.number = 0
    errors = m.validate()
    assert_true(any("番号" in e for e in errors), "番号0はエラー")
    return True


def test_incense_model_validate_number_negative():
    """IncenseModel.validate: 負の番号はエラー"""
    m = IncenseModel()
    m.number = -1
    errors = m.validate()
    assert_true(any("番号" in e for e in errors), "負の番号はエラー")
    return True


def test_incense_model_validate_valid_data():
    """IncenseModel.validate: 有効データはエラーなし"""
    m = _valid_model()
    m.relationship = "長男"
    m.furigana = "タナカタロウ"
    assert_equal(len(m.validate()), 0, "有効データはエラーなし")
    return True


def test_incense_model_validate_name_too_long():
    """IncenseModel.validate: 51文字の名前はエラー"""
    m = _valid_model()
    m.name = "あ" * 51
    errors = m.validate()
    assert_true(any("名前" in e and "50文字" in e for e in errors), "51文字の名前はエラー")
    return True


def test_incense_model_validate_relationship_too_long():
    """IncenseModel.validate: 31文字の続柄はエラー"""
    m = _valid_model()
    m.relationship = "あ" * 31
    errors = m.validate()
    assert_true(any("続柄" in e and "30文字" in e for e in errors), "31文字の続柄はエラー")
    return True


def test_incense_model_validate_furigana_too_long():
    """IncenseModel.validate: 101文字のフリガナはエラー"""
    m = _valid_model()
    m.furigana = "ア" * 101
    errors = m.validate()
    assert_true(any("フリガナ" in e and "100文字" in e for e in errors), "101文字のフリガナはエラー")
    return True


def test_incense_model_validate_forbidden_chars_in_name():
    """IncenseModel.validate: 名前に禁止文字が含まれるとエラー"""
    m = _valid_model()
    for char in ['<', '>', '&', '"', "'"]:
        m.name = f"田中{char}太郎"
        errors = m.validate()
        assert_true(any("名前" in e and "使用できない文字" in e for e in errors),
                    f"名前の禁止文字 '{char}' はエラー")
    return True


def test_incense_model_validate_forbidden_chars_in_relationship():
    """IncenseModel.validate: 続柄に禁止文字が含まれるとエラー"""
    m = _valid_model()
    m.relationship = "長男/次男"
    errors = m.validate()
    assert_true(any("続柄" in e and "使用できない文字" in e for e in errors),
                "続柄の禁止文字はエラー")
    return True


# --- is_valid ---

def test_incense_model_is_valid():
    """IncenseModel.is_valid: 有効/無効の切り替え"""
    m = IncenseModel()
    assert_false(m.is_valid(), "番号0の空モデルは無効")
    m.number = 1
    assert_true(m.is_valid(), "番号設定後は有効")
    return True


# --- get_display_name ---

def test_incense_model_get_display_name_with_name():
    """IncenseModel.get_display_name: 名前あり（続柄なし）"""
    m = IncenseModel()
    m.number = 1
    m.name = "田中太郎"
    assert_equal(m.get_display_name(), "田中太郎", "名前のみ表示")
    return True


def test_incense_model_get_display_name_with_relationship():
    """IncenseModel.get_display_name: 名前あり・続柄あり"""
    m = IncenseModel()
    m.number = 1
    m.name = "田中太郎"
    m.relationship = "長男"
    assert_equal(m.get_display_name(), "田中太郎 (長男)", "名前と続柄が表示")
    return True


def test_incense_model_get_display_name_no_name():
    """IncenseModel.get_display_name: 名前なしはデフォルト文字列"""
    m = IncenseModel()
    m.number = 3
    assert_equal(m.get_display_name(), "焼香順 #3", "名前なし → 番号表示")
    return True


# --- get_summary ---

def test_incense_model_get_summary():
    """IncenseModel.get_summary: No.・名前・続柄を含む"""
    m = IncenseModel()
    m.number = 2
    m.name = "田中花子"
    m.relationship = "妻"
    result = m.get_summary()
    assert_true("No.2" in result, "No.が含まれる")
    assert_true("田中花子" in result, "名前が含まれる")
    assert_true("妻" in result, "続柄が含まれる")
    return True


def test_incense_model_get_summary_no_name():
    """IncenseModel.get_summary: 名前なしはNo.のみ"""
    m = IncenseModel()
    m.number = 5
    result = m.get_summary()
    assert_equal(result, "No.5", "名前なしはNo.のみ")
    return True


# --- get_full_name ---

def test_incense_model_get_full_name_with_relationship():
    """IncenseModel.get_full_name: 名前 + 続柄"""
    m = _valid_model()
    m.relationship = "長女"
    assert_equal(m.get_full_name(), "田中太郎 (長女)", "名前と続柄のフルネーム")
    return True


def test_incense_model_get_full_name_without_relationship():
    """IncenseModel.get_full_name: 続柄なしは名前のみ"""
    m = _valid_model()
    assert_equal(m.get_full_name(), "田中太郎", "続柄なしは名前のみ")
    return True


# --- get_relationship_display ---

def test_incense_model_get_relationship_display_set():
    """IncenseModel.get_relationship_display: 続柄ありはその値"""
    m = _valid_model()
    m.relationship = "次男"
    assert_equal(m.get_relationship_display(), "次男", "続柄がそのまま返る")
    return True


def test_incense_model_get_relationship_display_empty():
    """IncenseModel.get_relationship_display: 続柄なしは '未設定'"""
    m = _valid_model()
    assert_equal(m.get_relationship_display(), "未設定", "空の続柄は未設定")
    return True


# --- has_furigana ---

def test_incense_model_has_furigana_true():
    """IncenseModel.has_furigana: フリガナありはTrue"""
    m = _valid_model()
    m.furigana = "タナカタロウ"
    assert_true(m.has_furigana(), "フリガナありはTrue")
    return True


def test_incense_model_has_furigana_false():
    """IncenseModel.has_furigana: フリガナなしはFalse"""
    m = _valid_model()
    assert_false(m.has_furigana(), "フリガナなしはFalse")
    return True


def test_incense_model_has_furigana_whitespace():
    """IncenseModel.has_furigana: 空白のみはFalse"""
    m = _valid_model()
    m.furigana = "   "
    assert_false(m.has_furigana(), "空白のみのフリガナはFalse")
    return True


# --- is_empty ---

def test_incense_model_is_empty_true():
    """IncenseModel.is_empty: 名前・続柄が空はTrue"""
    m = IncenseModel()
    m.number = 1
    assert_true(m.is_empty(), "名前・続柄が空はTrue")
    return True


def test_incense_model_is_empty_false():
    """IncenseModel.is_empty: 名前があればFalse"""
    m = _valid_model()
    assert_false(m.is_empty(), "名前があればFalse")
    return True


# --- clear ---

def test_incense_model_clear():
    """IncenseModel.clear: フィールドがリセットされる"""
    m = _valid_model()
    m.relationship = "長男"
    m.furigana = "タナカタロウ"
    m.notes = "備考テスト"
    m.check = True
    m.clear()
    assert_equal(m.name, "", "名前がクリア")
    assert_equal(m.relationship, "", "続柄がクリア")
    assert_equal(m.furigana, "", "フリガナがクリア")
    assert_equal(m.notes, "", "備考がクリア")
    assert_false(m.check, "チェックがFalseにリセット")
    return True


# --- to_excel_row / from_excel_row ---

def test_incense_model_to_excel_row():
    """IncenseModel.to_excel_row: 正しい列順で返る"""
    m = _valid_model()
    m.relationship = "長男"
    m.furigana = "タナカタロウ"
    m.check = True
    row = m.to_excel_row()
    assert_equal(row[0], 1, "0列目: 番号")
    assert_equal(row[1], "田中太郎", "1列目: 名前")
    assert_equal(row[2], "長男", "2列目: 続柄")
    assert_equal(row[3], "タナカタロウ", "3列目: フリガナ")
    assert_equal(row[4], "○", "4列目: チェック=○")
    return True


def test_incense_model_to_excel_row_no_check():
    """IncenseModel.to_excel_row: チェックなしは空文字"""
    m = _valid_model()
    row = m.to_excel_row()
    assert_equal(row[4], "", "チェックなしは空文字")
    return True


def test_incense_model_from_excel_row():
    """IncenseModel.from_excel_row: 行データから正しく設定される"""
    m = IncenseModel()
    m.from_excel_row([3, "鈴木一郎", "父", "スズキイチロウ", "○"])
    assert_equal(m.number, 3, "番号が設定される")
    assert_equal(m.name, "鈴木一郎", "名前が設定される")
    assert_equal(m.relationship, "父", "続柄が設定される")
    assert_equal(m.furigana, "スズキイチロウ", "フリガナが設定される")
    assert_true(m.check, "チェックが設定される")
    return True


def test_incense_model_from_excel_row_no_check():
    """IncenseModel.from_excel_row: チェックなし行"""
    m = IncenseModel()
    m.from_excel_row([1, "田中太郎", "", "", ""])
    assert_false(m.check, "空文字はFalse")
    return True


# --- to_dict / from_dict (BaseModel継承) ---

def test_incense_model_to_dict():
    """IncenseModel.to_dict: 辞書変換"""
    m = _valid_model()
    m.relationship = "長男"
    data = m.to_dict()
    assert_equal(data["name"], "田中太郎", "名前が含まれる")
    assert_equal(data["relationship"], "長男", "続柄が含まれる")
    assert_true("created_at" in data, "created_atが含まれる")
    return True


def test_incense_model_from_dict():
    """IncenseModel.from_dict: 辞書から復元"""
    m = IncenseModel()
    m.from_dict({"number": 2, "name": "佐藤次郎", "relationship": "次男"})
    assert_equal(m.number, 2, "番号が設定される")
    assert_equal(m.name, "佐藤次郎", "名前が設定される")
    assert_equal(m.relationship, "次男", "続柄が設定される")
    return True


def test_incense_model_to_json_from_json():
    """IncenseModel.to_json/from_json: JSON往復テスト"""
    m = _valid_model()
    m.relationship = "長男"

    json_str = m.to_json()

    m2 = IncenseModel()
    m2.from_json(json_str)
    assert_equal(m2.name, "田中太郎", "JSON往復で名前が保持")
    assert_equal(m2.relationship, "長男", "JSON往復で続柄が保持")
    return True


def run_incense_model_tests():
    """焼香順モデルテストを実行"""
    suite = TestSuite("焼香順モデルテスト")

    suite.add_test(test_incense_model_creation)
    suite.add_test(test_incense_model_validate_number_zero)
    suite.add_test(test_incense_model_validate_number_negative)
    suite.add_test(test_incense_model_validate_valid_data)
    suite.add_test(test_incense_model_validate_name_too_long)
    suite.add_test(test_incense_model_validate_relationship_too_long)
    suite.add_test(test_incense_model_validate_furigana_too_long)
    suite.add_test(test_incense_model_validate_forbidden_chars_in_name)
    suite.add_test(test_incense_model_validate_forbidden_chars_in_relationship)
    suite.add_test(test_incense_model_is_valid)
    suite.add_test(test_incense_model_get_display_name_with_name)
    suite.add_test(test_incense_model_get_display_name_with_relationship)
    suite.add_test(test_incense_model_get_display_name_no_name)
    suite.add_test(test_incense_model_get_summary)
    suite.add_test(test_incense_model_get_summary_no_name)
    suite.add_test(test_incense_model_get_full_name_with_relationship)
    suite.add_test(test_incense_model_get_full_name_without_relationship)
    suite.add_test(test_incense_model_get_relationship_display_set)
    suite.add_test(test_incense_model_get_relationship_display_empty)
    suite.add_test(test_incense_model_has_furigana_true)
    suite.add_test(test_incense_model_has_furigana_false)
    suite.add_test(test_incense_model_has_furigana_whitespace)
    suite.add_test(test_incense_model_is_empty_true)
    suite.add_test(test_incense_model_is_empty_false)
    suite.add_test(test_incense_model_clear)
    suite.add_test(test_incense_model_to_excel_row)
    suite.add_test(test_incense_model_to_excel_row_no_check)
    suite.add_test(test_incense_model_from_excel_row)
    suite.add_test(test_incense_model_from_excel_row_no_check)
    suite.add_test(test_incense_model_to_dict)
    suite.add_test(test_incense_model_from_dict)
    suite.add_test(test_incense_model_to_json_from_json)

    return suite.run_tests()


if __name__ == "__main__":
    run_incense_model_tests()
