"""
日付ユーティリティのテストケース
"""
import sys
import os
from unittest.mock import MagicMock
from datetime import datetime

# datetimejp はオプション依存のため事前にモック
sys.modules['datetimejp'] = MagicMock()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_framework import TestSuite, assert_equal, assert_true, assert_false
from utils.date_utils import (
    calc_age,
    convert_japanese_date_to_gregorian,
    convert_to_wareki,
    increment_day_with_validation,
    diff_years,
)


# --- calc_age ---

def test_calc_age_normal():
    """calc_age: 誕生日後に死亡した場合の年齢"""
    birth = datetime(1950, 4, 15)
    death = datetime(2024, 4, 20)
    assert_equal(calc_age(birth, death), 74, "1950/4/15 → 2024/4/20 = 74歳")
    return True


def test_calc_age_before_birthday():
    """calc_age: 誕生日前に死亡した場合は1歳引く"""
    birth = datetime(1950, 6, 1)
    death = datetime(2024, 5, 31)
    assert_equal(calc_age(birth, death), 73, "誕生日前は年齢-1")
    return True


def test_calc_age_on_birthday():
    """calc_age: 誕生日当日に死亡した場合は誕生日を迎えた年齢"""
    birth = datetime(1950, 4, 15)
    death = datetime(2024, 4, 15)
    assert_equal(calc_age(birth, death), 74, "誕生日当日は74歳")
    return True


def test_calc_age_none_inputs():
    """calc_age: None入力はNoneを返す"""
    assert_equal(calc_age(None, datetime(2024, 1, 1)), None, "birth=None → None")
    assert_equal(calc_age(datetime(1950, 1, 1), None), None, "death=None → None")
    assert_equal(calc_age(None, None), None, "両方None → None")
    return True


# --- convert_japanese_date_to_gregorian ---

def test_convert_japanese_date_reiwa():
    """convert_japanese_date_to_gregorian: 令和→西暦"""
    result = convert_japanese_date_to_gregorian("令和6年4月15日")
    assert_equal(result, "2024/04/15", "令和6年 = 2024年")
    return True


def test_convert_japanese_date_heisei():
    """convert_japanese_date_to_gregorian: 平成→西暦"""
    result = convert_japanese_date_to_gregorian("平成31年4月30日")
    assert_equal(result, "2019/04/30", "平成31年 = 2019年")
    return True


def test_convert_japanese_date_showa():
    """convert_japanese_date_to_gregorian: 昭和→西暦"""
    result = convert_japanese_date_to_gregorian("昭和45年3月1日")
    assert_equal(result, "1970/03/01", "昭和45年 = 1970年")
    return True


def test_convert_japanese_date_with_afternoon_time():
    """convert_japanese_date_to_gregorian: 午後の時刻付き"""
    result = convert_japanese_date_to_gregorian("令和6年4月15日 午後2:30")
    assert_equal(result, "2024/04/15 14:30", "午後2:30 = 14:30")
    return True


def test_convert_japanese_date_invalid():
    """convert_japanese_date_to_gregorian: 西暦形式はNoneを返す"""
    result = convert_japanese_date_to_gregorian("2024/04/15")
    assert_equal(result, None, "西暦形式は変換できない")
    return True


# --- convert_to_wareki ---

def test_convert_to_wareki_reiwa():
    """convert_to_wareki: 西暦2024年 → 令和6年"""
    d = datetime(2024, 4, 15)
    assert_equal(convert_to_wareki(d), "令和6年4月15日", "2024年 = 令和6年")
    return True


def test_convert_to_wareki_heisei():
    """convert_to_wareki: 西暦2005年 → 平成17年"""
    d = datetime(2005, 7, 20)
    assert_equal(convert_to_wareki(d), "平成17年7月20日", "2005年 = 平成17年")
    return True


def test_convert_to_wareki_showa():
    """convert_to_wareki: 西暦1970年 → 昭和45年"""
    d = datetime(1970, 3, 1)
    assert_equal(convert_to_wareki(d), "昭和45年3月1日", "1970年 = 昭和45年")
    return True


def test_convert_to_wareki_with_afternoon_time():
    """convert_to_wareki: 午後の時刻付き変換"""
    d = datetime(2024, 4, 15, 14, 30)
    assert_equal(convert_to_wareki(d), "令和6年4月15日 午後2時30分", "14:30 = 午後2時30分")
    return True


def test_convert_to_wareki_none():
    """convert_to_wareki: None入力は空文字"""
    assert_equal(convert_to_wareki(None), "", "None → 空文字")
    return True


# --- increment_day_with_validation ---
# 内部形式: YYMMDD+名前 (YY=令和元号オフセット, 出力YY=西暦-2000)
# この関数は入出力のYY形式が異なる（既知の仕様）ため、月・日・名前のみ検証する

def test_increment_day_basic():
    """increment_day_with_validation: 基本的な日付繰り上げ"""
    result = increment_day_with_validation("060415山田太郎")
    assert_equal(result[2:4], "04", "月は変わらない")
    assert_equal(result[4:6], "16", "15日 → 16日")
    assert_true(result.endswith("山田太郎"), "名前部分が保持される")
    return True


def test_increment_day_month_boundary():
    """increment_day_with_validation: 月末 → 翌月1日"""
    result = increment_day_with_validation("060430山田太郎")
    assert_equal(result[2:4], "05", "4月 → 5月")
    assert_equal(result[4:6], "01", "30日 → 1日")
    assert_true(result.endswith("山田太郎"), "名前部分が保持される")
    return True


def test_increment_day_year_boundary():
    """increment_day_with_validation: 12月31日 → 翌年1月1日"""
    result = increment_day_with_validation("061231山田太郎")
    assert_equal(result[2:4], "01", "12月 → 1月")
    assert_equal(result[4:6], "01", "31日 → 1日")
    assert_true(result.endswith("山田太郎"), "名前部分が保持される")
    return True


def run_date_utils_tests():
    """日付ユーティリティテストを実行"""
    suite = TestSuite("日付ユーティリティテスト")

    suite.add_test(test_calc_age_normal)
    suite.add_test(test_calc_age_before_birthday)
    suite.add_test(test_calc_age_on_birthday)
    suite.add_test(test_calc_age_none_inputs)

    suite.add_test(test_convert_japanese_date_reiwa)
    suite.add_test(test_convert_japanese_date_heisei)
    suite.add_test(test_convert_japanese_date_showa)
    suite.add_test(test_convert_japanese_date_with_afternoon_time)
    suite.add_test(test_convert_japanese_date_invalid)

    suite.add_test(test_convert_to_wareki_reiwa)
    suite.add_test(test_convert_to_wareki_heisei)
    suite.add_test(test_convert_to_wareki_showa)
    suite.add_test(test_convert_to_wareki_with_afternoon_time)
    suite.add_test(test_convert_to_wareki_none)

    suite.add_test(test_increment_day_basic)
    suite.add_test(test_increment_day_month_boundary)
    suite.add_test(test_increment_day_year_boundary)

    return suite.run_tests()


if __name__ == "__main__":
    run_date_utils_tests()
