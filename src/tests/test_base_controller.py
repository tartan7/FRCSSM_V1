"""
ベースコントローラーのテストケース
GUI・グローバルモジュールはモックに置き換えて単体テスト
"""
import sys
import os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# TkEasyGUI と services.data_service をモックしてから base_controller をインポート
sys.modules['TkEasyGUI'] = MagicMock()
sys.modules['services.data_service'] = MagicMock()

from test_framework import TestSuite, assert_equal, assert_true, assert_false
from controllers.base_controller import BaseController


def _make_controller():
    """テスト用コントローラーと mock ウィンドウを返す"""
    mock_window = MagicMock()
    return BaseController(mock_window), mock_window


# --- 初期化 ---

def test_base_controller_init():
    """BaseController: 初期化の確認"""
    controller, window = _make_controller()
    assert_equal(controller.window, window, "windowが設定される")
    assert_equal(controller.current_values, {}, "current_valuesは空dict")
    assert_true(controller.data_service is not None, "data_serviceが初期化される")
    return True


# --- update_values ---

def test_base_controller_update_values():
    """BaseController.update_values: 値が更新される"""
    controller, _ = _make_controller()
    values = {"key1": "value1", "key2": 42}
    controller.update_values(values)
    assert_equal(controller.current_values, values, "current_valuesが更新される")
    return True


def test_base_controller_update_values_overwrites():
    """BaseController.update_values: 前の値を完全に上書きする"""
    controller, _ = _make_controller()
    controller.update_values({"old": "data"})
    new_values = {"new": "data"}
    controller.update_values(new_values)
    assert_equal(controller.current_values, new_values, "前の値が上書きされる")
    assert_false("old" in controller.current_values, "古いキーは残らない")
    return True


def test_base_controller_update_values_empty():
    """BaseController.update_values: 空dictも受け付ける"""
    controller, _ = _make_controller()
    controller.update_values({"some": "data"})
    controller.update_values({})
    assert_equal(controller.current_values, {}, "空dictで上書き")
    return True


# --- show_error / show_success / show_confirm ---

def test_base_controller_show_error_calls_popup():
    """BaseController.show_error: sg.popup_error を正しい引数で呼ぶ"""
    import TkEasyGUI as sg
    sg.popup_error.reset_mock()
    controller, _ = _make_controller()
    controller.show_error("テストエラー", "エラータイトル")
    sg.popup_error.assert_called_once_with("テストエラー", title="エラータイトル")
    return True


def test_base_controller_show_error_default_title():
    """BaseController.show_error: デフォルトタイトルは 'エラー'"""
    import TkEasyGUI as sg
    sg.popup_error.reset_mock()
    controller, _ = _make_controller()
    controller.show_error("エラーメッセージ")
    sg.popup_error.assert_called_once_with("エラーメッセージ", title="エラー")
    return True


def test_base_controller_show_success_calls_popup():
    """BaseController.show_success: sg.popup を正しい引数で呼ぶ"""
    import TkEasyGUI as sg
    sg.popup.reset_mock()
    controller, _ = _make_controller()
    controller.show_success("成功メッセージ")
    sg.popup.assert_called_once_with("成功メッセージ", title="成功")
    return True


def test_base_controller_show_confirm_returns_result():
    """BaseController.show_confirm: sg.popup_ok_cancel の戻り値を返す"""
    import TkEasyGUI as sg
    sg.popup_ok_cancel.reset_mock()
    sg.popup_ok_cancel.return_value = "OK"
    controller, _ = _make_controller()
    result = controller.show_confirm("確認してください")
    assert_equal(result, "OK", "popup_ok_cancel の戻り値を返す")
    return True


def test_base_controller_show_confirm_cancel():
    """BaseController.show_confirm: キャンセル時はNoneを返す"""
    import TkEasyGUI as sg
    sg.popup_ok_cancel.reset_mock()
    sg.popup_ok_cancel.return_value = None
    controller, _ = _make_controller()
    result = controller.show_confirm("確認")
    assert_equal(result, None, "キャンセルはNone")
    return True


# --- close_excel_safely ---

def test_base_controller_close_excel_safely():
    """BaseController.close_excel_safely: data_service.cleanup を呼び出す"""
    controller, _ = _make_controller()
    controller.data_service.cleanup.reset_mock()
    controller.close_excel_safely()
    assert_true(controller.data_service.cleanup.called, "cleanupが呼ばれた")
    return True


def test_base_controller_close_excel_safely_on_exception():
    """BaseController.close_excel_safely: 例外が発生しても呼び出し元に伝播しない"""
    controller, _ = _make_controller()
    controller.data_service.cleanup.reset_mock()
    controller.data_service.cleanup.side_effect = Exception("Excel接続エラー")
    controller.close_excel_safely()  # 例外が漏れなければOK
    return True


# --- switch_window ---

def test_base_controller_switch_window_close():
    """BaseController.switch_window: use_hide=False で元ウィンドウを close する"""
    controller, mock_window = _make_controller()
    controller.switch_window([["dummy"]], title="新ウィンドウ", use_hide=False)
    mock_window.close.assert_called_once()
    mock_window.hide.assert_not_called()
    return True


def test_base_controller_switch_window_hide():
    """BaseController.switch_window: use_hide=True で元ウィンドウを hide する"""
    controller, mock_window = _make_controller()
    controller.switch_window([["dummy"]], title="新ウィンドウ", use_hide=True)
    mock_window.hide.assert_called_once()
    mock_window.close.assert_not_called()
    return True


def test_base_controller_switch_window_updates_window():
    """BaseController.switch_window: self.window が新ウィンドウに差し替わる"""
    import TkEasyGUI as sg
    new_mock_window = MagicMock()
    sg.Window.return_value = new_mock_window
    controller, _ = _make_controller()
    controller.switch_window([["dummy"]], title="新ウィンドウ")
    assert_equal(controller.window, new_mock_window, "self.window が更新される")
    return True


def run_base_controller_tests():
    """ベースコントローラーテストを実行"""
    suite = TestSuite("ベースコントローラーテスト")

    suite.add_test(test_base_controller_init)
    suite.add_test(test_base_controller_update_values)
    suite.add_test(test_base_controller_update_values_overwrites)
    suite.add_test(test_base_controller_update_values_empty)
    suite.add_test(test_base_controller_show_error_calls_popup)
    suite.add_test(test_base_controller_show_error_default_title)
    suite.add_test(test_base_controller_show_success_calls_popup)
    suite.add_test(test_base_controller_show_confirm_returns_result)
    suite.add_test(test_base_controller_show_confirm_cancel)
    suite.add_test(test_base_controller_close_excel_safely)
    suite.add_test(test_base_controller_close_excel_safely_on_exception)
    suite.add_test(test_base_controller_switch_window_close)
    suite.add_test(test_base_controller_switch_window_hide)
    suite.add_test(test_base_controller_switch_window_updates_window)

    return suite.run_tests()


if __name__ == "__main__":
    run_base_controller_tests()
