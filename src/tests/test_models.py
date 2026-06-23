"""
データモデルのテストケース
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_framework import TestSuite, assert_equal, assert_true, assert_false
from models.koden_model import KodenModel
from models.flower_model import FlowerModel
from models.condolence_model import CondolenceModel

def test_koden_model_creation():
    """香典モデルの作成テスト"""
    koden = KodenModel()
    assert_equal(koden.row_number, 0, "初期番号は0")
    assert_equal(koden.name, "", "初期名前は空文字")
    assert_equal(koden.price, 0, "初期価格は0")
    assert_false(koden.receipt, "初期領収証はFalse")
    return True

def test_koden_model_validation():
    """香典モデルの検証テスト"""
    koden = KodenModel()
    koden.row_number = 1
    koden.name = "テスト太郎"
    koden.price = 10000
    
    errors = koden.validate()
    assert_equal(len(errors), 0, "有効なデータはエラーなし")
    
    # 無効なデータのテスト
    koden.price = -1000
    errors = koden.validate()
    assert_true(len(errors) > 0, "無効な価格はエラーあり")
    return True

def test_koden_model_display_name():
    """香典モデルの表示名テスト"""
    koden = KodenModel()
    koden.name = "テスト太郎"
    koden.price = 10000
    
    display_name = koden.get_display_name()
    assert_equal(display_name, "テスト太郎 (10,000円)", "表示名が正しい")
    return True

def test_flower_model_creation():
    """供花料モデルの作成テスト"""
    flower = FlowerModel()
    assert_equal(flower.number, 0, "初期番号は0")
    assert_equal(flower.amount, 0, "初期金額は0")
    assert_equal(flower.name, "", "初期名前は空文字")
    assert_false(flower.receipt, "初期領収証はFalse")
    return True

def test_flower_model_validation():
    """供花料モデルの検証テスト"""
    flower = FlowerModel()
    flower.number = 1
    flower.name = "テスト花屋"
    flower.amount = 5000
    
    errors = flower.validate()
    assert_equal(len(errors), 0, "有効なデータはエラーなし")
    
    # 無効なデータのテスト
    flower.amount = -1000
    errors = flower.validate()
    assert_true(len(errors) > 0, "無効な金額はエラーあり")
    return True

def test_condolence_model_creation():
    """弔辞弔電モデルの作成テスト"""
    condolence = CondolenceModel()
    assert_equal(condolence.number, 0, "初期番号は0")
    assert_equal(condolence.company_name, "", "初期会社名は空文字")
    assert_equal(condolence.condolence_message, "", "初期弔辞は空文字")
    assert_false(condolence.check, "初期チェックはFalse")
    return True

def test_condolence_model_validation():
    """弔辞弔電モデルの検証テスト"""
    condolence = CondolenceModel()
    condolence.number = 1
    condolence.company_name = "テスト会社"
    condolence.condolence_message = "お悔やみ申し上げます"
    
    errors = condolence.validate()
    assert_equal(len(errors), 0, "有効なデータはエラーなし")
    return True

def test_condolence_model_message_count():
    """弔辞弔電モデルのメッセージ数テスト"""
    condolence = CondolenceModel()
    condolence.condolence_message = "弔辞メッセージ"
    condolence.telegram_message = "弔電メッセージ"
    
    assert_equal(condolence.get_message_count(), 2, "メッセージ数は2")
    assert_true(condolence.has_condolence(), "弔辞あり")
    assert_true(condolence.has_telegram(), "弔電あり")
    return True

def run_model_tests():
    """モデルテストを実行"""
    suite = TestSuite("データモデルテスト")
    
    # 香典モデルのテスト
    suite.add_test(test_koden_model_creation)
    suite.add_test(test_koden_model_validation)
    suite.add_test(test_koden_model_display_name)
    
    # 供花料モデルのテスト
    suite.add_test(test_flower_model_creation)
    suite.add_test(test_flower_model_validation)
    
    # 弔辞弔電モデルのテスト
    suite.add_test(test_condolence_model_creation)
    suite.add_test(test_condolence_model_validation)
    suite.add_test(test_condolence_model_message_count)
    
    return suite.run_tests()

if __name__ == "__main__":
    run_model_tests()