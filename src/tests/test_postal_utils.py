"""
郵便番号ユーティリティのテストケース
外部 API (zipcloud) は unittest.mock でモックして通信なしでテスト
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from unittest.mock import patch, MagicMock
from test_framework import TestSuite, assert_equal, assert_true, assert_false
from utils.postal_utils import lookup_postal_code


# --- 入力バリデーション ---

def test_postal_utils_invalid_non_digit():
    """lookup_postal_code: 数字以外のみの入力は None"""
    result = lookup_postal_code("abc-defg")
    assert_equal(result, None, "数字以外はNone")
    return True


def test_postal_utils_too_short():
    """lookup_postal_code: 6桁は None"""
    result = lookup_postal_code("123456")
    assert_equal(result, None, "6桁はNone")
    return True


def test_postal_utils_too_long():
    """lookup_postal_code: 8桁は None"""
    result = lookup_postal_code("12345678")
    assert_equal(result, None, "8桁はNone")
    return True


def test_postal_utils_empty_string():
    """lookup_postal_code: 空文字は None"""
    result = lookup_postal_code("")
    assert_equal(result, None, "空文字はNone")
    return True


def test_postal_utils_only_hyphens():
    """lookup_postal_code: ハイフンのみは None"""
    result = lookup_postal_code("---")
    assert_equal(result, None, "ハイフンのみはNone")
    return True


# --- 正常系（API モック） ---

def _make_mock_response(status=200, results=None):
    """urllib.request.urlopen が返す偽レスポンスを生成"""
    payload = {'status': status, 'results': results}
    encoded = json.dumps(payload).encode('utf-8')
    mock_resp = MagicMock()
    mock_resp.read.return_value = encoded
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


_SAMPLE_RESULT = [{
    'address1': '東京都',
    'address2': '渋谷区',
    'address3': '道玄坂',
}]


def test_postal_utils_valid_7digit_no_hyphen():
    """lookup_postal_code: 7桁数字（ハイフンなし）で正常取得"""
    with patch('urllib.request.urlopen', return_value=_make_mock_response(200, _SAMPLE_RESULT)):
        result = lookup_postal_code("1500043")
    assert_true(result is not None, "結果が返る")
    assert_equal(result['pref'], '東京都', "都道府県が正しい")
    assert_equal(result['city'], '渋谷区', "市区町村が正しい")
    assert_equal(result['town'], '道玄坂', "町域が正しい")
    assert_equal(result['address'], '東京都渋谷区道玄坂', "連結住所が正しい")
    return True


def test_postal_utils_valid_with_hyphen():
    """lookup_postal_code: ハイフンあり郵便番号で正常取得"""
    with patch('urllib.request.urlopen', return_value=_make_mock_response(200, _SAMPLE_RESULT)):
        result = lookup_postal_code("150-0043")
    assert_true(result is not None, "ハイフンありでも結果が返る")
    assert_equal(result['pref'], '東京都', "都道府県が正しい")
    return True


def test_postal_utils_returns_dict_keys():
    """lookup_postal_code: 返却辞書に pref/city/town/address キーが含まれる"""
    with patch('urllib.request.urlopen', return_value=_make_mock_response(200, _SAMPLE_RESULT)):
        result = lookup_postal_code("1500043")
    assert_true('pref' in result, "pref キーが含まれる")
    assert_true('city' in result, "city キーが含まれる")
    assert_true('town' in result, "town キーが含まれる")
    assert_true('address' in result, "address キーが含まれる")
    return True


# --- 異常系（API モック） ---

def test_postal_utils_api_status_not_200():
    """lookup_postal_code: APIステータス非200はNone"""
    with patch('urllib.request.urlopen',
               return_value=_make_mock_response(400, None)):
        result = lookup_postal_code("1500043")
    assert_equal(result, None, "ステータス400はNone")
    return True


def test_postal_utils_api_results_none():
    """lookup_postal_code: results=None はNone"""
    with patch('urllib.request.urlopen',
               return_value=_make_mock_response(200, None)):
        result = lookup_postal_code("9999999")
    assert_equal(result, None, "結果なしはNone")
    return True


def test_postal_utils_api_results_empty():
    """lookup_postal_code: results=[] はNone"""
    with patch('urllib.request.urlopen',
               return_value=_make_mock_response(200, [])):
        result = lookup_postal_code("9999999")
    assert_equal(result, None, "空の結果リストはNone")
    return True


def test_postal_utils_network_error_returns_none():
    """lookup_postal_code: 通信エラーはNone（例外を伝播しない）"""
    with patch('urllib.request.urlopen', side_effect=Exception("connection refused")):
        result = lookup_postal_code("1500043")
    assert_equal(result, None, "通信エラーはNone")
    return True


def test_postal_utils_timeout_returns_none():
    """lookup_postal_code: タイムアウトはNone"""
    import urllib.error
    with patch('urllib.request.urlopen',
               side_effect=urllib.error.URLError("timed out")):
        result = lookup_postal_code("1500043")
    assert_equal(result, None, "タイムアウトはNone")
    return True


# --- 入力正規化 ---

def test_postal_utils_strips_hyphens_before_request():
    """lookup_postal_code: ハイフンを除去した7桁でAPIを呼ぶ"""
    captured_url = []

    def mock_urlopen(url, timeout=None):
        captured_url.append(url)
        return _make_mock_response(200, _SAMPLE_RESULT)

    with patch('urllib.request.urlopen', side_effect=mock_urlopen):
        lookup_postal_code("150-0043")

    assert_true(len(captured_url) == 1, "urlopen が1回呼ばれる")
    assert_true("1500043" in captured_url[0], "ハイフン除去後の7桁でリクエスト")
    assert_false("-" in captured_url[0].split("zipcode=")[1], "URLにハイフンが含まれない")
    return True


def test_postal_utils_address_concatenation():
    """lookup_postal_code: address は pref+city+town の連結"""
    results = [{'address1': '北海道', 'address2': '札幌市中央区', 'address3': '大通西'}]
    with patch('urllib.request.urlopen',
               return_value=_make_mock_response(200, results)):
        result = lookup_postal_code("0600042")
    assert_equal(result['address'], '北海道札幌市中央区大通西', "連結住所が正しい")
    return True


def run_postal_utils_tests():
    """郵便番号ユーティリティテストを実行"""
    suite = TestSuite("郵便番号ユーティリティテスト")

    suite.add_test(test_postal_utils_invalid_non_digit)
    suite.add_test(test_postal_utils_too_short)
    suite.add_test(test_postal_utils_too_long)
    suite.add_test(test_postal_utils_empty_string)
    suite.add_test(test_postal_utils_only_hyphens)
    suite.add_test(test_postal_utils_valid_7digit_no_hyphen)
    suite.add_test(test_postal_utils_valid_with_hyphen)
    suite.add_test(test_postal_utils_returns_dict_keys)
    suite.add_test(test_postal_utils_api_status_not_200)
    suite.add_test(test_postal_utils_api_results_none)
    suite.add_test(test_postal_utils_api_results_empty)
    suite.add_test(test_postal_utils_network_error_returns_none)
    suite.add_test(test_postal_utils_timeout_returns_none)
    suite.add_test(test_postal_utils_strips_hyphens_before_request)
    suite.add_test(test_postal_utils_address_concatenation)

    return suite.run_tests()


if __name__ == "__main__":
    run_postal_utils_tests()
