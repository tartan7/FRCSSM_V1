"""
葬儀モデルのテストケース
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_framework import TestSuite, assert_equal, assert_true, assert_false
from models.funeral_model import FuneralModel


def _valid_model():
    """最低限有効なモデルを返すヘルパー"""
    m = FuneralModel()
    m.deceased_name = "山田太郎"
    m.family_name = "山田花子"
    return m


# --- 初期化 ---

def test_funeral_model_creation():
    """FuneralModel: 初期値の確認"""
    m = FuneralModel()
    assert_equal(m.deceased_name, "", "初期故人名は空文字")
    assert_equal(m.family_name, "", "初期遺族名は空文字")
    assert_equal(m.age, 0, "初期年齢は0")
    assert_equal(m.temple_phone, "", "初期寺院電話は空文字")
    assert_equal(m.id, None, "初期IDはNone")
    return True


# --- validate ---

def test_funeral_model_validate_required():
    """FuneralModel.validate: 故人名・遺族名は必須"""
    m = FuneralModel()
    errors = m.validate()
    assert_true(any("故人名" in e for e in errors), "故人名エラーが含まれる")
    assert_true(any("遺族名" in e for e in errors), "遺族名エラーが含まれる")
    return True


def test_funeral_model_validate_valid_data():
    """FuneralModel.validate: 有効データはエラーなし"""
    m = _valid_model()
    m.age = 80
    assert_equal(len(m.validate()), 0, "有効データはエラーなし")
    return True


def test_funeral_model_validate_name_too_long():
    """FuneralModel.validate: 51文字の故人名はエラー"""
    m = _valid_model()
    m.deceased_name = "あ" * 51
    errors = m.validate()
    assert_true(any("故人名" in e and "50文字" in e for e in errors), "51文字の故人名はエラー")
    return True


def test_funeral_model_validate_age_negative():
    """FuneralModel.validate: マイナス年齢はエラー"""
    m = _valid_model()
    m.age = -1
    assert_true(any("年齢" in e for e in m.validate()), "マイナス年齢はエラー")
    return True


def test_funeral_model_validate_age_over_150():
    """FuneralModel.validate: 151歳以上はエラー"""
    m = _valid_model()
    m.age = 151
    assert_true(any("年齢" in e for e in m.validate()), "151歳はエラー")
    return True


def test_funeral_model_validate_age_boundary():
    """FuneralModel.validate: 0歳・150歳は有効"""
    m = _valid_model()
    m.age = 0
    assert_equal(len(m.validate()), 0, "0歳は有効")
    m.age = 150
    assert_equal(len(m.validate()), 0, "150歳は有効")
    return True


def test_funeral_model_validate_date_western():
    """FuneralModel.validate: 西暦形式の日付は有効"""
    m = _valid_model()
    m.birth_date = "1944/04/15"
    m.death_date = "2024/04/15"
    errors = m.validate()
    assert_false(any("生年月日" in e for e in errors), "西暦形式の生年月日は有効")
    assert_false(any("死亡日時" in e for e in errors), "西暦形式の死亡日時は有効")
    return True


def test_funeral_model_validate_date_wareki():
    """FuneralModel.validate: 和暦形式の日付は有効"""
    m = _valid_model()
    m.birth_date = "昭和19年4月15日"
    m.death_date = "令和6年4月15日"
    errors = m.validate()
    assert_false(any("生年月日" in e for e in errors), "和暦形式の生年月日は有効")
    assert_false(any("死亡日時" in e for e in errors), "和暦形式の死亡日時は有効")
    return True


def test_funeral_model_validate_date_invalid():
    """FuneralModel.validate: スラッシュなし西暦はエラー"""
    m = _valid_model()
    m.birth_date = "20240415"
    assert_true(any("生年月日" in e for e in m.validate()), "不正な日付形式はエラー")
    return True


def test_funeral_model_validate_phone_valid():
    """FuneralModel.validate: 数字・ハイフン・括弧の電話番号は有効"""
    m = _valid_model()
    m.temple_phone = "03-1234-5678"
    m.venue_phone = "0120(000)000"
    errors = m.validate()
    assert_false(any("寺院電話" in e for e in errors), "ハイフン付き電話番号は有効")
    assert_false(any("会場電話" in e for e in errors), "括弧付き電話番号は有効")
    return True


def test_funeral_model_validate_phone_invalid():
    """FuneralModel.validate: 文字入り電話番号はエラー"""
    m = _valid_model()
    m.temple_phone = "03-abc-5678"
    assert_true(any("寺院電話" in e for e in m.validate()), "文字入り電話番号はエラー")
    return True


# --- get_display_name ---

def test_funeral_model_get_display_name():
    """FuneralModel.get_display_name: 故人名あり"""
    m = FuneralModel()
    m.deceased_name = "山田太郎"
    assert_equal(m.get_display_name(), "山田太郎様の葬儀", "故人名あり")
    return True


def test_funeral_model_get_display_name_empty():
    """FuneralModel.get_display_name: 故人名なしはデフォルト文字列"""
    m = FuneralModel()
    assert_equal(m.get_display_name(), "葬儀情報", "故人名なし → デフォルト")
    return True


# --- get_summary ---

def test_funeral_model_get_summary():
    """FuneralModel.get_summary: 故人名・年齢・遺族名を含む"""
    m = FuneralModel()
    m.deceased_name = "山田太郎"
    m.age = 80
    m.family_name = "山田花子"
    result = m.get_summary()
    assert_true("山田太郎" in result, "故人名が含まれる")
    assert_true("80歳" in result, "年齢が含まれる")
    assert_true("山田花子" in result, "遺族名が含まれる")
    return True


# --- calculate_age ---

def test_funeral_model_calculate_age_western():
    """FuneralModel.calculate_age: 西暦日付で年齢計算"""
    m = FuneralModel()
    m.birth_date = "1944/04/15"
    m.death_date = "2024/04/15"
    assert_equal(m.calculate_age(), 80, "1944→2024 = 80歳")
    return True


def test_funeral_model_calculate_age_wareki():
    """FuneralModel.calculate_age: 和暦日付で年齢計算"""
    m = FuneralModel()
    m.birth_date = "昭和19年4月15日"
    m.death_date = "令和6年4月15日"
    assert_equal(m.calculate_age(), 80, "昭和19年(1944)→令和6年(2024) = 80歳")
    return True


def test_funeral_model_calculate_age_no_dates():
    """FuneralModel.calculate_age: 日付なしは0"""
    m = FuneralModel()
    assert_equal(m.calculate_age(), 0, "日付なしは0")
    return True


# --- is_valid ---

def test_funeral_model_is_valid():
    """FuneralModel.is_valid: 有効/無効の切り替え"""
    m = FuneralModel()
    assert_false(m.is_valid(), "空のモデルは無効")
    m.deceased_name = "山田太郎"
    m.family_name = "山田花子"
    assert_true(m.is_valid(), "必須項目設定後は有効")
    return True


# --- get_funeral_schedule ---

def test_funeral_model_get_schedule_empty():
    """FuneralModel.get_funeral_schedule: 日付なしは空リスト"""
    m = FuneralModel()
    assert_equal(m.get_funeral_schedule(), [], "日付なしは空リスト")
    return True


def test_funeral_model_get_schedule_full():
    """FuneralModel.get_funeral_schedule: 通夜・葬儀・出棺の順"""
    m = FuneralModel()
    m.overnight_date = "令和6年4月15日"
    m.funeral_date = "令和6年4月16日"
    m.departure_date = "令和6年4月16日"
    m.venue_name = "〇〇斎場"
    m.crematory_name = "〇〇火葬場"
    schedule = m.get_funeral_schedule()
    assert_equal(len(schedule), 3, "3イベント")
    assert_equal(schedule[0]["event"], "通夜", "1番目は通夜")
    assert_equal(schedule[1]["event"], "葬儀", "2番目は葬儀")
    assert_equal(schedule[2]["event"], "出棺", "3番目は出棺")
    return True


# --- to_dict / from_dict / to_json / from_json (BaseModel継承) ---

def test_funeral_model_to_dict():
    """FuneralModel.to_dict: 辞書変換"""
    m = FuneralModel()
    m.deceased_name = "山田太郎"
    m.age = 80
    data = m.to_dict()
    assert_equal(data["deceased_name"], "山田太郎", "故人名が正しく変換")
    assert_equal(data["age"], 80, "年齢が正しく変換")
    assert_true("created_at" in data, "created_atが含まれる")
    return True


def test_funeral_model_from_dict():
    """FuneralModel.from_dict: 辞書からの復元"""
    m = FuneralModel()
    m.from_dict({"deceased_name": "山田太郎", "family_name": "山田花子", "age": 80})
    assert_equal(m.deceased_name, "山田太郎", "故人名が設定される")
    assert_equal(m.family_name, "山田花子", "遺族名が設定される")
    assert_equal(m.age, 80, "年齢が設定される")
    return True


def test_funeral_model_to_json_from_json():
    """FuneralModel.to_json/from_json: JSON往復テスト"""
    m = FuneralModel()
    m.deceased_name = "山田太郎"
    m.age = 80

    json_str = m.to_json()

    m2 = FuneralModel()
    m2.from_json(json_str)
    assert_equal(m2.deceased_name, "山田太郎", "JSON往復で故人名が保持")
    assert_equal(m2.age, 80, "JSON往復で年齢が保持")
    return True


def run_funeral_model_tests():
    """葬儀モデルテストを実行"""
    suite = TestSuite("葬儀モデルテスト")

    suite.add_test(test_funeral_model_creation)
    suite.add_test(test_funeral_model_validate_required)
    suite.add_test(test_funeral_model_validate_valid_data)
    suite.add_test(test_funeral_model_validate_name_too_long)
    suite.add_test(test_funeral_model_validate_age_negative)
    suite.add_test(test_funeral_model_validate_age_over_150)
    suite.add_test(test_funeral_model_validate_age_boundary)
    suite.add_test(test_funeral_model_validate_date_western)
    suite.add_test(test_funeral_model_validate_date_wareki)
    suite.add_test(test_funeral_model_validate_date_invalid)
    suite.add_test(test_funeral_model_validate_phone_valid)
    suite.add_test(test_funeral_model_validate_phone_invalid)
    suite.add_test(test_funeral_model_get_display_name)
    suite.add_test(test_funeral_model_get_display_name_empty)
    suite.add_test(test_funeral_model_get_summary)
    suite.add_test(test_funeral_model_calculate_age_western)
    suite.add_test(test_funeral_model_calculate_age_wareki)
    suite.add_test(test_funeral_model_calculate_age_no_dates)
    suite.add_test(test_funeral_model_is_valid)
    suite.add_test(test_funeral_model_get_schedule_empty)
    suite.add_test(test_funeral_model_get_schedule_full)
    suite.add_test(test_funeral_model_to_dict)
    suite.add_test(test_funeral_model_from_dict)
    suite.add_test(test_funeral_model_to_json_from_json)

    return suite.run_tests()


if __name__ == "__main__":
    run_funeral_model_tests()
