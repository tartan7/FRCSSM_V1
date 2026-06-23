"""
イベント処理テスト
各機能ボタンのイベント処理をテスト
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_framework import TestSuite, assert_equal, assert_true, assert_false, Mock
from controllers.main_controller import MainController
from controllers.koden_controller import KodenController
from controllers.funeral_controller import FuneralController
from controllers.flower_controller import FlowerController
from controllers.condolence_controller import CondolenceController
from controllers.construction_controller import ConstructionController
import TkEasyGUI as sg
from unittest.mock import Mock, patch

def test_main_controller_initialization():
    """メインコントローラーの初期化テスト"""
    # モックウィンドウを作成
    mock_window = Mock()
    mock_window.read.return_value = (sg.WIN_CLOSED, {})
    
    controller = MainController(mock_window)
    assert_true(controller is not None, "メインコントローラーが初期化される")
    assert_true(hasattr(controller, 'event_handlers'), "イベントハンドラーが存在する")
    return True

def test_main_controller_event_handlers():
    """メインコントローラーのイベントハンドラーテスト"""
    mock_window = Mock()
    controller = MainController(mock_window)
    
    # 主要なイベントハンドラーが存在することを確認
    expected_events = [
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
    
    for event in expected_events:
        assert_true(event in controller.event_handlers, f"イベントハンドラー '{event}' が存在する")
    
    return True

def test_koden_controller_functionality():
    """香典コントローラーの機能テスト"""
    mock_window = Mock()
    controller = KodenController(mock_window)

    # 基本的なメソッドが存在することを確認
    assert_true(hasattr(controller, 'handle_koden_input'), "香典入力ハンドラーが存在する")
    assert_true(hasattr(controller, 'data_service'), "データサービスが存在する")

    return True

def test_funeral_controller_functionality():
    """葬儀コントローラーの機能テスト"""
    mock_window = Mock()
    controller = FuneralController(mock_window)

    # 基本的なメソッドが存在することを確認
    assert_true(hasattr(controller, 'handle_basic_info_input'), "葬儀入力ハンドラーが存在する")
    assert_true(hasattr(controller, 'handle_funeral_data_save'), "葬儀保存ハンドラーが存在する")
    assert_true(hasattr(controller, 'handle_calendar_event'), "カレンダーイベントハンドラーが存在する")

    return True

def test_flower_controller_functionality():
    """供花コントローラーの機能テスト"""
    mock_window = Mock()
    controller = FlowerController(mock_window)

    # 基本的なメソッドが存在することを確認
    assert_true(hasattr(controller, 'handle_flower_input'), "供花入力ハンドラーが存在する")
    assert_true(hasattr(controller, 'data_service'), "データサービスが存在する")

    return True

def test_condolence_controller_functionality():
    """弔辞弔電コントローラーの機能テスト"""
    mock_window = Mock()
    controller = CondolenceController(mock_window)

    # 基本的なメソッドが存在することを確認
    assert_true(hasattr(controller, 'handle_condolence_input'), "弔辞弔電入力ハンドラーが存在する")
    assert_true(hasattr(controller, 'data_service'), "データサービスが存在する")

    return True

def test_construction_controller_functionality():
    """施工状況コントローラーの機能テスト"""
    mock_window = Mock()
    controller = ConstructionController(mock_window)

    # 基本的なメソッドが存在することを確認
    assert_true(hasattr(controller, 'handle_construction_input'), "施工状況入力ハンドラーが存在する")
    assert_true(hasattr(controller, 'handle_construction_update'), "施工状況更新ハンドラーが存在する")
    assert_true(hasattr(controller, 'handle_print_operations'), "印刷操作ハンドラーが存在する")

    return True

def test_event_handling_with_mock():
    """モックを使用したイベント処理テスト"""
    mock_window = Mock()
    controller = MainController(mock_window)
    
    # 各イベントをテスト
    test_events = [
        ('-sm00-', '基本情報・施工情報入力'),
        ('-sm01-', '香典入力'),
        ('-sm02-', '供花料入力'),
        ('-sm03-', '弔辞弔電入力'),
        ('-sm04-', '会計情報入力'),
        ('-sm05-', '供物入力'),
        ('-sm06-', '焼香順入力'),
        ('-sm08-', 'フォルダ作成・設定'),
        ('-sm13-', '清書出力'),
        ('-sm14-', '詳細設定'),
        ('-sm15-', '通夜集計'),
        ('-sm16-', '葬儀集計'),
        ('-sm17-', '寺院詳細別紙作成・出力'),
        ('-sm18-', '施工状況入力・袋印刷'),
        ('-Quit-', '終了')
    ]
    
    for event, description in test_events:
        try:
            # イベントハンドラーを呼び出し
            handler = controller.event_handlers.get(event)
            assert_true(handler is not None, f"イベント '{event}' ({description}) のハンドラーが存在する")
            
            # ハンドラーが呼び出し可能であることを確認
            assert_true(callable(handler), f"イベント '{event}' ({description}) のハンドラーが呼び出し可能")
            
        except Exception as e:
            assert_false(True, f"イベント '{event}' ({description}) の処理でエラー: {str(e)}")
    
    return True

def test_window_creation_and_destruction():
    """ウィンドウの作成と破棄テスト"""
    try:
        # テスト用のレイアウトを作成
        layout = [
            [sg.Text("テストウィンドウ")],
            [sg.Button("テストボタン", key="-test-")],
            [sg.Button("閉じる", key="-close-")]
        ]
        
        # ウィンドウを作成
        window = sg.Window("テスト", layout, finalize=True)
        assert_true(window is not None, "ウィンドウが作成される")
        
        # ウィンドウを閉じる
        window.close()
        assert_true(True, "ウィンドウが正常に閉じられる")
        
    except Exception as e:
        assert_false(True, f"ウィンドウの作成・破棄でエラー: {str(e)}")
    
    return True

def test_controller_error_handling():
    """コントローラーのエラーハンドリングテスト"""
    mock_window = Mock()
    controller = MainController(mock_window)

    # 存在しないイベントをテスト（例外が発生しないことを確認）
    try:
        result = controller.handle_event("nonexistent_event", {})
        # handle_event は True を返してループを継続させる（これも正常な動作）
        assert_true(result is None or result is False or result is True,
                    "存在しないイベントは例外なく処理される")
    except Exception as e:
        assert_false(True, f"存在しないイベントの処理でエラー: {str(e)}")

    return True

def test_data_service_integration():
    """データサービスの統合テスト"""
    from services.data_service import DataService
    
    try:
        data_service = DataService()
        assert_true(data_service is not None, "データサービスが初期化される")
        
        # 基本的なメソッドが存在することを確認
        assert_true(hasattr(data_service, 'get_koden_data'), "香典データ取得メソッドが存在する")
        assert_true(hasattr(data_service, 'save_koden_data'), "香典データ保存メソッドが存在する")
        assert_true(hasattr(data_service, 'get_funeral_data'), "葬儀データ取得メソッドが存在する")
        assert_true(hasattr(data_service, 'save_funeral_data'), "葬儀データ保存メソッドが存在する")
        
    except Exception as e:
        assert_false(True, f"データサービスの統合でエラー: {str(e)}")
    
    return True

def test_excel_service_integration():
    """Excelサービスの統合テスト"""
    from services.excel_service import ExcelService
    
    try:
        excel_service = ExcelService()
        assert_true(excel_service is not None, "Excelサービスが初期化される")
        
        # 基本的なメソッドが存在することを確認
        assert_true(hasattr(excel_service, 'open_workbook'), "ワークブック開くメソッドが存在する")
        assert_true(hasattr(excel_service, 'close_workbook'), "ワークブック閉じるメソッドが存在する")
        assert_true(hasattr(excel_service, 'read_cell_value'), "セル読み取りメソッドが存在する")
        assert_true(hasattr(excel_service, 'write_cell_value'), "セル書き込みメソッドが存在する")
        
    except Exception as e:
        assert_false(True, f"Excelサービスの統合でエラー: {str(e)}")
    
    return True

def test_validation_service_integration():
    """バリデーションサービスの統合テスト"""
    from services.validation_service import ValidationService
    
    try:
        validation_service = ValidationService()
        assert_true(validation_service is not None, "バリデーションサービスが初期化される")
        
        # 基本的なメソッドが存在することを確認
        assert_true(hasattr(validation_service, 'validate_required'), "必須項目検証メソッドが存在する")
        assert_true(hasattr(validation_service, 'validate_number'), "数値検証メソッドが存在する")
        assert_true(hasattr(validation_service, 'validate_price'), "価格検証メソッドが存在する")
        assert_true(hasattr(validation_service, 'validate_name'), "名前検証メソッドが存在する")
        
    except Exception as e:
        assert_false(True, f"バリデーションサービスの統合でエラー: {str(e)}")
    
    return True

def run_event_handling_tests():
    """イベント処理テストを実行"""
    suite = TestSuite("イベント処理テスト")
    
    # コントローラーのテスト
    suite.add_test(test_main_controller_initialization)
    suite.add_test(test_main_controller_event_handlers)
    suite.add_test(test_koden_controller_functionality)
    suite.add_test(test_funeral_controller_functionality)
    suite.add_test(test_flower_controller_functionality)
    suite.add_test(test_condolence_controller_functionality)
    suite.add_test(test_construction_controller_functionality)
    
    # イベント処理のテスト
    suite.add_test(test_event_handling_with_mock)
    suite.add_test(test_window_creation_and_destruction)
    suite.add_test(test_controller_error_handling)
    
    # サービスの統合テスト
    suite.add_test(test_data_service_integration)
    suite.add_test(test_excel_service_integration)
    suite.add_test(test_validation_service_integration)
    
    return suite.run_tests()

if __name__ == "__main__":
    run_event_handling_tests()