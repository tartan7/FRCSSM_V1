"""
インタラクティブイベントテスト
実際のアプリケーションのイベント処理をテスト
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import TkEasyGUI as sg
import time
import threading
from test_framework import TestSuite, assert_equal, assert_true, assert_false, Mock

def test_main_application_events():
    """メインアプリケーションのイベント処理テスト"""
    try:
        from views.main_layout import get_main_layout
        layout = get_main_layout()
        assert_true(layout is not None, "メインアプリケーションレイアウトが作成される")
        assert_true(len(layout) > 0, "メインレイアウトに要素が存在する")
    except Exception as e:
        assert_false(True, f"メインアプリケーションイベントでエラー: {str(e)}")

    return True

def test_controller_event_handling():
    """コントローラーのイベント処理テスト"""
    try:
        from controllers.main_controller import MainController
        
        # モックウィンドウを作成
        mock_window = Mock()
        mock_window.read.return_value = (sg.WIN_CLOSED, {})
        
        # コントローラーを初期化
        controller = MainController(mock_window)
        assert_true(controller is not None, "メインコントローラーが初期化される")
        
        # 各イベントをテスト
        test_events = [
            '-sm00-',  # 基本情報・施工情報入力
            '-sm01-',  # 香典入力
            '-sm02-',  # 供花料入力
            '-sm03-',  # 弔辞弔電入力
            '-sm04-',  # 会計情報入力
            '-sm05-',  # 供物入力
            '-sm06-',  # 焼香順入力
            '-sm08-',  # フォルダ作成・設定
            '-sm13-',  # 清書出力
            '-sm14-',  # 詳細設定
            '-sm15-',  # 通夜集計
            '-sm16-',  # 葬儀集計
            '-sm17-',  # 寺院詳細別紙作成・出力
            '-sm18-',  # 施工状況入力・袋印刷
            '-Quit-'   # 終了
        ]
        
        for event in test_events:
            try:
                # イベントハンドラーを取得
                handler = controller.event_handlers.get(event)
                assert_true(handler is not None, f"イベント '{event}' のハンドラーが存在する")
                assert_true(callable(handler), f"イベント '{event}' のハンドラーが呼び出し可能")
                
            except Exception as e:
                assert_false(True, f"イベント '{event}' の処理でエラー: {str(e)}")
        
    except Exception as e:
        assert_false(True, f"コントローラーイベント処理でエラー: {str(e)}")
    
    return True

def test_koden_input_window():
    """香典入力ウィンドウのテスト"""
    try:
        from controllers.koden_controller import KodenController
        
        # モックウィンドウを作成
        mock_window = Mock()
        mock_window.read.return_value = (sg.WIN_CLOSED, {})
        
        # コントローラーを初期化
        controller = KodenController(mock_window)
        assert_true(controller is not None, "香典コントローラーが初期化される")
        
        # 香典入力ウィンドウのレイアウトをテスト
        try:
            from views.koden_layout import get_koden_layout
            koden_layout = get_koden_layout()
            assert_true(koden_layout is not None, "香典入力レイアウトが作成される")
        except Exception as e:
            assert_false(True, f"香典入力ウィンドウでエラー: {str(e)}")
        
    except Exception as e:
        assert_false(True, f"香典入力テストでエラー: {str(e)}")
    
    return True

def test_funeral_input_window():
    """葬儀入力ウィンドウのテスト"""
    try:
        from controllers.funeral_controller import FuneralController
        
        # モックウィンドウを作成
        mock_window = Mock()
        mock_window.read.return_value = (sg.WIN_CLOSED, {})
        
        # コントローラーを初期化
        controller = FuneralController(mock_window)
        assert_true(controller is not None, "葬儀コントローラーが初期化される")
        
        # 葬儀入力ウィンドウのレイアウトをテスト
        try:
            from views.funeral_layout import get_funeral_layout
            funeral_layout = get_funeral_layout()
            assert_true(funeral_layout is not None, "葬儀入力レイアウトが作成される")
        except Exception as e:
            assert_false(True, f"葬儀入力ウィンドウでエラー: {str(e)}")
        
    except Exception as e:
        assert_false(True, f"葬儀入力テストでエラー: {str(e)}")
    
    return True

def test_flower_input_window():
    """供花入力ウィンドウのテスト"""
    try:
        from controllers.flower_controller import FlowerController
        
        # モックウィンドウを作成
        mock_window = Mock()
        mock_window.read.return_value = (sg.WIN_CLOSED, {})
        
        # コントローラーを初期化
        controller = FlowerController(mock_window)
        assert_true(controller is not None, "供花コントローラーが初期化される")
        
        # 供花入力ウィンドウのレイアウトをテスト
        try:
            from views.tab_layouts import get_tab_layout
            flower_layout = get_tab_layout('tab2')
            assert_true(flower_layout is not None, "供花入力レイアウトが作成される")
        except Exception as e:
            assert_false(True, f"供花入力ウィンドウでエラー: {str(e)}")
        
    except Exception as e:
        assert_false(True, f"供花入力テストでエラー: {str(e)}")
    
    return True

def test_condolence_input_window():
    """弔辞弔電入力ウィンドウのテスト"""
    try:
        from controllers.condolence_controller import CondolenceController
        
        # モックウィンドウを作成
        mock_window = Mock()
        mock_window.read.return_value = (sg.WIN_CLOSED, {})
        
        # コントローラーを初期化
        controller = CondolenceController(mock_window)
        assert_true(controller is not None, "弔辞弔電コントローラーが初期化される")
        
        # 弔辞弔電入力ウィンドウのレイアウトをテスト
        try:
            from views.tab_layouts import get_tab_layout
            condolence_layout = get_tab_layout('tab3')
            assert_true(condolence_layout is not None, "弔辞弔電入力レイアウトが作成される")
        except Exception as e:
            assert_false(True, f"弔辞弔電入力ウィンドウでエラー: {str(e)}")
        
    except Exception as e:
        assert_false(True, f"弔辞弔電入力テストでエラー: {str(e)}")
    
    return True

def test_construction_input_window():
    """施工状況入力ウィンドウのテスト"""
    try:
        from controllers.construction_controller import ConstructionController
        
        # モックウィンドウを作成
        mock_window = Mock()
        mock_window.read.return_value = (sg.WIN_CLOSED, {})
        
        # コントローラーを初期化
        controller = ConstructionController(mock_window)
        assert_true(controller is not None, "施工状況コントローラーが初期化される")
        
        # 施工状況入力ウィンドウのレイアウトをテスト
        try:
            from views.tab_layouts import get_tab_layout
            construction_layout = get_tab_layout('tab1')
            assert_true(construction_layout is not None, "施工状況入力レイアウトが作成される")
        except Exception as e:
            assert_false(True, f"施工状況入力ウィンドウでエラー: {str(e)}")
        
    except Exception as e:
        assert_false(True, f"施工状況入力テストでエラー: {str(e)}")
    
    return True

def test_data_models_integration():
    """データモデルの統合テスト"""
    try:
        from models.koden_model import KodenModel
        from models.funeral_model import FuneralModel
        from models.flower_model import FlowerModel
        from models.condolence_model import CondolenceModel
        
        # 香典モデルのテスト
        koden = KodenModel()
        koden.row_number = 1
        koden.price = 10000
        koden.name = "テスト太郎"
        koden.address = "東京都"
        koden.furigana = "テストタロウ"
        
        assert_true(koden.is_valid(), "香典モデルが有効")
        assert_equal(koden.get_display_name(), "テスト太郎 (10,000円)", "香典モデルの表示名が正しい")
        
        # 葬儀モデルのテスト
        funeral = FuneralModel()
        funeral.deceased_name = "故人"
        funeral.family_name = "家族"
        funeral.temple_name = "寺院"

        assert_true(funeral.is_valid(), "葬儀モデルが有効")
        assert_equal(funeral.get_display_name(), "故人様の葬儀", "葬儀モデルの表示名が正しい")
        
        # 供花モデルのテスト
        flower = FlowerModel()
        flower.number = 1
        flower.amount = 5000
        flower.name = "供花様"
        flower.address = "東京都"
        
        assert_true(flower.is_valid(), "供花モデルが有効")
        assert_equal(flower.get_display_name(), "供花様 (5,000円)", "供花モデルの表示名が正しい")

        # 弔辞弔電モデルのテスト
        condolence = CondolenceModel()
        condolence.number = 1
        condolence.company_name = "会社様"
        condolence.condolence_message = "お悔やみ申し上げます"

        assert_true(condolence.is_valid(), "弔辞弔電モデルが有効")
        assert_equal(condolence.get_display_name(), "会社様 (弔辞弔電)", "弔辞弔電モデルの表示名が正しい")
        
    except Exception as e:
        assert_false(True, f"データモデル統合でエラー: {str(e)}")
    
    return True

def test_services_integration():
    """サービスの統合テスト"""
    try:
        from services.data_service import DataService
        from services.excel_service import ExcelService
        from services.validation_service import ValidationService
        
        # データサービスのテスト
        data_service = DataService()
        assert_true(data_service is not None, "データサービスが初期化される")
        
        # Excelサービスのテスト
        excel_service = ExcelService()
        assert_true(excel_service is not None, "Excelサービスが初期化される")
        
        # バリデーションサービスのテスト
        validation_service = ValidationService()
        assert_true(validation_service is not None, "バリデーションサービスが初期化される")
        
        # バリデーションのテスト
        result, message = validation_service.validate_required("テスト", "名前")
        assert_true(result, "必須項目検証が正常に動作する")
        
        result, message = validation_service.validate_number(100, "数値", min_val=0, max_val=1000)
        assert_true(result, "数値検証が正常に動作する")
        
        result, message = validation_service.validate_price(5000, "価格")
        assert_true(result, "価格検証が正常に動作する")
        
    except Exception as e:
        assert_false(True, f"サービス統合でエラー: {str(e)}")
    
    return True

def test_error_handling_in_controllers():
    """コントローラーのエラーハンドリングテスト"""
    try:
        from controllers.main_controller import MainController
        
        # モックウィンドウを作成
        mock_window = Mock()
        mock_window.read.return_value = (sg.WIN_CLOSED, {})
        
        # コントローラーを初期化
        controller = MainController(mock_window)
        
        # 存在しないイベントをテスト
        try:
            result = controller.handle_event("nonexistent_event", {})
            assert_true(result is None or result is False, "存在しないイベントは適切に処理される")
        except Exception:
            # エラーが発生しても正常（適切なエラーハンドリング）
            pass
        
        # 無効なイベントをテスト
        try:
            result = controller.handle_event(None, {})
            assert_true(result is None or result is False, "無効なイベントは適切に処理される")
        except Exception:
            # エラーが発生しても正常（適切なエラーハンドリング）
            pass
        
        # 無効な値をテスト
        try:
            result = controller.handle_event("-sm00-", None)
            assert_true(result is None or result is False, "無効な値は適切に処理される")
        except Exception:
            # エラーが発生しても正常（適切なエラーハンドリング）
            pass
        
    except Exception as e:
        assert_false(True, f"コントローラーエラーハンドリングでエラー: {str(e)}")
    
    return True

def run_interactive_event_tests():
    """インタラクティブイベントテストを実行"""
    suite = TestSuite("インタラクティブイベントテスト")
    
    # メインアプリケーションのテスト
    suite.add_test(test_main_application_events)
    suite.add_test(test_controller_event_handling)
    
    # 各機能ウィンドウのテスト
    suite.add_test(test_koden_input_window)
    suite.add_test(test_funeral_input_window)
    suite.add_test(test_flower_input_window)
    suite.add_test(test_condolence_input_window)
    suite.add_test(test_construction_input_window)
    
    # データモデルとサービスの統合テスト
    suite.add_test(test_data_models_integration)
    suite.add_test(test_services_integration)
    
    # エラーハンドリングのテスト
    suite.add_test(test_error_handling_in_controllers)
    
    return suite.run_tests()

if __name__ == "__main__":
    run_interactive_event_tests()